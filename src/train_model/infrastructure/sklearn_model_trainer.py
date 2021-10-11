import logging

from pandas import DataFrame
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.shared.constants import TARGET_VARIABLE_NAME
from src.train_model.domain.model_trainer import IModelTrainer

logger = logging.getLogger(__name__)


class SklearnModelTrainer(IModelTrainer):
    def __init__(
        self,
        size_test_split: float,
        test_split_seed: int,
        alpha: float,
        l1_ratio: float,
        model_seed: int,
    ):
        """
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
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.model_seed = model_seed

    def train_model(self, dataset: dict, preprocesser: Pipeline) -> dict:

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
        # Preprocess the train features
        try:
            data_columns = features.columns.to_list()
            x_train_preprocessed_array = preprocesser.transform(x_train)
            x_train_preprocessed = DataFrame(
                x_train_preprocessed_array, columns=data_columns
            )
            logger.info("Training features preprocessed succesfully.")
        except Exception as err:
            msg = "Error preprocessing training features."
            raise Exception(msg) from err
        # Define and train the model
        try:
            # Define the model
            model = ElasticNet(
                alpha=self.alpha, l1_ratio=self.l1_ratio, random_state=self.model_seed
            )
            # Train the model
            model.fit(x_train_preprocessed, y_train)
            logger.info("Model trained succesfully")

            # Build the pipeline (preprocessing plus model)
            pipeline_steps = [*preprocesser.steps, *[("elastic_net", model)]]
            pipeline = Pipeline(steps=pipeline_steps)

            # Metadata to track (hyperparameters,...)
            parameters_to_track = {
                "alpha": self.alpha,
                "l1_ratio": self.l1_ratio,
                "test_split_seed": self.test_split_seed,
                "model_seed": self.model_seed,
                "test_split_percent": self.size_test_split,
            }
            metadata_to_track = {
                "parameters": parameters_to_track,
                "pipeline": pipeline,
            }
            return metadata_to_track

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
