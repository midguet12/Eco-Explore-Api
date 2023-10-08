FROM python:3.11-slim 
COPY ./src /app 
RUN pip install "poetry" 

WORKDIR /app 
RUN touch /README.md
RUN poetry install
EXPOSE 8000
CMD [ "poetry", "run", "uvicorn", "--host=0.0.0.0", "--port", "8000", "eco_explore_api.routes:app" ]