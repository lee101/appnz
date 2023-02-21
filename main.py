# !/usr/bin/env python
import os

import jinja2
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

config = {}
config["webapp2_extras.sessions"] = dict(secret_key="93986c9cdd240540f70efaea56a9e3f2")
from fastapi.middleware.gzip import GZipMiddleware

templates = Jinja2Templates(directory=".")
app = FastAPI(
    openapi_url="/static/openapi.json",
    docs_url="/swagger-docs",
    redoc_url="/redoc",
    title="Generate Text API",
    description="Generate text, control stopping criteria like max_length/max_sentences",
    root_path="https://api.text-generator.io",
    version="1",
)
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    # extensions=['jinja2.ext.autoescape'],
    # autoescape=True
)
config = {'webapp2_extras.sessions': dict(secret_key='93986c9cdd240540f70efaea56a9e3f2')}

app.add_middleware(GZipMiddleware, minimum_size=1000)

# app.add_middleware(HTTPSRedirectMiddleware)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


## serve favicon.ico from root
app.mount("/", StaticFiles(directory="static"), name="favicon")
