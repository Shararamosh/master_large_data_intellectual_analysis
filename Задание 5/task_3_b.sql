SELECT studentname, AVG(grade) AS avg_grade
FROM students JOIN exam_result on students.studentid = exam_result.studentid
GROUP BY studentname
ORDER BY AVG(grade) ASC
LIMIT 1