import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.model_evaluation import ModelEvaluation
from networksecurity.components.model_pusher import ModelPusher

from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig
   
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact,
    ModelPusherArtifact
)


class TrainingPipeline:
    
    def __init__(self):
           self.training_pipeline_config=TrainingPipelineConfig()
    def start_data_ingestion(self):
         try:
              self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
              logging.info("Starting data ingestion")
              data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
              data_ingestion_artifact=data_ingestion.intiate_data_ingestion()
              logging.info(f"Data ingestion completed and artifact:{data_ingestion_artifact}")
              return data_ingestion_artifact
         except Exception as e:
              raise NetworkSecurityException(e,sys)
           
    def start_data_validation(self,data_ingestion_artifact= DataIngestionArtifact):
         try:
             data_validation_config= DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
             data_validation=DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
             data_validation_artifact=data_validation.intiate_data_validation()
             return data_validation_artifact
         except Exception as e:
              raise NetworkSecurityException(e,sys)
            
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
         try:
               data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
               data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
               data_transformation_artifact= data_transformation.initiate_data_transformation()
               return  data_transformation_artifact
         except Exception as e:
              raise NetworkSecurityException(e,sys)
         
    def start_model_trainer(self,data_transformation_artifact: DataTransformationArtifact):
         try:
            self.model_trainer_config: ModelTrainerConfig = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact

         except Exception as e:
              raise NetworkSecurityException(e,sys)
            
    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,model_trainer_artifact:ModelTrainerArtifact):
         try:
                
              model_evaluation_config:ModelEvaluationConfig =ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
              model_eval=ModelEvaluation(model_evaluation_config,data_validation_artifact,model_trainer_artifact)
              model_eval_artifact=model_eval.initiate_model_evaluation()

              return model_eval_artifact

              
         except Exception as e:
              raise NetworkSecurityException(e,sys)
             
    def start_model_pusher(self,model_eval_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config, model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except  Exception as e:
            raise  NetworkSecurityException(e,sys)
         
    def run_pipeline(self):
         try:
              data_ingestion_artifact=self.start_data_ingestion()
              #print(data_ingestion_artifact)

              data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

              data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
          

              model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

              model_eval_artifact=self.start_model_evaluation(data_validation_artifact=data_validation_artifact,model_trainer_artifact=model_trainer_artifact)
              if not model_eval_artifact.is_model_accepted:
                #raise Exception("Trained model is not better than the best model")
                print("Trained model is not better than the best model")

              
              model_pusher_artifact = self.start_model_pusher(model_eval_artifact)

         except Exception as e:
              raise NetworkSecurityException(e,sys)
          