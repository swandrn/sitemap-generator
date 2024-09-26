import os
import sys
sys.path.append(os.getcwd())
from sqlalchemy import create_engine
from utilities import env

engine = create_engine(f'postgresql+psycopg2://{env.DB_USER}:{env.DB_PWD}@{env.DB_HOST}/{env.DB_NAME}')