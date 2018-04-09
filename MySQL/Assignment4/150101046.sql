drop database if exists 09feb2018;
create database 09feb2018;
use 09feb2018;

CREATE TABLE course
(
	course_id varchar(10) not null,
	division ENUM('I','II','III','IV','NA') DEFAULT 'NA',
	CONSTRAINT courseKey PRIMARY KEY (course_id,division)
);

CREATE TABLE department
(
	department_id varchar(10) not null,
	name varchar(50),
	CONSTRAINT departmentKey PRIMARY KEY (department_id)
);

CREATE TABLE slot
(
	letter ENUM('A','B','C','D','E','F','G','H','I','J','K','L','A1','B1','C1','D1','E1'),
	day ENUM('Monday','Tuesday','Wednesday','Thursday','Friday'),
	start_time varchar(10) not null,
	end_time varchar(10) not null,
	CONSTRAINT slotKey PRIMARY KEY (letter,day)
);

CREATE TABLE room
(
	room_number varchar(20) not null,
	location ENUM('Core-I','Core-II','Core-III','Core-IV','LH','Local'),
	CONSTRAINT roomKey PRIMARY KEY (room_number)
);

CREATE TABLE scheduledIn
(
	course_id varchar(10) not null,				/* course which ahs been scheduled */
	division ENUM('I','II','III','IV','NA') DEFAULT 'NA' not null,		/* divisions for which course is there */
	department_id varchar(10) not null,			/* department fromw hich course belongs	*/
	letter ENUM('A','B','C','D','E','F','G','H','I','J','K','L','A1','B1','C1','D1','E1') not null,		/* slot letter in which course has been scheduled */
	day ENUM('Monday','Tuesday','Wednesday','Thursday','Friday') not null,	/* day on which the scheduled slot occurs */
	room_number varchar(20) not null,			/* room number in which the course is scheduled */
	CONSTRAINT fKey_course FOREIGN KEY (course_id,division) REFERENCES course(course_id,division),
	CONSTRAINT fKey_department FOREIGN KEY (department_id) REFERENCES department(department_id),
	CONSTRAINT fKey_slot FOREIGN KEY (letter,day) REFERENCES slot(letter,day),
	CONSTRAINT fKey_room FOREIGN KEY (room_number) REFERENCES room(room_number),
	CONSTRAINT scheduledInKey PRIMARY KEY (course_id,division,department_id,letter,day,room_number)
);

describe course;
describe department;
describe slot;
describe room;
describe scheduledIn;
