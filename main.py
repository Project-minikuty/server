from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from routes import auth, general, admin,doctor
from dotenv import load_dotenv
from db import get_db
load_dotenv()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    html_content = """
    <html>
        <head>
            <title>Official backend docs of Medlab</title>
            <script>location.replace("/docs");</script>
        </head>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


app.include_router(auth.app)
app.include_router(general.app)
app.include_router(admin.app)
app.include_router(doctor.app)



@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/notFound")


@app.get("/notFound")
@app.post("/notFound")
def notFound():
    return {
    "success": 'false',
    "message": 'Page not found',
    "error": {
      "statusCode": 404,
      "message": 'You reached a route that is not defined on this server',
    },
  }
