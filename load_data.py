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

skill_corrections = {
    'JAVASRCIPT': 'JAVASCRIPT',
    'DATA MODELIING': 'DATA MODELING',
    'RESTFUL APIS': 'REST API',
}
cleaned_skills = cleaned_skills.replace(skill_corrections)

unique_skills=cleaned_skills.drop_duplicates().dropna().tolist()

#print(unique_company_names)
#print("***")
#print(unique_skills)

cur = conn.cursor()

for company in unique_company_names:
    cur.execute(
        "INSERT INTO companies (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (company,)
    )

for skills in unique_skills:
    cur.execute(
        "INSERT INTO skills (skill_name) VALUES (%s) ON CONFLICT (skill_name) DO NOTHING",
        (skills,)
    )

cur.execute("SELECT company_id, name FROM companies")
company_map = {name: cid for cid, name in cur.fetchall()}

job_ids = []

cur.execute("SELECT skill_id, skill_name FROM skills")
skill_map = {name: sid for sid, name in cur.fetchall()}

for i, row in df.iterrows():
    date_posted = row['date_posted'] if pd.notna(row['date_posted']) else None
    
    cur.execute("""
        INSERT INTO jobs (title, company_id, city, work_model, seniority, source, date_posted, link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING job_id
    """, (
        row['title'],
        company_map[row['company']],
        row['city'],
        row['work_model'],
        row['seniority'],
        row['source'],
        date_posted,
        row['link']
    ))
    job_id = cur.fetchone()[0]
    job_ids.append(job_id)
    
    if pd.notna(row['salary_min_uop']) or pd.notna(row['salary_max_uop']):
        cur.execute("""
            INSERT INTO contracts (job_id, contract_type, salary_min, salary_max)
            VALUES (%s, %s, %s, %s)
        """, (
            job_id,
            'uop',
            row['salary_min_uop'] if pd.notna(row['salary_min_uop']) else None,
            row['salary_max_uop'] if pd.notna(row['salary_max_uop']) else None
        ))

    if pd.notna(row['salary_min_b2b']) or pd.notna(row['salary_max_b2b']):
        cur.execute("""
            INSERT INTO contracts (job_id, contract_type, salary_min, salary_max)
            VALUES (%s, %s, %s, %s)
        """, (
            job_id,
            'b2b',
            row['salary_min_b2b'] if pd.notna(row['salary_min_b2b']) else None,
            row['salary_max_b2b'] if pd.notna(row['salary_max_b2b']) else None
        ))

    job_skill_list = [s.strip().upper() for s in row['skills'].split(',')]
    for skill_name in job_skill_list:
        skill_name = skill_corrections.get(skill_name, skill_name)
        skill_id = skill_map[skill_name]
        cur.execute("""
            INSERT INTO job_skills (job_id, skill_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (job_id, skill_id))

conn.commit()