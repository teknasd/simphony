from datetime import datetime as dt
from datetime import timedelta
from airflow.utils.dates import days_ago
#The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
#importing the operators required
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.redis.hooks.redis import RedisHook
from airflow.operators.python import get_current_context
from airflow.exceptions import AirflowException

import sys, os, json, requests
import pydicom
sys.path.append("..")
from utils.algos import vuno,aikenist
import utils.get_zip_file as util
#from utils.helper import *
from utils.db import db_config as dbc
import shutil
#sys.path.append("..")
#from utils.get_zip_file import *
state = {}
#these args will get passed to each operator
#these can be overridden on a per-task basis during operator #initialization
#notice the start_date is any date in the past to be able to run it #as soon as it's created
BASEURL = "https://api1.aikenist.com/"

def on_failure_callback(context):
    ti = context.get('ti')
    state = ti.xcom_pull(key='state',task_ids='register.job')
    print(state)
    if state:
        db = dbc.SessionLocal()
        util.update_active_job_status(db, state['job_id'], 'Failed', 'Failed')
        flag,data = util.send_log(db,state["job_id"],'Inferencing failed.','failed',0, msg_id = 9)
        db.close()
        os.remove(state["zip_path"])
        shutil.rmtree(state["unzip_path"])

def on_success_callback(context):
    ti = context.get('ti')
    state = ti.xcom_pull(key='state',task_ids='register.job')
    print(state)
    if state:
        db = dbc.SessionLocal()
        util.update_active_job_status(db, state['job_id'], 'Task processing complete', context['task'].task_id)
        db.close()

default_args = {
'owner' : 'carpl',
'depends_on_past' : False,
'start_date': dt(2022, 2, 15, 8, 15),
'schedule_interval': '*/1 * * * *', #..every 1 minute
'email' : ['example@123.com'],
'email_on_failure' : False,
'email_on_retry' : False,
'retries' : 3,
'retry_delay' : timedelta(seconds=5),
'state' : state,
'catchup': False,
"on_failure_callback": on_failure_callback,
"on_success_callback": on_success_callback,
}

dag = DAG(
'algo.67',
description = 'Aikenist',
default_args = default_args,
schedule_interval='*/1 * * * *',
max_active_runs=4,
catchup=False,
)


def push(state,ti):
    ti.xcom_push(key='state', value=state)
def pull(prev_task,ti):
    return ti.xcom_pull(key='state', task_ids=prev_task)
    
def x(state,ti):
    pass

def get_job(state,ti):
    db = dbc.SessionLocal()
    data = util.get_active_job(db, algo_id='67')
    if data is not None:
        job_id = data.job_id
        state["job_id"] = job_id
        state["zip_path"] = data.path
        db.close()
    else:
        db.close()
        raise AirflowException()
    push(state,ti)

def unzip_file(state,ti):
    print(os.path.abspath(os.path.dirname(__file__)))
    state = pull('register.job',ti)
    status = util.unzip_file(state['zip_path'],state['job_id'],'/opt/tmp_folder')
    if status != "failed":
        state["unzip_path"] = status
    push(state,ti)

def missing_data(state, ti):
    state = pull('unzip', ti)
    push(state,ti)

def zip_file(state,ti):
    state = pull('convert.outputs',ti)
    try:
        status,final_path = util.zip_directory(state['algo_output_path'],'/opt/tmp_folder/', state['job_id'])
        if status != "failed":
            state["final_zip_path"] = final_path
    
    except:
        raise Exception("Could not Zip File")
    push(state,ti)

def choose_valid_xray(state,ti):
    state = pull('unzip',ti)
    push(state,ti)

def extract_jobID(state, ti):
    state = pull('post.request', ti)
    # if(state['post_request_data'] and state['post_request_data']['analysis_id']):
    #     state['algo_job_id'] = state['post_request_data']['analysis_id']
    # else:
    #     raise Exception("Failed while accessing job ID")
    push(state, ti)

def prepare_request_upload(state,ti):
    state = pull('choose.valid.xray',ti)
    login_url = BASEURL + 'auth'
    payload = json.dumps({
        "username": "mahajan@mahajan.com",
        "password": "mahajan@312"
    })
    headers = {
            'Content-Type': 'application/json'
            }
    response = requests.request("POST", login_url, headers=headers, data=payload)
    if response.status_code == 200:
        state["post_url"] = BASEURL + 'api/dcms/upload'
        state["access_token"] = response.json()['access_token']
        state["post_header"] = {
            "Authorization": "JWT " + response.json()['access_token']}
    push(state,ti)

def send_data_request(state,ti):
    state = pull('prepare.request',ti)
    # dicom_files, study_id = aikenist.choose_valid_ct(state['unzip_path'])
    
    #flag, data = True, {'job_id': '4e662a2b530248d8942c2b2fd2fb7d95'}
    flag,data = aikenist.post_request_headct(state,state["unzip_path"])
    print("flag,data",flag,data)
    state["post_request"] = flag
    # state["study_id"] = study_id
    if flag:
        state["post_request_data"] = data
        state["log"] = "Sent file to AI Server"
        state["log_status"] = "success"
    else:
        state["post_request_error"] = data
        state["log"] = data
        state["log_status"] = "failed"
    # state['dicom_files'] = dicom_files
    push(state,ti)


def prepare_predict_request(state, ti):
    state = pull('post.request',ti)

    state["predict_url"] = BASEURL + "api/status?uuid="
    state["predict_header"] = {
            "Authorization": "JWT " + state["access_token"]}
    push(state,ti)

