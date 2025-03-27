# 👣 Machine learning pipeline

This project aims to **automate** the ML pipeline to train a 📈 regression model.

📝 Notes:

- Each step/component of the pipeline is 🐳 **containerized** since each one has its own 📦 packages. It also makes the code _reproducible_ between development and production environments.

- The code for each 👣 step is separated from the pipeline, which is **orchestrated** with Airflow (the pipeline is defined as a [Directed Acyclic Graph](https://airflow.apache.org/docs/apache-airflow/1.10.12/concepts.html#dags) in `src/airflow_dags`).

![](https://i.ibb.co/9s82GHB/aaa.png)

# 💻 Set up

🐱 Get the repository

```bash
git clone git@github.com:victorviro/ml_pipeline.git
```

🏢 Build and up the project

```bash
make init-airflow
make buildup
```

🔛 Enable pre-commit hooks

```bash
pre-commit install
```

# 🐞 Debugging

🏗️ Create virtual environment (e.g. with virtualenv)

```bash
python3.12 -m venv venv
source venv/bin/activate
```

📥 Install the dependencies

```bash
make install
```

# Development process

✔️ Test

```bash
make test
```

⚠️ Lint

```bash
make lint
```

🌟 Format

```bash
make format
```
