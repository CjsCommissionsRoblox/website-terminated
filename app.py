import html
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic
from sanic.response import html as sanic_html
from sanic.exceptions import NotFound
from jinja2 import Environment, FileSystemLoader

from core.models import LogEntry

load_dotenv()

app = Sanic("LogViewerApp")

app.static("/static", "./static")

jinja_env = Environment(loader=FileSystemLoader("templates"))


def render_template(name, *args, **kwargs):
    template = jinja_env.get_template(name + ".html")
    return sanic_html(template.render(*args, **kwargs))


@app.exception(NotFound)
async def not_found_handler(request, exception):
    return render_template("not_found")


@app.get("/")
async def index(request):
    return render_template("not_found")


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8096)),
        debug=os.getenv("DEBUG", "false").lower() == "true"
    )
