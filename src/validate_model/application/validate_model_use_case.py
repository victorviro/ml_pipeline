from src.validate_model.domain.model_validator import IModelValidator


def validate_model(model_validator: IModelValidator):
    if isinstance(model_validator, IModelValidator):
        model_validator.validate_model()
