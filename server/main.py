from controller import app
from fastapi import FastAPI
import uvicorn

MainApp = FastAPI()
MainApp.mount("/control", app)


if __name__ == "__main__":
    uvicorn.run(MainApp, host="0.0.0.0", log_level="debug")
