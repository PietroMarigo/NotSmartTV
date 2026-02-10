from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
import input

app = FastAPI()


@app.post("/{button_name}")
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
