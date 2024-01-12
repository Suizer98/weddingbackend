# Getting Started with FastAPI App

This project was created for weddinginvitation frontend app.

## Available Scripts

In the project directory, you can run:

### `uvicorn sql_app.main:app --reload`

Runs the app in the development mode.\
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `pip install -r requirements.txt`

To install all dependencies from `requirements.txt`

### `conda env create -f environment.yml`

To import environment from `environment.yml`

### `black .`

This to fix the formatting issues that might caused pipeline blocks

### `heroku stack:set container -a weddingbackend`

This is to setup heroku container for staging uses

### `Storing your postgresql password and secretkey`

```
heroku config:set SQLALCHEMY_DATABASE_URL="postgresql://{user}:pw@{hostname}.{yourhostingwebsite}.com/wedding_db_lgif" -a weddingbackend
heroku config:set SECRETKEY=xxxx -a weddingbackend
```
```.env
SQLALCHEMY_DATABASE_URL=postgresql://
SECRETKEY=xxxx
```

You can store the env variable somewhere using .env or setting this inside your heroku container so it don't get exposed