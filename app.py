__version__ = "1.1.2"

import html
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic, response
from sanic.exceptions import NotFound
from jinja2 import Environment, FileSystemLoader

from core.models import LogEntry


app = Sanic(__name__)
app.static("/static", "./static")

jinja_env = Environment(loader=FileSystemLoader("templates"))


def render_template(name, *args, **kwargs):
    template = jinja_env.get_template(name + ".html")
    return response.html(template.render(*args, **kwargs))


app.ctx.render_template = render_template

@app.exception(NotFound)
async def not_found(request, exc):
    return render_template("not_found")


@app.get("/")
async def index(request):
    return render_template("not_found")

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=os.getenv("PORT", 8096),
        debug=bool(os.getenv("DEBUG", False)),
    )
