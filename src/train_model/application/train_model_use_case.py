from src.train_model.domain.model_trainer import IModelTrainer


def train_model(model_trainer: IModelTrainer):
    if isinstance(model_trainer, IModelTrainer):
        model_trainer.train_model()
