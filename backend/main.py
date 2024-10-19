from fastapi import FastAPI
import uvicorn
from app.routers import tasks_router


app = FastAPI()

app.include_router(tasks_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9090)
