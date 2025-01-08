from mongoengine import connect
from fastapi import FastAPI

from blogs.routes import blogroutes
from serive.routes import serviceroutes
from fastapi.middleware.cors import CORSMiddleware

from user.routes import useroutes
connect('UaaWebsitemain', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/UaaWebsitemain")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin(s)
    allow_credentials=True,                  # Allow cookies and credentials
    allow_methods=["*"],                     # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                     # Allow all headers
)


app.include_router(serviceroutes.router, tags=['service'])
app.include_router(blogroutes.router, tags=["Blog routes"])
app.include_router(useroutes.router, tags=["user routes"])