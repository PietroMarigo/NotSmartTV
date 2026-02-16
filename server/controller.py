from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import requests
import input


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


app = FastAPI()


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
async def remote(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/key/{button_name}")
async def press_button(button_name: str):
    r = input.press(button_name)
    if not r:
        raise HTTPException(status_code=404, detail="Nah braw")
    return {"status": "pressed", "key": button_name}


@app.websocket("/ws/mouse")
async def mouse_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if "," in data:
                x, y = data.split(",")
                input.move_mouse(x, y)

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error: {e}")


@app.post("/system/home")
async def system_home():
    try:
        requests.post("http://localhost:8002/select/launch/home", timeout=1)
        return {"status": "forward"}
    except Exception as e:
        return {"status": "error", "messege": f"{e}"}


@app.post("/system/close")
async def close_all():
    try:
        requests.post("http://localhost:8002/select/launch/close", timeout=1)
        return {"status": "forward"}
    except Exception as e:
        return {"status": "error", "messege": f"{e}"}
