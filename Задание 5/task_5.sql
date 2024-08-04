SELECT teachername, AVG(grade)
FROM teacher
JOIN exam_sheet ON teacher.teacherid = exam_sheet.teacherid
JOIN exam_result ON exam_sheet.examsheetid = exam_result.examsheetid
GROUP BY teachername