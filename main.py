import os
import sys

from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
from networksecurity.pipeline.training_pipeline import TrainingPipeline

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)

AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

os.environ["AWS_ACCESS_KEY_ID"]=AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"]=AWS_SECRET_ACCESS_KEY

import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

client=pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)


database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]


app=FastAPI()
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
    return RedirectResponse(url="/docs")


# here we will train the model and it's a training route
@app.get("/train")
async def train_route():
    try:
            
            training_pipleline=TrainingPipeline()
            if training_pipleline.is_pipeline_running:
                  return Response("Training pipeline is already running")
            training_pipleline.run_pipeline()
            return Response("Training successful")
    except Exception as e:
              raise NetworkSecurityException(e,sys)
    
"""
#this is a prediction route
@app.get("/predict")
async def predict_route(request:Request,file: UploadFile = File(...)):
    try:
        pass
    except Exception as e:
              raise NetworkSecurityException(e,sys)
    

def main():
      try:
            
            training_pipleline=TrainingPipeline()
            training_pipleline.run_pipeline()
      except Exception as e:
              raise NetworkSecurityException(e,sys)
"""   
#Start the server of fast FastAPI
if __name__=="__main__":
      app_run(app,host="localhost", port=8000)


