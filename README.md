Max char per line prediction
==============================

## Description

This project aims to automate the **ML pipeline** to train a model for predicting the maximum number of characters per line.

- Data ingestion
- Data validation
- Data versioning
- Data preprocessing/transformation
- Model training
- Model evaluation/validation
- Model versioning
- Model deployment

![](https://i.ibb.co/YL3s7T8/ml-model-lifecycle.png)

Considerations:

- This project also aims to define a *template* for future projects. A more detailed description of the problem this project solves and the data used, is available in the documentation.
- Each step/component of the pipeline is **containerized** since each one has their own packages. Moreover, it makes code *reproducible* between development and production environments.
- An api is created for each component in order to **separate the code from the pipeline**, which is **orchestraded** with Airflow (the pipeline is defined as a DAG in `src/airflow_dags`).
- A detailed description of each step is available in the documentation.
