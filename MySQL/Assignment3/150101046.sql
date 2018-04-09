drop database if exists 25jan2018;
create database 25jan2018;
use 25jan2018;

CREATE TABLE ett
(
	course_id varchar(10) not null,
	exam_date DATE not null,
	start_time varchar(10) not null,
	end_time varchar(10) not null,
	CONSTRAINT ettKey PRIMARY KEY (course_id,exam_date,start_time)
);

CREATE TABLE cc
(
	course_id varchar(10) not null,
	number_of_credits int DEFAULT 0 CHECK (number_of_credits BETWEEN 0 AND 12),
	CONSTRAINT ccKey PRIMARY KEY (course_id)
);

CREATE TABLE cwsl
(
	cid varchar(10) not null,
	serial_number int,
	roll_number varchar(15) not null,
	name varchar(50),
	email varchar(50),
	CONSTRAINT cwslKey PRIMARY KEY (cid, roll_number)
);

drop table if exists ett_temp;
CREATE TEMPORARY TABLE ett_temp
(
	course_id varchar(10) not null,
	exam_date DATE not null,
	start_time varchar(10) not null,
	end_time varchar(10) not null,
	CONSTRAINT ettKey PRIMARY KEY (course_id,exam_date,start_time)
);

drop table if exists cc_temp;
CREATE TEMPORARY TABLE cc_temp
(
	course_id varchar(10) not null,
	number_of_credits int DEFAULT 0 CHECK (number_of_credits BETWEEN 0 AND 12),
	CONSTRAINT ccKey PRIMARY KEY (course_id)
);

drop table if exists cwsl_temp;
CREATE TEMPORARY TABLE cwsl_temp
(
	cid varchar(10) not null,
	serial_number int,
	roll_number varchar(15) not null,
	name varchar(50),
	email varchar(50),
	CONSTRAINT cwslKey PRIMARY KEY (cid, roll_number)
);

CREATE TABLE ett_clone LIKE ett;
CREATE TABLE cc_clone LIKE cc;
CREATE TABLE cwsl_clone LIKE cwsl;

describe ett;
describe cc;
describe cwsl;

describe ett_temp;
describe cc_temp;
describe cwsl_temp;

describe ett_clone;
describe cc_clone;
describe cwsl_clone;