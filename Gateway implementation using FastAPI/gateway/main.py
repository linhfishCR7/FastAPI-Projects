from fastapi import FastAPI, Request
import uvicorn
from network import proxy_request


app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "OK"}


# Catch-all proxy route: forward everything else to configured upstreams
@app.api_route("/rajan/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def gateway_proxy(full_path: str, request: Request):
    return await proxy_request(full_path, request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

