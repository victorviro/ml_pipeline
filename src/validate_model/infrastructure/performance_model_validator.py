import logging

from src.validate_model.domain.model_validator import IModelValidator

logger = logging.getLogger(__name__)


class PerformanceModelValidator(IModelValidator):
    @staticmethod
    def validate_model(metrics: dict, metrics_threshold: dict) -> bool:
        """
        Validate the model based on its performance metrics in the test set and
        threshold values.
        """

        logger.info("Validating model...")
        rmse, rmse_threshold = metrics["rmse_test"], metrics_threshold["rmse"]
        if rmse > rmse_threshold:
            msg = (
                "Square root of mean squared error bigger that the thresold fixed:"
                f" RMSE in test set = {rmse} > thresold fixed = {rmse_threshold}"
            )
            logger.warning(f"Model was not validated succesfully: {msg}.")
            return False

        msg = (
            "Square root of mean squared error smaller that the threshold "
            f"fixed: {rmse} < thresold fixed = {rmse_threshold}."
        )
        logger.info(f"Model validated succesfully in test set: {msg}")
        return True
