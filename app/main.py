from fastapi import FastAPI
import uvicorn
from db.utils import init_db
from routers import categories, problems, real_world_examples, solutions

app = FastAPI()
init_db()


app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(problems.router, prefix="/problems", tags=["problems"])
app.include_router(real_world_examples.router, prefix="/real_world_examples", tags=["real_world_examples"])
app.include_router(solutions.router, prefix="/solutions", tags=["solutions"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)