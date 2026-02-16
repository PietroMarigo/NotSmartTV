from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from launcher import select_app, Apps, close_apps

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    context = {
        "request": request,
        "app_list": Apps.keys(),
    }
    return templates.TemplateResponse("tv.html", context)


@app.post("/launch/close")
async def close_all():
    close_apps()


@app.post("/launch/{app_name}")
async def open_service(app_name: str):
    try:
        s = select_app(app_name)
        if not s:
            raise HTTPException(status_code=404, detail="Not an app")
        return {"status": "launching app", "app": app_name}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Something went really wrong {e}")
