import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

df = pd.read_excel("job_postings_template.xlsx", sheet_name="Job Postings")
print(df.head())
print(df.columns)

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="job_market",
    user="postgres",
    password=db_password
)