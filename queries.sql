SELECT contracts.salary_min, jobs.city, jobs.title 
FROM contracts INNER JOIN jobs ON contracts.job_id = jobs.job_id 
ORDER BY contracts.salary_min DESC LIMIT 10

