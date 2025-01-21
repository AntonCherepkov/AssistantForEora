from .basic_heandlers import router as basic_router
from .dialog_handlers import router as dialog_router

routers = [
    basic_router,
    dialog_router
]