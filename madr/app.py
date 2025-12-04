from fastapi import FastAPI

from madr.api.router import routers

app = FastAPI()

[app.include_router(router) for router in routers]


@app.get('/')
def read_root():
    return {'ola': 'mundo'}
