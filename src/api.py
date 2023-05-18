import json
from rabi import Rabi    
import threading
from pprint import pprint
import config
from controller import Controller
from fastapi import FastAPI,Form
import uvicorn
from pydantic import BaseModel
from typing import Dict
from log_manager import logger
''' this is the main thread '''
# C = Controller(filepaths=["funcs"])
# C = Controller()

app = FastAPI(
    title="Simphony"
)

''' ------------------------'''

class RunModel(BaseModel):
    dag: str = None
    context: Dict = None

@app.post("/run")
async def run_dag(model: RunModel):
    try:
        logger.info("paylload:",model)
        r = Rabi(q = config.ACK_Q)
        task_obj = {"dag": model.dag,"ctrl":True,"context":model.context}
        r.push_to_q(json.dumps(task_obj))
        r.close()
        db_result = 'Success'
        logger.info("success")
        return {'status': 'Failed'} if db_result == "Failed" else {'status': 'Success'}
    except Exception as e:
        logger.critical(e)
        return {'status': 'Failed'}

