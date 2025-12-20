from fastapi import FastAPI
import uvicorn

from controller import router as order_router

app = FastAPI()


app.include_router(
    order_router,
    prefix="/order"
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
