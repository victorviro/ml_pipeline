import abc


class IModelServer(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'serve_predictions') and
                callable(subclass.serve_predictions))

    @abc.abstractmethod
    def serve_predictions(self):
        """
        This method must serve serve predictions
        """
