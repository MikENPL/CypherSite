from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from pathlib import Path
import importlib, inspect
import cyphersite.functions as methods

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
# Name : Module pairs
ciphers = {file.stem : importlib.import_module(f"cyphersite.ciphers.{file.stem}") for file in Path(BASE_DIR / "ciphers").glob("*.py") if file.stem != "__init__"}
tabs = [(methods.parse_title(tab), tab) for tab in ciphers]

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"tabs": tabs})

@app.get("/{cipher_name}")
def cipher_page(request: Request, cipher_name: str):
    module = ciphers[cipher_name]
    title = methods.parse_title(cipher_name)
    functions = {name : func for name, func in inspect.getmembers(module, inspect.isfunction) if getattr(func, "exposed", False)}
    forms = {}
    for func_name in functions:
        forms[func_name] = [(methods.parse_title(param.name), param.annotation.__name__) for param in inspect.signature(functions[func_name]).parameters.values()]
    print(forms)
    return templates.TemplateResponse(request, "cipher.html", {"title": title, "cipher_name": cipher_name, "forms": forms})
