import os
import sys
sys.path.append(os.getcwd())
import pandas as pd
from sqlalchemy import create_engine

def flat_dict_to_sql(dictionary: dict, db_name: str, table_name: str):
    engine = create_engine(f'sqlite:///{db_name}.db')
    df = pd.DataFrame(list(dictionary.items()), columns=['page_url', 'parent_url'])
    df.to_sql(table_name, con=engine.raw_connection(), if_exists='append')

def nested_dict_to_df(dictionary: dict, db_name: str, table_name: str):
    engine = create_engine(f'sqlite:///{db_name}.db')
    df = pd.DataFrame(dictionary)
    df.to_sql(table_name, con=engine.raw_connection(), if_exists='append')