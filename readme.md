# Wedding Backend FastAPI app

This project was created for weddinginvitation frontend app.

Tech stacks: Render container (previously Heroku container), Python FastAPI, Render PostgreSQL

![Tech stacks](https://skillicons.dev/icons?i=fastapi,python,docker,ubuntu,bash,heroku,vercel,postgres,anaconda)

## Local Development

### Run command

```
uvicorn wedding_app.main:app --reload
```

### Docker container

If you are Docker euthanist, have Docker Desktop on your end:
```
docker-compose up --build
```

Runs the app in the development mode.\
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### To install all dependencies from `requirements.txt`
Make sure you have Python environment or Anaconda available
```
pip install -r requirements.txt
```

### To import environment from `environment.yml`
```
conda env create -f environment.yml
```

### Seeing "Oh no! 💥 💔 💥, 2 files would be reformatted"
We should fix the formatting issues that might caused pipeline blocks
```
black .
```

### Staging environment (Heroku, Render...)
This is to setup heroku container for staging uses
```
heroku login
heroku stack:set container -a weddingbackend
```

### Storing your postgresql password and secretkey
For staging environment like Heroku:
```
heroku config:set SQLALCHEMY_DATABASE_URL="postgresql://{user}:pw@{hostname}.{yourhostingwebsite}.com/wedding_db_lgif" -a weddingbackend
heroku config:set SECRETKEY=xxxx -a weddingbackend
```
Local:
```.env
SQLALCHEMY_DATABASE_URL=postgresql://
SECRETKEY=xxxx
USER=xx
PASSWORD=xxx
```

You can store the env variable somewhere using .env or setting this inside your heroku container so it don't get exposed. 
For Render just find `Environment Variable` and key in manually.
