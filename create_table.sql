CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE jobs (
    job_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    company_id INTEGER REFERENCES companies(company_id),
    city TEXT,
    work_model TEXT,
    seniority TEXT,
    source TEXT,
    date_posted DATE,
    link TEXT
);

CREATE TABLE contracts (
    contract_id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(job_id),
    contract_type TEXT NOT NULL,
    salary_min NUMERIC,
    salary_max NUMERIC
);

CREATE TABLE skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name TEXT NOT NULL UNIQUE
);

CREATE TABLE job_skills (
    job_id INTEGER REFERENCES jobs(job_id),
    skill_id INTEGER REFERENCES skills(skill_id),
    PRIMARY KEY (job_id, skill_id)
);