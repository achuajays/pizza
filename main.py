from fastapi import FastAPI, Path, Query
from typing import Optional             
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str

class UPItem(BaseModel):
    name: Optional[str] = None

d = {}

@app.get('/g/{item_id}')
def g(item_id: int):
    return {'data': d.get(item_id, 'not found')}

@app.get('/gt/{test_id}')
def gt(test_id: int, item_name: Optional[str] = None, test: int = 0):
    for i in d:
        if item_name == d[i]['name']:
            return {'data': d[i]}
    return {'data': 'not found'}

@app.post('/c/{item_id}')
def c(item_id: int, item: Item):
    if item_id in d:
        return {'error': 'item_id already exists'}
    d[item_id] = item.dict()
    return {'data': d[item_id]}

@app.put('/u/{item_id}')
def u(item_id: int, item: UPItem):
    if item_id not in d:
        return {'error': 'item_id not found'}
    if item.name is not None:
        d[item_id]['name'] = item.name
    return {'data': d[item_id]}

@app.delete('/d/')
def delete_item(item_id: int = Query(..., description="delete")):
    if item_id not in d:
        return {'error': 'item_id not found'}
    del d[item_id]
    return {'success': 'success'}
