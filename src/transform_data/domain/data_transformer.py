import abc


class IDataTransformer(metaclass=abc.ABCMeta):
    """
    An interface used to transform/preprocess data.
    """

    @abc.abstractmethod
    def transform_data(self):
        """
        This method must transform the data in some way
        """
