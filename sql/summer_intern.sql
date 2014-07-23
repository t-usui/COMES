DROP TABLE IF EXISTS opcode_variety;
DROP TABLE IF EXISTS file_name;
DROP TABLE IF EXISTS instruction_sequence;
DROP TABLE IF EXISTS compiler_information;

CREATE TABLE opcode_variety (
    id integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
    opcode_name varchar(32) NOT NULL UNIQUE KEY
);

CREATE TABLE file_name (
	id			integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
	file_name	varchar(64) NOT NULL UNIQUE KEY
); 

CREATE TABLE instruction_sequence (
	file_name		varchar(64) NOT NULL,
	instruction_id	integer NOT NULL,
	opcode			varchar(16) NOT NULL,
	operand1		varchar(16),
	operand2		varchar(16)
);

CREATE TABLE compiler_information (
	file_name	varchar(64) NOT NULL UNIQUE KEY,
	compiler	varchar(32) NOT NULL
);