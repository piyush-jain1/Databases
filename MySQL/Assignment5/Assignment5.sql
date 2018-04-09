-- Question (a)
SELECT DISTINCT course_id AS 'Courses in Room 2001' 
FROM scheduledIn 
WHERE room_number = '2001';

-- Question (b)
SELECT DISTINCT course_id AS 'Courses in Slot C' 
FROM scheduledIn 
WHERE letter = 'C';

-- Question (c)
SELECT DISTINCT division AS 'Divisions which are alloted to room L2 or L3' 
FROM scheduledIn 
WHERE room_number = 'L2' or room_number = 'L3';

-- Question (d)
SELECT course_id AS 'Courses which are alloted to multiple rooms' 
FROM (
		SELECT course_id,COUNT(DISTINCT room_number) AS room_count
		FROM scheduledIn
		GROUP BY course_id
		) AS room_count_table
WHERE room_count_table.room_count > 1;

-- Question (e)
SELECT DISTINCT name AS 'Department in which any of the course have been alloted to L1 or L2 or L3 or L4' 
FROM scheduledIn 
NATURAL JOIN department 
WHERE room_number IN ('L1', 'L2', 'L3', 'L4');

-- Question (f)
SELECT name AS 'Department names which do not use L1 or L2 rooms' 
FROM (
		SELECT department_id 
		FROM department 
		WHERE department_id NOT IN (
									SELECT DISTINCT department_id
									FROM scheduledIn
									WHERE room_number IN ('L1', 'L2')
									)
	) AS depts
NATURAL JOIN department;


-- Question (g)
SELECT department_id AS 'Department which ahve utilized all the slots'
FROM (
	SELECT DISTINCT department_id, letter
	FROM scheduledIn
	) AS department_slots
GROUP BY department_id
HAVING COUNT(*) = (SELECT COUNT(DISTINCT letter)
						FROM slot);

-- Question (h)
SELECT letter AS Slot, COUNT(DISTINCT course_id) AS 'Number of Courses' 
FROM scheduledIn 
GROUP BY letter
ORDER BY COUNT(DISTINCT(course_id)) ASC;

-- Question (i)
SELECT room_number, COUNT(DISTINCT course_id) AS 'Number of Courses' 
FROM scheduledIn 
GROUP BY room_number 
ORDER BY COUNT(DISTINCT(course_id)) DESC;

-- Question (j)
SELECT letter AS 'Slot with minimum number of courses'
FROM (
	SELECT letter, COUNT(DISTINCT course_id) AS course_count
	FROM scheduledIn 
	GROUP BY letter
	) AS course_count_table
WHERE course_count = (SELECT MIN(course_count) 
					  FROM (
					  	SELECT letter, COUNT(DISTINCT course_id) AS course_count
						FROM scheduledIn 
						GROUP BY letter
						) AS course_count_table );

-- Question (k)
SELECT DISTINCT(letter) AS 'Slots Assigned to Minor Courses' 
FROM scheduledIn 
WHERE course_id RLIKE '.*[M]$';

-- Question (l)
SELECT name AS 'Department Name', letter AS 'Slot Unused'
FROM
	(
		SELECT * 
		FROM (
			SELECT * 
			FROM
				(SELECT DISTINCT department_id FROM department) AS dept 
			CROSS JOIN 
				(SELECT DISTINCT letter FROM slot) AS letter
			) AS all_dept_slots
		WHERE  (department_id, letter) NOT IN (	
					SELECT DISTINCT department_id, letter
					FROM scheduledIn
				)
	) AS answer
NATURAL JOIN department
ORDER BY department_id;
