import logging
from requests import post
from json import loads, dumps

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

from src.shared.constants import REGISTRY_MODEL_NAME, URL_TRANSFORM_DATA_API
from src.train_model.domain.model_trainer import IModelTrainer
from src.shared.interfaces.data_tracker import IDataTracker
from src.shared.training_helper import get_regression_metrics


logger = logging.getLogger(__name__)


class MlflowSklearnTrainer(IModelTrainer):
    """
    A class which implements the interface IModelTrainer to train a model.
    It trains the model using Scikit-learn, track the experiment in MLFlow, and
    register the model trained in MLFlow model registry.

    :param transformer_name: Name of the transformer pipeline stored
    :type transformer_name: str
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
    :param model_name: Name of the model used to track the experiment in MLFlow
    :type model_name: str
    """

    def __init__(self, transformer_name: str, size_test_split: float,
                 test_split_seed: int, alpha: float, l1_ratio: float, model_seed: int,
                 model_name: str):
        self.transformer_name = transformer_name
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.model_seed = model_seed
        self.model_name = model_name

    def transform_features(self, features: DataFrame,
                           transformer_pipe_path: str) -> DataFrame:
        """
        Transform/Preprocess the features through a request by calling the
        transform data API.

        :param features: The features to be transformed
        :type features: DataFrame
        :param transformer_pipe_path: The path where the sk transformer pipe is stored
        :type transformer_pipe_path: str
        :return: The features transformed
        :rtype: DataFrame
        """
        body = {
                "transformer_pipe_path": transformer_pipe_path,
                "pipe_name": self.transformer_name,
                "data": features.to_dict(orient='list')
        }
        try:
            request = post(URL_TRANSFORM_DATA_API, data=dumps(body))
            content = loads(request.content.decode('utf-8'))
            features_transformed = DataFrame(content["data"])
            return features_transformed
        except Exception as err:
            msg = f'Error transforming train or test features. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

    def train_model(self, data: dict, data_tracker: IDataTracker):
        """
        Train the model using Scikit-learn, track the experiment in MLFlow, and
        register the model trained in MLFlow model registry.

        :param data: The dataset used for training and evaluate the model
        :type data: dict
        :param data_tracker: A data tracker to track info of the experiment
        :type data_tracker: IDataTracker
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
            # Get the artifacts path of the MLflow experiment run
            tracked_artifacts_path = data_tracker.get_artifacts_path(
                model_name=self.model_name
            )
            # Transform train features
            X_train_transformed = self.transform_features(
                features=X_train,
                transformer_pipe_path=tracked_artifacts_path
            )
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

            # Predictions in the test and training sets
            y_train_predicted = model.predict(X_train_transformed)
            X_test_transformed = self.transform_features(
                features=X_test,
                transformer_pipe_path=tracked_artifacts_path
            )
            y_test_predicted = model.predict(X_test_transformed)

            # Compute metrics in the test and training sets
            (rmse_test, mae_test, r2_test) = get_regression_metrics(y_test,
                                                                    y_test_predicted)
            (rmse_train, mae_train, r2_train) = get_regression_metrics(
                y_train, y_train_predicted
            )

            logger.info(f'Metrics train set: \nRMSE: {rmse_train} \nMAE: {mae_train}'
                        f' \nR2: {r2_train}')
            logger.info(f'Metrics test set: \nRMSE: {rmse_test} \nMAE: {mae_test}'
                        f' \nR2: {r2_test}')

            # Track information (hyperparameters, metrics...)
            data_tracker.track_parameters({
                "alpha": self.alpha,
                "l1_ratio": self.l1_ratio,
                "test_split_seed": self.test_split_seed,
                "model_seed": self.model_seed,
                "test_split_percent": self.size_test_split
            })
            data_tracker.track_metrics({
                "rmse_train": rmse_train,
                "r2_train": r2_train,
                "mae_train": mae_train,
                "rmse_test": rmse_test,
                "r2_test": r2_test,
                "mae_test": mae_test
            })

            # Track the model in the experiment run
            data_tracker.track_sklearn_model(
                model=model,
                model_name=self.model_name
            )
            logger.info('Model tracked in the experiment succesfully')

            # Register the model in model registry (staged as None)
            data_tracker.register_model(
                model_name=self.model_name,
                name=REGISTRY_MODEL_NAME
            )
        except Exception as err:
            msg = f'Error training the model. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
