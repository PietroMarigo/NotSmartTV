from fastapi import FastAPI
import buttons


app = FastAPI()


@app.post("/left")
async def click_left():
    buttons.left()
    return {"status": "pressed", "key": "left"}


@app.post("/right")
async def click_right():
    buttons.right()
    return {"status": "pressed", "key": "right"}


@app.post("/up")
async def click_up():
    buttons.up()
    return {"status": "pressed", "key": "up"}


@app.post("/down")
async def click_dwon():
    buttons.down()
    return {"status": "pressed", "key": "down"}
