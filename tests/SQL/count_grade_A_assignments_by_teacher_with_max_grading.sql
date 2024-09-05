-- Find the number of grade A's given by the teacher who has graded the most assignments
SELECT teacher_id, COUNT(CASE WHEN grade = 'A' THEN 1 END) AS grade_A_count
FROM Assignments
WHERE teacher_id = (
    -- Subquery to find the teacher who graded the most assignments
    SELECT teacher_id
    FROM Assignments
    GROUP BY teacher_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
)
GROUP BY teacher_id;
