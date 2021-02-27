from src.train_model.domain.model_trainer import IModelTrainer


def train_model(model_trainer: IModelTrainer):
    if isinstance(model_trainer, IModelTrainer):
        artifact_uri = model_trainer.train_model()
        return artifact_uri
