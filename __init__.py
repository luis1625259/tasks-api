from contextlib import AbstractAsyncContextManager
from fastapi import fastapi

@AbstractAsyncContextManager
async def lifespan(_:fastapi):
    app = fastapi(
        title ="todo API"
        description = "API para gerenciamento de tarefas com arquitetura em comandos",
        version="1.0.0"
        lifespan = lifespan,
        contact = {
            "name":"Equipe da disciplina INF8B",

        },)
    return app
    
    