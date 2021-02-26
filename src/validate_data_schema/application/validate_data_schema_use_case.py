from src.validate_data_schema.domain.data_validator import IDataValidator


def validate_schema(data_validator: IDataValidator):
    if isinstance(data_validator, IDataValidator):
        data_validator.validate_data()
