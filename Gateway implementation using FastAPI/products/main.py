from fastapi import FastAPI
import uvicorn
from controller import router as product_router


app = FastAPI(
    api_prefix="/api/v1",
    title="Products Service",
    description="API for managing products",
    version="1.0.0"
)

app.include_router(
    product_router,
    prefix="/product"
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)