def send_predict_request(state,ti):
    state = pull('prepare.predict.request',ti)
    #flag, data = True, {'job_id': '4e662a2b530248d8942c2b2fd2fb7d95'}
    if(state['post_request_data']):
        uuid_dict = state['post_request_data']
    flag,data = aikenist.predict_request(state,uuid_dict)
    print("flag,data",flag,data)
    state["predict_request"] = flag


    if flag:
        state["log"] = "Inference results received"
        state["log_status"] = "success"
        state["predict_request_results"] = data
    else:
        state["predict_request_error"] = data
        state["log"] = data
        state["log_status"] = "failed"
    # state['dicom_files'] = dicom_files
    push(state,ti)


def convert_output(state, ti):
    state = pull('send.predict.request', ti)

    try:
        output = aikenist.post_process_67(state["predict_request_results"], 
        {},
         '/opt/tmp_folder', 
         state['job_id'])
        state['algo_output_path'] = output
        db = dbc.SessionLocal()
        util.send_log(db,state["job_id"],"Inference completed at AI gateway","success",1, msg_id=9)
        db.close()
    except:
        db = dbc.SessionLocal()
        util.send_log(db,state["job_id"],"Inference failed at AI Server","failed",1, msg_id=9)
        db.close()
        raise AirflowException()

    push(state, ti)

def algorithm_input_validator(state, ti):
    state = pull('unzip', ti)
    state["input_validation"] = True
    push(state, ti)

def send_to_HGW(state,ti):
    state = pull('save.zip', ti)
    db = dbc.SessionLocal()
    flag,data = util.send_to_HGW(db,state["final_zip_path"],state["job_id"])
    util.send_log(db,state["job_id"],"Sending file to hospital gateway","success",1, msg_id=10)

    if flag:
        state["send_output_request_data"] = data
    else:
        state["send_output_request_error"] = data
    db.close()
    try:
        os.remove(state["zip_path"])
    except:
        pass
    try:
        shutil.rmtree(state["unzip_path"])
    except:
        pass
    push(state,ti)

def send_log_1(state,ti):
    state = pull('post.request', ti)
    db = dbc.SessionLocal()
    st = state["log_status"]
    if st == 'failed':
        st = 'Failed'
    flag,data = util.send_log(db,state["job_id"],state["log"],st,0, msg_id=7)
    db.close()
    del state['log']
    push(state,ti)

def send_log_2(state,ti):
    state = pull('send.predict.request', ti)
    print(state)
    db = dbc.SessionLocal()
    st = state["log_status"]
    if st == 'failed':
        st = 'Failed'
    flag,data = util.send_log(db,state["job_id"],state["log"],st,1, msg_id = 8)
    db.close()
    del state['log']
    push(state,ti)

registerJob = PythonOperator(
 task_id = 'register.job', 
 python_callable = get_job,
 op_kwargs={'state':state},
 dag = dag)

unzip = PythonOperator(
 task_id = 'unzip', 
 python_callable = unzip_file,
 op_kwargs={'state':state},
 dag = dag)

input_validator = PythonOperator(
 task_id = 'input.validation', 
 python_callable = algorithm_input_validator,
 op_kwargs={'state':state},
 dag = dag)

choose_valid_xray = PythonOperator(
 task_id = 'choose.valid.xray',
 python_callable = choose_valid_xray,
 op_kwargs={'state':state},
 dag = dag)


#zip_folder = PythonOperator(
 #task_id = 'zip', 
 #python_callable = zip_file,
 #op_kwargs={'state':state},
 #dag = dag)


send_file = PythonOperator(
 task_id = 'post.request', 
 python_callable = send_data_request,
 op_kwargs={'state':state},
 dag = dag)


prepare_request = PythonOperator(
 task_id = 'prepare.request', 
 python_callable = prepare_request_upload,
 op_kwargs={'state':state},
 dag = dag)

prepare_predict_request = PythonOperator(
 task_id = 'prepare.predict.request',
 python_callable = prepare_predict_request,
 op_kwargs={'state':state},
 dag = dag)

send_predict_request = PythonOperator(
 task_id = 'send.predict.request',
 python_callable = send_predict_request,
 op_kwargs={'state':state},
 dag = dag)


send_failed_log_1 = PythonOperator(
 task_id = 'send.failed.log.1', 
 python_callable = send_log_1,
 op_kwargs={'state':state},
 dag = dag)


send_failed_log_2 = PythonOperator(
 task_id = 'send.failed.log.2', 
 python_callable = send_log_2,
 op_kwargs={'state':state},
 dag = dag)

extract_vuno_jobid = PythonOperator(
 task_id = 'extract.vuno.jobid', 
 python_callable = extract_jobID,
 op_kwargs={'state':state},
 dag = dag)

convert_outputs = PythonOperator(
 task_id = 'convert.outputs', 
 python_callable = convert_output,
 op_kwargs={'state':state},
 dag = dag)

sleep = PythonOperator(
 task_id = 'sleep', 
 python_callable = vuno.wait,
 op_kwargs={'state':state},
 dag = dag)

save_zip = PythonOperator(
 task_id = 'save.zip', 
 python_callable = zip_file,
 op_kwargs={'state':state},
 dag = dag)

send_carpl = PythonOperator(
 task_id = 'send.to.HGW', 
 python_callable = send_to_HGW,
 op_kwargs={'state':state},
 dag = dag)

registerJob >> unzip >> input_validator >> choose_valid_xray >> prepare_request >>  send_file
send_file >> send_failed_log_1
send_file >> extract_vuno_jobid >> sleep
sleep >> prepare_predict_request >> send_predict_request >> send_failed_log_2
send_predict_request >> convert_outputs >> save_zip >> send_carpl


