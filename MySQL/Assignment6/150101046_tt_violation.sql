DROP PROCEDURE IF EXISTS tt_violation;

DELIMITER $$

CREATE PROCEDURE tt_violation()
BEGIN
	DECLARE cur1 CURSOR FOR 
		SELECT DISTINCT c.roll_number, c.name, c.course_id, e.exam_date, e.start_time, e.end_time 
		FROM cwsl AS c, ett AS e 
		WHERE c.course_id = e.course_id;
	DROP TABLE IF EXISTS ttv;
	CREATE TABLE ttv (roll_number VARCHAR(15),name VARCHAR(50),course_id1 VARCHAR(10),course_id2 VARCHAR(10));
	BLOCK1: BEGIN
		DECLARE roll_number1 VARCHAR(15);
		DECLARE name1 VARCHAR(50);
		DECLARE course_id1 VARCHAR(10);
		DECLARE exam_date1 DATE;
		DECLARE start_time1 VARCHAR(10);
		DECLARE end_time1 VARCHAR(10);
		DECLARE exit_loop1 boolean DEFAULT FALSE;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop1 = TRUE;
		OPEN cur1;
		loop1 : LOOP
			FETCH cur1 INTO roll_number1, name1, course_id1, exam_date1, start_time1, end_time1;
			BLOCK2: BEGIN
				DECLARE cur2 CURSOR FOR 
					SELECT c.course_id
					FROM cwsl AS c, ett AS e 
					WHERE c.course_id = e.course_id AND c.roll_number = roll_number1 AND e.exam_date = exam_date1 AND e.start_time = start_time1 AND e.end_time = end_time1 AND c.course_id < course_id1;
				BLOCK3: BEGIN
				DECLARE course_id2 VARCHAR(10);
				DECLARE exit_loop2 boolean DEFAULT FALSE;
				DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop2 = TRUE;
				OPEN cur2;
				loop2 : LOOP
					FETCH cur2 INTO course_id2;
					IF course_id2 IS NOT NULL THEN
						INSERT INTO ttv values(roll_number1, name1, course_id1, course_id2);
					END IF;
					IF exit_loop2 THEN
						CLOSE cur2;
						LEAVE loop2;
					END IF;
				END LOOP loop2;
				END BLOCK3;
			END BLOCK2;
		IF exit_loop1 THEN
			CLOSE cur1;
			LEAVE loop1;
		END IF;
		END LOOP loop1;
	END BLOCK1;
	SELECT DISTINCT * FROM ttv;
END $$

DELIMITER ;

CALL tt_violation();

