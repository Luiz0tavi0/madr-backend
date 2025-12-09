from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from madr.api.v1.router import routers

app = FastAPI()
origins = ['http://localhost:3000', 'http://127.0.0.1:3000']


[app.include_router(router) for router in routers]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
