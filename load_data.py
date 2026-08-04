import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

df = pd.read_excel("job_postings_template.xlsx", sheet_name="Job Postings")

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="job_market",
    user="postgres",
    password=db_password
)

print("Connected!")

unique_company_names=df['company'].unique()

cleaned_skills = df['skills'].str.split(',').explode().str.strip()
cleaned_skills=cleaned_skills.str.upper()
unique_skills=cleaned_skills.drop_duplicates().dropna().tolist()

print(unique_company_names)
print("***")
print(unique_skills)