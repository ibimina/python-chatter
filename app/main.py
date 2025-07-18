from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models

from .routers import user, auth, article, topic, bookmark, follow, message


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(article.router)
app.include_router(topic.router)
app.include_router(bookmark.router)
app.include_router(follow.router)
app.include_router(message.router)



@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}