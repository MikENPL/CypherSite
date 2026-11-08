from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from pathlib import Path
import importlib, inspect

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
# Name : Module pairs
ciphers = {file.stem : importlib.import_module(f"cyphersite.ciphers.{file.stem}") for file in Path(BASE_DIR / "ciphers").glob("*.py") if file.stem != "__init__"}
tabs = [(tab.replace("_", " ").title(), tab) for tab in ciphers]

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"tabs": tabs})

@app.get("/{cipher_name}")
def cipher_page(request: Request, cipher_name: str):
    module = ciphers[cipher_name]
    functions = {name : func for name, func in inspect.getmembers(module, inspect.isfunction) if getattr(func, "exposed", False)}
    return str(functions)
    return templates.TemplateResponse(request, "cipher.html", {"title": cipher_name.replace("_", " ").title()})
