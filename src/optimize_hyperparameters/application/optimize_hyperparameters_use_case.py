from src.optimize_hyperparameters.domain.hyperparameter_optimizer import (
    IHyperparameterOptimizer)


def optimize_hyperparameters(hyperparameter_optimizer: IHyperparameterOptimizer):
    if isinstance(hyperparameter_optimizer, IHyperparameterOptimizer):
        hyperparameter_optimizer.optimize_hyperparameters()
