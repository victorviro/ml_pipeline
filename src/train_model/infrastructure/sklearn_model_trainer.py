import logging

from pandas import DataFrame
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.shared.constants import TARGET_VARIABLE_NAME
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

    def __init__(
        self,
        size_test_split: float,
        test_split_seed: int,
        alpha: float,
        l1_ratio: float,
        model_seed: int,
    ):
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.model_seed = model_seed

    def train_model(self, dataset: dict, transformer: Pipeline) -> dict:
        """
        Train the model using Scikit-learn, and return information to track.

        :param dataset: The dataset used for training and evaluate the model
        :type dataset: dict
        :param transformer: The sklearn transformer pipeline fitted
        :type transformer: Pipeline
        :return: Information to track
        :rtype: dict
        """

        # Load the dataset to pandas DataFrame
        dataset_df = DataFrame.from_dict(dataset)
        features = dataset_df.drop(TARGET_VARIABLE_NAME, axis=1)
        target = dataset_df[TARGET_VARIABLE_NAME]

        # Split the dataset in training and test sets.
        try:
            x_train, _, y_train, _ = train_test_split(
                features,
                target,
                test_size=self.size_test_split,
                random_state=self.test_split_seed,
            )
        except ValueError as err:
            msg = "ValueError splitting the dataset into training and test sets."
            raise ValueError(msg) from err
        # Transform train features
        try:
            data_columns = features.columns.to_list()
            x_train_transformed_array = transformer.transform(x_train)
            x_train_transformed = DataFrame(
                x_train_transformed_array, columns=data_columns
            )
            logger.info("Training features transformed succesfully.")
        except Exception as err:
            msg = (
                "Error transforming training features. Error description: "
                f"{err.__class__.__name__}: {err}."
            )
        # Define and train the model
        try:
            # Define the model
            model = ElasticNet(
                alpha=self.alpha, l1_ratio=self.l1_ratio, random_state=self.model_seed
            )
            # Train the model
            model.fit(x_train_transformed, y_train)
            logger.info("Model trained succesfully")

            # Build the pipeline (transformations plus model)
            pipeline_steps = [*transformer.steps, *[("elastic_net", model)]]
            pipeline = Pipeline(steps=pipeline_steps)

            # Information to track (hyperparameters,...)
            parameters_to_track = {
                "alpha": self.alpha,
                "l1_ratio": self.l1_ratio,
                "test_split_seed": self.test_split_seed,
                "model_seed": self.model_seed,
                "test_split_percent": self.size_test_split,
            }
            information_to_track = {
                "parameters": parameters_to_track,
                "pipeline": pipeline,
            }
            return information_to_track

        except TypeError as err:
            msg = "TypeError training the model."
            logger.error(msg)
            raise Exception(msg) from err
        except ValueError as err:
            msg = "ValueError training the model."
            logger.error(msg)
            raise Exception(msg) from err
        except Exception as err:
            msg = "Unknown error training the model."
            logger.error(msg)
            raise Exception(msg) from err
