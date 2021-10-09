import logging

from src.shared.interfaces.data_tracker import IDataTracker

logger = logging.getLogger(__name__)


class ValidateModel:
    """
    Class to validate the model in some way by calling its method
    `validate_model`. It updates its stage in Model Registry if its validation succeds
    by calling a method of the IDataTracker object.

    :param data_tracker: Object with methods to track information
    :type data_tracker: IDataTracker
    """

    def __init__(self, data_tracker: IDataTracker):
        self.data_tracker = data_tracker

    def execute(self, metrics_threshold: dict):
        metrics = self.data_tracker.get_metrics()
        if not metrics:
            msg = "There are no metrics tracked from the model evaluation."
            raise Exception(msg)
        # Validate the model
        model_validated = self.validate_model_performance(
            metrics=metrics, metrics_threshold=metrics_threshold
        )
        if not model_validated:
            raise Exception(
                "Model was not validated succesfully. Model performance is "
                "not enough."
            )
        # Update model's stage in Model Registry
        self.data_tracker.update_validated_model_in_registry()

    @staticmethod
    def build(data_tracker: IDataTracker):
        validate_model = ValidateModel(data_tracker=data_tracker)
        return validate_model

    @staticmethod
    def validate_model_performance(metrics: dict, metrics_threshold: dict) -> bool:
        """
        Validated the model based on its performance metrics in the test set and
        threshold values.

        :param metrics: Metrics of the model's performance in the test set
        :type metrics: dict
        :param metrics_threshold: Threshold values of the metrics
        :type metrics_threshold: dict
        :return: If the model is validated
        :rtype: bool
        """
        rmse, rmse_threshold = metrics["rmse_test"], metrics_threshold["rmse"]
        if rmse > rmse_threshold:
            msg = (
                "Square root of mean squared error bigger that the thresold fixed:"
                f" {rmse} > thresold fixed = {rmse_threshold}"
            )
            logger.warning(f"Model was not validated succesfully: {msg}.")
            return False

        msg = (
            "Square root of mean squared error smaller that the threshold "
            f"fixed: {rmse} < thresold fixed = {rmse_threshold}."
        )
        logger.info(f"Model validated succesfully in test set: {msg}")
        return True
