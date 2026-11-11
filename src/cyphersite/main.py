from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import importlib, inspect
import cyphersite.functions as methods

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
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
        forms[func_name] = [(param.name, param.annotation.__name__) for param in inspect.signature(functions[func_name]).parameters.values()]
    return templates.TemplateResponse(request, "cipher.html", {"title": title, "cipher_name": cipher_name, "forms": forms})

@app.post("/{cipher_name}/{func_name}")
async def execute_cipher(request: Request, cipher_name: str, func_name: str):
    form_data = dict(await request.form())
    module=ciphers[cipher_name]
    functions = {name : func for name, func in inspect.getmembers(module, inspect.isfunction) if getattr(func, "exposed", False)}
    forms = {}
    for func_name_loop in functions:
        forms[func_name_loop] = [(param.name, param.annotation.__name__) for param in inspect.signature(functions[func_name_loop]).parameters.values()]
    func = getattr(module, func_name)
    result_text = inspect.getdoc(func)
    if result_text is None:
        result_text = ""
    for argument, atype in forms[func_name]:
        match atype:
            case "str":
                continue
            case "int":
                form_data[argument] = int(form_data[argument])
            case "bool":
                if argument in form_data:
                    form_data[argument] = True
    result = (func(**form_data))
    print(result)
    return {"result": result, "result_text": result_text}