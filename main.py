import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponses
import pandas as pd


def  set_env_variable(env_file_path):
    pass

app=FASTAPI()
origins=["*"]

#for cross locations connections
app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

#for authentications

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponses(url="/docs")


# here we will train the model and it's a training route
@app.get("/train")
async def train_route():
    try:
        pass
    except Exception as e:
              raise NetworkSecurityException(e,sys)
    

#this is a prediction route
@app.get("/predict")
async def predict_route(request:Request,file: UploadFile = File(...)):
    try:
        pass
    except Exception as e:
              raise NetworkSecurityException(e,sys)
    

def main():
      try:
            set_env_variable(env_file_path)
            training_pipleline=TrainPipeline()
            training_pipleline.run_pipeline()
      except Exception as e:
              raise NetworkSecurityException(e,sys)
    
#Start the server of fast FastAPI
if __name__=="__main__":
      app_run(app,host=APP_HOST, port=APP_PORT)


