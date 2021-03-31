import abc


class ITransformationFitter(metaclass=abc.ABCMeta):
    """
    An interface used to fit a transformer/preprocessing.
    """

    @abc.abstractmethod
    def fit_transformer(self):
        """
        This method must fit a transformation/preproessing in some way
        """
