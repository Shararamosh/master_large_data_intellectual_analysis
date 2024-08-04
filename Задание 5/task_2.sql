SELECT studentname, AVG(grade) AS avg_grade
FROM students JOIN exam_result ON students.studentid = exam_result.studentid
GROUP BY studentname
HAVING AVG(grade) > 4.5
ORDER BY avg_grade DESC