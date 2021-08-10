ML pipeline
==============================

## Description

This project aims to automate the **ML pipeline** to train a regression model. A more detailed description of the problem this project solves and the data used is available in the documentation.

Notes:

- Each step/component of the pipeline is **containerized** since each one has its own packages. It also makes the code *reproducible* between development and production environments.

- The code for each step is separated from the pipeline, which is **orchestraded** with Airflow (the pipeline is defined as a DAG in `src/airflow_dags`).





![](https://i.ibb.co/9s82GHB/aaa.png)

