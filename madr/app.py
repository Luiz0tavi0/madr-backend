from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from madr.api.v1.router import routers

app = FastAPI()
origins = [
    'http://localhost',
    'http://localhost:8080',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

[app.include_router(router) for router in routers]
