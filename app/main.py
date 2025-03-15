from fastapi import FastAPI
import uvicorn
from app.db.utils import init_db
from app.routers import categories, problems, real_world_examples, solutions

app = FastAPI()
init_db()


app.include_router(categories.router)
app.include_router(problems.router)
app.include_router(real_world_examples.router)
app.include_router(solutions.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)