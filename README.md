Deploying a Scalable ML Pipeline in Production
================


This project is part of the [ML DevOps Engineer Nanodegree](https://www.udacity.com/course/machine-learning-dev-ops-engineer-nanodegree--nd0821)
 program, from Udacity. I developed a classification model on publicly available
 Census Bureau data. There are unit tests to monitor the model performance on
 various data slices.

I deployed the model using the FastAPI package, and some API tests were also
 implemented. The slice-validation and the API tests were incorporated into
 a CI/CD framework using GitHub Actions.


### Install
To set up your environment to run the codes in this repository, start by setting
 up the Github CLI, and the Heroku CLI in your machine:

```bash
> conda create -n [envname] "python=3.8" scikit-learn boto3 pandas numpy rich dvc -c conda-forge
> heroku login
```

Then, install Docker in your machine, start the Docker Desktop App and run:

```bash
> make docker-build
```


### Run
In a terminal or command window, navigate to the top-level project directory
 `mlops-on-heroku-fastapi/` (that contains this README) and run the
 following command:

```bash
> make live-post
```


### License
The contents of this repository are covered under the [MIT License](LICENSE).