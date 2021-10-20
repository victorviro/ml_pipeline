from __future__ import annotations

import logging
from typing import Any, Dict

from src.shared.interfaces.data_tracker import IDataTracker
from src.shared.interfaces.model_register import IModelRegister, ModelStage
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

    def __init__(
        self,
        model_validator: IModelValidator,
        data_tracker: IDataTracker,
        model_register: IModelRegister,
        registry_model_name: str,
    ):
        self.model_validator = model_validator
        self.data_tracker = data_tracker
        self.model_register = model_register
        self.registry_model_name = registry_model_name

    def execute(self, metrics_threshold: Dict[str, Any]) -> None:
        metrics = self.data_tracker.get_information_logged_for_model_validation()
        if not metrics:
            msg = "There are no metrics tracked from the model evaluation."
            raise Exception(msg)
        model_validated = self.model_validator.validate_model(
            metrics=metrics, metrics_threshold=metrics_threshold
        )
        if not model_validated:
            raise Exception("Model was not validated succesfully.")
        # Update model's stage to 'Staging' in Model Registry
        stage = self.model_register.get_stage_from_enum(ModelStage.STAGING)
        self.model_register.transition_model_version_stage(
            name=self.registry_model_name, stage=stage
        )

    @staticmethod
    def build(
        model_validator: IModelValidator,
        data_tracker: IDataTracker,
        model_register: IModelRegister,
        registry_model_name: str,
    ) -> ValidateModel:
        validate_model = ValidateModel(
            model_validator=model_validator,
            data_tracker=data_tracker,
            model_register=model_register,
            registry_model_name=registry_model_name,
        )
        return validate_model
