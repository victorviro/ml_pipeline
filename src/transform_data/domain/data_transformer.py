import abc


class IDataTransformer(metaclass=abc.ABCMeta):
    """
    An interface used to transform/preprocess data.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'transform_data') and
                callable(subclass.transform_data))

    @abc.abstractmethod
    def transform_data(self):
        """
        This method must transform the data in some way
        """
