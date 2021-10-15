import logging

from src.shared.interfaces.data_tracker import IDataTracker
from src.validate_model.domain.model_validator import IModelValidator

logger = logging.getLogger(__name__)


class ValidateModel:
    """
    Class to validate a model. It updates its stage in Model Registry if
    its validation succeds.

    :param model_validator: Object with a method to validate a model
    :type model_validator: IModelValidator
    :param data_tracker: Object with methods to track information
    :type data_tracker: IDataTracker
    """

    def __init__(self, model_validator: IModelValidator, data_tracker: IDataTracker):
        self.model_validator = model_validator
        self.data_tracker = data_tracker

    def execute(self, metrics_threshold: dict):
        metrics = self.data_tracker.get_metrics()
        if not metrics:
            msg = "There are no metrics tracked from the model evaluation."
            raise Exception(msg)
        model_validated = self.model_validator.validate_model(
            metrics=metrics, metrics_threshold=metrics_threshold
        )
        if not model_validated:
            raise Exception("Model was not validated succesfully.")
        # Update model's stage in Model Registry
        self.data_tracker.update_validated_model_in_registry()

    @staticmethod
    def build(model_validator: IModelValidator, data_tracker: IDataTracker):
        validate_model = ValidateModel(
            model_validator=model_validator, data_tracker=data_tracker
        )
        return validate_model
