from src.validate_model.domain.model_validator import IModelValidator


def validate_model(model_validator: IModelValidator):
    """
    This method validates a model in some way by calling the method
    `validate_model` of object IModelValidator.

    :param model_validator: Object with a method to validate a model
    :type model_validator: IModelValidator
    """
    if isinstance(model_validator, IModelValidator):
        model_validator.validate_model()
