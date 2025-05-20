# API for detecting toxicity in Romanian Language. 
For frontend go to [here](https://github.com/eduard-negescu/toxicity-detection-react)
API written in python and FastApi to serve an NLP model. 
The model is based on a BeRT model and was fitted with the readerbench/ro-offense dataset.
The model is not included in the repo due to size constraints, without it the programme won't work. 

# Technologies used
python, huggingface transformers, fastapi, jwt (for authentication), postgresql, sqlalchemy (ORM), alembic (for migrations), transformers, pytorch, sqladmin (for admin dashboard), pydantic

# Installation
* Create .env with the following variables, DB_URL for the url of a postgres db and SECRET_KEY for encryption.
* pip install -r requirements.txt
* "alembic upgrade head" to apply the db migrations.
* "uvicorn app.main:app" to run the programme.