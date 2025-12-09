from madr.api.v1.novelists import router as novelists_router
from madr.api.v1.users import router as users_router

routers = [
    users_router,
    novelists_router,
]
