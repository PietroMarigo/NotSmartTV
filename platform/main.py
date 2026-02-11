from controller import app
from fastapi import FastAPI
import uvicorn

Mainapp = FastAPI()
Mainapp.mount("/select", app)


if __name__ == "__main__":
    uvicorn.run(Mainapp, host="0.0.0.0", port=8002, log_level="info")
