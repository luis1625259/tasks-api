import json
from fastapi import FastAPI, HTTPException
from pydantic import Field, BaseModel
app = FastAPI()

class Task(BaseModel):
    title: str = Field(..., example="Fazer compras")
    description: str = Field(..., example="Comprar leite, pão e ovos")
    owner: str = Field(..., example="João")
    status: str = Field(..., example="Pendente")
    comments: list[str] = Field(default_factory=list, example=["Comentário 1", "Comentário 2"])

# Define um simples Get da rota padrão URL("/")
@app.get("/")#Parametro que indica qual verbo será executado 
async def get_root_message():
#Define nome da função
#Retorna um objeto JSON com menssagem Ola Mundo 
    return {"message":"Hello World"}

@app.delete("/tasks/{id}")
async def delete_task(id: int):
    tasks_list = await ler_arquivo_json()
    tasks_list["tasks"] = [item for item in tasks_list["tasks"] if item["id"] != id]
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks_list, f, ensure_ascii=False, indent=4)
    return {"message": "Task deletada com sucesso"}


@app.get("/Tasks")
async def buscartodos():
    dados= await ler_arquivo_json()
    return dados ["tasks"]

@app.get("/Tasks/{id}")
async def buscarid(id:int):
    dados= await ler_arquivo_json()
    lista_de_dados = dados ["tasks"]
    tarefa=next((item for item in lista_de_dados if item ["id"]==id),None)
    if tarefa is None:
        raise HTTPException(status_code=404,detail="notfoud")
    return tarefa

@app.post("/tasks")
async def create_task(task: Task):
    tasks = await ler_arquivo_json()
    last_id = tasks["tasks"][-1]["id"] if tasks["tasks"] else 0
    new_task = task.model_dump()
    new_task["id"] = last_id + 1
    tasks["tasks"].append(new_task)
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)
    return new_task

@app.put("/tasks/{id}")
async def update_task(id: int, task: Task):
    tasks_data = await ler_arquivo_json()
    tasks_list = tasks_data["tasks"]
    index = next((i for i, item in enumerate(tasks_list) if item["id"] == id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = task.model_dump()
    updated["id"] = id
    tasks_list[index] = updated
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=4)
    return updated





async def ler_arquivo_json():
    with open("tasks.json",encoding="utf-8") as f:
        dados = json.load(f)
    return dados

