from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
tab_names = [tab.stem.replace("_", " ").title() for tab in Path(BASE_DIR / "cyphers").iterdir()]

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"tabs": tab_names})