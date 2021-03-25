from src.train_model.domain.model_trainer import IModelTrainer


def train_model(model_trainer: IModelTrainer):
    """
    This method train a model in some way by calling the method
    `train_model` of object IModelTrainer.

    :param model_trainer: Object with a method to train a model
    :type model_trainer: IModelTrainer
    """
    if isinstance(model_trainer, IModelTrainer):
        model_trainer.train_model()
