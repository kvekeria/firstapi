#!/usr/bin/env python

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from .routers import post, user, auth, voting
from .database import engine
from .config import settings

app = FastAPI()

@app.get('/')
def home():
    return {'welcome to' : 'firstapi'}


origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(voting.router)
