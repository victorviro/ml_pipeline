import abc


class IDataTransformer(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'transform_data') and
                callable(subclass.transform_data))

    @abc.abstractmethod
    def transform_data(self):
        """
        This method must transform the data in some way
        """
