from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import wave
import os
import pylab
import uuid
from io import BytesIO
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, Form, UploadFile

from db_functions import register_user, login_user, create_test, get_home_info, get_history, poppy, let_me

class RegisterUser(BaseModel):
    uuid: str
    password: str
    age: int

class User(BaseModel):
    uuid: str
    password: str

class Password(BaseModel):
    password: str


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
        return {"message": "Nothing Wrong Here!!"}

@app.post("/register")
async def register(user:RegisterUser):
        return register_user(user)


@app.post("/login")
async def login(user: User):
        return login_user(user)

@app.post("/verify")
async def analyze_audio(file: UploadFile = File(...), token: str = Form(...)):
        wav_f = file.file
        sound_info, frame_rate = get_wav_info(wav_f)
        pylab.figure(num=None, figsize=(19, 12))
        pylab.subplot(111)
        pylab.specgram(sound_info, Fs=frame_rate)
        filename = str(uuid.uuid4())
        pylab.savefig('tmp/'+filename+".png")
        path = 'tmp/'+filename+".png"
        with open(path, "rb") as image:
            f = image.read()
            b = bytearray(f)
            url = 'https://koff-fastai.ratemycourse.review/classify-url' 
            r = requests.post(url, b)
            print(r.json()["predictions"][0])
            preds = {
                    "verdict": r.json()["predictions"][0][0],
                    "specs":{
                            "ill": r.json()["predictions"][0][1],
                            "not-ill": r.json()["predictions"][1][1]
                    }
            }
            print(create_test(preds, token))
            return {"message":"success", "pred": preds, "blockchain":"fail"}


@app.get("/home/{token}")
async def get_home_data(token: str):
        return get_home_info(token)


@app.get("/history/{token}")
async def get_hist(token: str):
        return get_history(token)


@app.get("/add-to-queue/{token}")
async def add_to_queue(token: str):
        return add_queue(token)

#-------------------------------------------------------------------------------------------
#web-app
@app.post("/let-me-in")
async def let_me_in(password: Password):
        return let_me(password.password)

@app.get("/scan")
async def scannnig():
        return scan_db()

@app.get("/pop-it")
async def pop_it_now():
        return poppy()


#-------------------------------------------------------------------------------------------
#helpers

def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate