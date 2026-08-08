-- Question 1
-- What are the top 10 highest minimum salaries offered (regardless of contract type), along with the job title and city?

SELECT contracts.salary_min, jobs.city, jobs.title 
FROM contracts INNER JOIN jobs ON contracts.job_id = jobs.job_id 
ORDER BY contracts.salary_min DESC LIMIT 10

-- Question 2
-- What is the average minimum salary for each contract type (uop vs b2b)?

SELECT contract_type, AVG(salary_min) AS avg_salary_min
FROM contracts
GROUP BY contract_type

-- Question 3
-- What are the top 10 most in-demand skills across all job postings, ranked by how many jobs require them?

SELECT skills.skill_name, COUNT(job_skills.job_id) AS demand_count
FROM skills JOIN job_skills ON skills.skill_id = job_skills.skill_id
GROUP BY skills.skill_id, skills.skill_name
ORDER BY demand_count DESC
LIMIT 10

-- Question 4
-- Which cities have an average minimum salary above the overall average minimum salary across all cities?

SELECT jobs.city, AVG(contracts.salary_min) as avg_min_salary
FROM jobs JOIN contracts ON jobs.job_id = contracts.job_id
GROUP BY jobs.city
HAVING
	AVG(contracts.salary_min) > (
		SELECT AVG(salary_min) FROM contracts
	)
ORDER BY avg_min_salary DESC


-- Question 5
-- For each job, show its title, city, salary_min, and its salary rank within its own city (rank 1 = highest salary in that city).

SELECT
    jobs.title,
    jobs.city,
    contracts.salary_min,
    RANK() OVER (PARTITION BY jobs.city ORDER BY contracts.salary_min DESC) AS city_rank
FROM jobs
JOIN contracts ON jobs.job_id = contracts.job_id
ORDER BY jobs.city, city_rank