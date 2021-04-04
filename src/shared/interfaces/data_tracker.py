import abc


class IDataTracker(metaclass=abc.ABCMeta):
    """
    An interface used to track data in an experiment.
    """

    @abc.abstractmethod
    def track_data(self):
        """
        This method must track data to an experiment
        """
        return NotImplementedError
