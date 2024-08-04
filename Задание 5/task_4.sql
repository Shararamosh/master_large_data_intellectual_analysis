SELECT studentname
FROM students JOIN exam_result on students.studentid = exam_result.studentid
GROUP BY studentname
HAVING MAX(grade)<3