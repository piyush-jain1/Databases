DROP PROCEDURE IF EXISTS count_credits;

DELIMITER $$

CREATE PROCEDURE count_credits()
BEGIN
	DECLARE cur1 CURSOR FOR 
		SELECT cw.roll_number, cw.name, SUM(cc.number_of_credits) AS credits
		FROM cwsl AS cw, cc AS cc
		WHERE cc.course_id = cw.course_id
		GROUP BY cw.roll_number, cw.name;
	DROP TABLE IF EXISTS ccr;
	CREATE TABLE ccr (roll_number VARCHAR(15),name VARCHAR(50),credits int);
	BLOCK1: BEGIN
		DECLARE roll_number VARCHAR(15);
		DECLARE name VARCHAR(50);
		DECLARE credits int;
		DECLARE exit_loop1 boolean DEFAULT FALSE;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop1 = TRUE;
		OPEN cur1;
		loop1 : LOOP
			FETCH cur1 INTO roll_number, name, credits;
			IF credits > 40 THEN
				INSERT INTO ccr values(roll_number, name, credits);
			END IF;
			IF exit_loop1 THEN
				CLOSE cur1;
				LEAVE loop1;
			END IF;
		END LOOP loop1;
	END BLOCK1;
	SELECT * FROM ccr;
END $$

DELIMITER ;

CALL count_credits();

