👣 Machine learning pipeline
==============================


This project aims to **automate** the ML pipeline to train a 📈 regression model.

📝 Notes:

- Each step/component of the pipeline is 🐳 **containerized** since each one has its own 📦 packages. It also makes the code *reproducible* between development and production environments.

- The code for each 👣 step is separated from the pipeline, which is **orchestrated** with Airflow (the pipeline is defined as a [Directed Acyclic Graph](https://airflow.apache.org/docs/apache-airflow/1.10.12/concepts.html#dags) in `src/airflow_dags`).


![](https://i.ibb.co/9s82GHB/aaa.png)


# 💻 Set up

- 🐱 Get the repository

  `git clone git@github.com:victorviro/ml_pipeline.git`

- 🏢 Build and up the project

  `make init-airflow`

  `make buildup`

- 🔛 Enable pre-commit hooks

  `pre-commit install`

# 🐞 Debugging

- 🏗️ Create virtual environment (e.g. with virtualenv)
  
  ```
  python3 -m virtualenv venv
  source venv/bin/activate
  ```

- 📥 Install the dependencies

  `make install`

# Development process

- ✔️ Test

  `make test`

- ⚠️ Lint

  `make lint`

- 🌟 Format

  `make format`