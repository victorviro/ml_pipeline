import logging

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.pipeline import Pipeline

from src.train_model.domain.model_trainer import IModelTrainer


logger = logging.getLogger(__name__)


class SklearnModelTrainer(IModelTrainer):
    """
    A class which implements the interface IModelTrainer to train a model.
    It trains the model using Scikit-learn.

    :param size_test_split: Percentage of test dataset when splitting the dataset
    :type size_test_split: float
    :param test_split_seed: Seed used when splitting the dataset
    :type test_split_seed: int
    :param alpha: Alpha hyperparameter of the elasticnet model
    :type alpha: float
    :param l1_ratio: L1 ratio hyperparameter of the elasticnet model
    :type l1_ratio: float
    :param model_seed: Seed used when training the model
    :type model_seed: int
    """

    def __init__(self, size_test_split: float,
                 test_split_seed: int, alpha: float, l1_ratio: float, model_seed: int):
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.model_seed = model_seed

    def train_model(self, data: dict, transformer: Pipeline) -> dict:
        """
        Train the model using Scikit-learn, and return information to track.

        :param data: The dataset used for training and evaluate the model
        :type data: dict
        :param transformer: The sklearn transformer pipeline fitted
        :type transformer: Pipeline
        :return: Information to track
        :rtype: dict
        """

        # Convert the dataset to pandas DataFrame
        try:
            data_df = DataFrame.from_dict(data)
            logger.info(f'Dataset converted to pandas DataFrame succesfully.')
        except Exception as err:
            msg = f'Error converting the dataset to df. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
        # Split the data into training and test sets.
        try:
            X = data_df.drop("max_char_per_line", axis=1)
            y = data_df["max_char_per_line"]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.size_test_split, random_state=self.test_split_seed
            )
        except Exception as err:
            msg = f'Error getting target variable or splitting the dataset. Error: {err}'
            logger.error(msg)
            raise Exception(msg)

        try:
            # Transform train features
            data_columns = X.columns.to_list()
            X_train_transformed_array = transformer.transform(X_train)
            X_train_transformed = DataFrame(X_train_transformed_array,
                                            columns=data_columns)
            logger.info('Training features transformed succesfully')

            # Define the model
            model = ElasticNet(
                alpha=self.alpha,
                l1_ratio=self.l1_ratio,
                random_state=self.model_seed
            )
            # Train the model
            model.fit(X_train_transformed, y_train)
            logger.info(f'Model trained succesfully. Hyperparameters: '
                        f'alpha={self.alpha}, l1_ratio={self.l1_ratio}.')

            # Build the pipeline (transformations plus model)
            steps_pipe = transformer.steps
            steps_pipe.append(('elastic_net', model))
            pipeline = Pipeline(steps=steps_pipe)

            # Information to track (hyperparameters,...)
            parameters_to_track = {
                "alpha": self.alpha,
                "l1_ratio": self.l1_ratio,
                "test_split_seed": self.test_split_seed,
                "model_seed": self.model_seed,
                "test_split_percent": self.size_test_split
            }
            information_to_track = {
                "parameters": parameters_to_track,
                "pipeline": pipeline
            }
            return information_to_track

        except Exception as err:
            msg = f'Error training the model. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
