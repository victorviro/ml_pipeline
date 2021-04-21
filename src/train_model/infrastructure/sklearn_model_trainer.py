import logging

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.pipeline import Pipeline

from src.train_model.domain.model_trainer import IModelTrainer
from src.shared.training_helper import get_regression_metrics


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

    def transform_features(self, features: DataFrame, data_columns: list,
                           transformer: Pipeline) -> DataFrame:
        """
        Transform/Preprocess the features.

        :param features: The features to be transformed
        :type features: DataFrame
        :param data_columns: The column names of the data transformed
        :type data_columns: list
        :param transformer: The sklearn transformer pipeline fitted
        :type transformer: Pipeline
        :return: The features transformed
        :rtype: DataFrame
        """

        try:
            features_transformed_array = transformer.transform(features)
            features_transformed = DataFrame(features_transformed_array,
                                             columns=data_columns)

            return features_transformed
        except Exception as err:
            msg = f'Error transforming train or test features. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

    def train_model(self, data: dict, transformer: Pipeline) -> dict:
        """
        Train the model using Scikit-learn, and return information to track.

        :param data: The dataset used for training and evaluate the model
        :type data: dict
        :param transformer: The sklearn transformer pipeline fitted
        :type transformer: Pipeline
        :return: Information to track
        :rtype: Dict
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
            data_columns.append('ratio_cols_rows')
            X_train_transformed = self.transform_features(
                features=X_train,
                data_columns=data_columns,
                transformer=transformer
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
                data_columns=data_columns,
                transformer=transformer
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

            # Information to track (hyperparameters, metrics...)
            parameters_to_track = {
                "alpha": self.alpha,
                "l1_ratio": self.l1_ratio,
                "test_split_seed": self.test_split_seed,
                "model_seed": self.model_seed,
                "test_split_percent": self.size_test_split
            }
            metrics_to_track = {
                "rmse_train": rmse_train,
                "r2_train": r2_train,
                "mae_train": mae_train,
                "rmse_test": rmse_test,
                "r2_test": r2_test,
                "mae_test": mae_test
            }
            information_to_track = {
                "parameters": parameters_to_track,
                "metrics": metrics_to_track,
                "model": model
            }
            return information_to_track

        except Exception as err:
            msg = f'Error training the model. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
