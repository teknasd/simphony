# simphony

## a bare metal orchestrator made with python and rabbit and reddis

```
python -> to write code
rabbit -> to maintain queues
reddis -> to maintain states
```

### How to use it:
- write loose functions in dags/funcs.py
- Define it as ``` Make(funcA) >> Make(funcB) ``` to make link
- define your dag in controller.py
- run controller.py in one shell
- run worker.py in as many shells you want


### TODO:
- connector for redis
- auto push pull from redis using task ids using decorators
- save dag_ids and task_ids in db 
- write connectors for sqlite,mysql,postgres etc
- keep flag of STATELESS to skip all DB operations and use redis only
- multitreading in workers (concurrency)
- multiprocessing in workers (parallelization)
- Have controller in class ✅
- FastAPI to trigger dag controller
- use task definations and task flow from same file ✅
- UI ? idk 





