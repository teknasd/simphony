import json
from rabi import Rabi    
import threading
from pprint import pprint
import config
from controller import Controller
from fastapi import FastAPI,Form
import uvicorn
from pydantic import BaseModel

''' this is the main thread '''
# C = Controller(filepaths=["funcs"])
# C = Controller()

app = FastAPI(
    title="Simphony"
)

''' ------------------------'''

class RunModel(BaseModel):
    dag: str = None
    context: str = None

@app.post("/run")
async def run_dag(dag: str = Form(...),context: str = Form(...)):
    try:
        print("paylload:",dag,context)
        # C = Controller( [dag + ".py"])
        # print(C.dag_store)
        r = Rabi(q = config.ACK_Q)
        task_obj = {"dag": dag,"ctrl":True}
        r.push_to_q(json.dumps(task_obj))
        r.close()
        db_result = 'Success'
        return {'status': 'Failed'} if db_result == "Failed" else {'status': 'Success'}
    except Exception as e:
        print(e)
        return {'status': 'Failed'}

