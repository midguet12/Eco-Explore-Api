# Eco-Explore-Api
Eco Explore Api an exploration and travel Service 


# Installation

You need install all requeriments for develop the api
### Requeriments 
- Python >= 3.11 
- Poetry 

then copy the application.ini from the build.config folder into your `src` folder, and add all keys for develop.

After that can install al dependencies of the api

Change your current path to the `src` dir and Install depencencies using poetry 

```bash
poetry install 
```

# How to Run in Development Mode


1. Enter to the poetry shell for containerized enviroment 
```bash 
poetry shell 
```

2. Run the project using `uvicorn` this command will launch uvicorn inside poetry environment, this project already have Swagger installed for apy test, dont need another tool for test the API 

```bash 
poetry run uvicorn eco-explore-api.routes:app --reload
```


