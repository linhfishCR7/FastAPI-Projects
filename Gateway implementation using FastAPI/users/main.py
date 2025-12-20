from fastapi import FastAPI
import uvicorn

from controller import auth_router



app = FastAPI(
    title="Users Service",
    description="API for user registration and authentication",
    version="1.0.0"
)
app.include_router(auth_router, prefix="/auth")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003)