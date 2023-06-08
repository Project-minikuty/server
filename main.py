from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from routes import auth, general, admin,doctor,parent
from dotenv import load_dotenv
from db import get_db
load_dotenv()


app = FastAPI(title="Medlab backend",
              description="This is the docs for the api's used in medlab",
              version="0.9.12",
              contact={
                  "name": "Tomin Joy",
                  "email": "tominjk007@gmail.com",
              },
              

              )


app.add_middleware(

    CORSMiddleware,
    allow_origins=['*',"https://medlab-mini.netlify.app ","http://localhost:3000"],
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
app.include_router(parent.app)



@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/notFound")


@app.get("/notFound")
@app.post("/notFound")
@app.post("/notFound")
@app.patch("/notFound")
@app.delete("/notFound")
def notFound():
    return {
    "success": 'false',
    "message": 'Page not found',
    "error": {
      "statusCode": 404,
      "message": 'You reached a route that is not defined on this server',
    },
  }

