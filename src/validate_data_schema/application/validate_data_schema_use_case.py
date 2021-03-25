from src.validate_data_schema.domain.data_validator import IDataValidator


def validate_data_schema(data_validator: IDataValidator):
    """
    This method validate the data schema in some way calling the method
    `validate_data` of object IDataValidator

    :param data_validator: Object with a method to validate data
    :type data_validator: IDataValidator
    """
    if isinstance(data_validator, IDataValidator):
        data_validator.validate_data()
