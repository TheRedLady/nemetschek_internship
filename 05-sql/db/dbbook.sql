--
-- 	Database Table Creation
--
--		This file will create the tables for use with the book 
--  Database Management Systems by Raghu Ramakrishnan and Johannes Gehrke.
--  It is run automatically by the installation script.
--
--	Version 0.1.0.0 2002/04/05 by: David Warden.
--	Copyright (C) 2002 McGraw-Hill Companies Inc. All Rights Reserved.
--
--  First drop any existing tables. Any errors are ignored.
--
drop table if exists emp cascade;
drop table if exists works cascade;
drop table if exists dept cascade;
drop table if exists flights cascade;
drop table if exists aircraft cascade;
drop table if exists certified cascade;
drop table if exists employees cascade;
drop table if exists suppliers cascade;
drop table if exists parts cascade;
drop table if exists catalog cascade;
drop table if exists sailors cascade;
--
-- Now, add each table.
--
create table emp(
	eid serial primary key,
	ename varchar(30),
	age numeric(3,0),
	salary money
	);
create table dept(
	did serial primary key,
	dname varchar(20),
	budget money,
	managerid integer references emp(eid)
	);
create table works(
	eid integer references emp (eid),
	did integer references dept (did),
	pct_time integer,
	primary key(eid,did)
	);
create table flights(
	flno serial primary key,
	origin varchar(20),
	destination varchar(20),
	distance integer,
	departs date,
	arrives date,
	price money
	);
create table aircraft(
	aid serial primary key,
	aname varchar(30),
	crusingrange integer
	);
create table employees(
	eid serial primary key,
	ename varchar(30),
	salary money
	);
create table certified(
	eid integer references employees (eid),
	aid integer references aircraft (aid),
	primary key(eid,aid)
	);
create table suppliers(
	sid serial primary key,
	sname varchar(30),
	address varchar(50)
	);
create table parts(
	pid serial primary key,
	pname varchar(40),
	color varchar(15)
	);
create table catalog(
	sid integer references suppliers (sid),
	pid integer references parts (pid),
	cost money,
	primary key(sid,pid)
	);
create table sailors(
	sid serial primary key,
	sname varchar(30),
	rating integer,
	age numeric(3,0)
	);

\copy aircraft from '/data/aircraft.txt' delimiter ',' csv
\copy suppliers from '/data/suppliers.txt' delimiter ',' csv
\copy parts from '/data/parts.txt' delimiter ',' csv
\copy catalog from '/data/catalog.txt' delimiter ',' csv
\copy employees from '/data/employees.txt' delimiter ',' csv
\copy certified from '/data/certified.txt' delimiter ',' csv
\copy emp from '/data/emp.txt' delimiter ',' csv
\copy dept from '/data/dept.txt' delimiter ',' csv
\copy flights from '/data/flights.txt' delimiter ',' csv
\copy sailors from '/data/sailors.txt' delimiter ',' csv
\copy works from '/data/works.txt' delimiter ',' csv

--
-- Exit the Script.
--
