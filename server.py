from sanic import Sanic, text

from auth import protected
from login import login

app = Sanic("AuthApp")
app.config.SECRET = "KEEP_IT_SECRET_KEEP_IT_SAFE"
app.blueprint(login)


@app.get("/secret")
@protected
async def secret(request):
    return text("To go fast, you must be fast.")