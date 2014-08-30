USE COMES;
DROP TABLE IF EXISTS opcode_variety;
DROP TABLE IF EXISTS bigram_variety;
DROP TABLE IF EXISTS trigram_variety;
DROP TABLE IF EXISTS file_name;
DROP TABLE IF EXISTS instruction_sequence;
DROP TABLE IF EXISTS instruction_code_block;
DROP TABLE IF EXISTS corrupted_instruction_sequence;
DROP TABLE IF EXISTS compiler_information;
DROP TABLE IF EXISTS optimization_level_information;

CREATE TABLE opcode_variety (
    id 			integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
    opcode_name	varchar(32) NOT NULL UNIQUE KEY
);

CREATE TABLE bigram_variety (
	id			integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
	bigram1		varchar(32) NOT NULL,
	bigram2		varchar(32) NOT NULL,
	UNIQUE (bigram1, bigram2)
);

CREATE TABLE trigram_variety (
	id			integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
	trigram1	varchar(32) NOT NULL,
	trigram2	varchar(32) NOT NULL,
	trigram3	varchar(32) NOT NULL,
	UNIQUE (trigram1, trigram2, trigram3)
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

CREATE TABLE instruction_code_block (
	id				integer AUTO_INCREMENT PRIMARY KEY,
	file_name		varchar(64) NOT NULL,
	instruction_id	integer NOT NULL,
	subroutine		varchar(32) NOT NULL,
	location		varchar(32)
);

CREATE TABLE corrupted_instruction_sequence (
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

CREATE TABLE optimization_level_information (
	file_name			varchar(64) NOT NULL UNIQUE KEY,
	optimization_level	varchar(32) NOT NULL
);