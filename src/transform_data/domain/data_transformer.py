import abc


class IDataTransformer(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = self.get_data()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'transform_data') and
                callable(subclass.transform_data))

    @abc.abstractmethod
    def transform_data(self):
        """
        This method must transform the data in some way
        """
