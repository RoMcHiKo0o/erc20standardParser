--file with table create, reset status of records and table truncate

-- create type contract_status as enum ('waits processing', 'processing', 'processed');
-- drop table contract;

-- create table contract(
-- 	contract_address varchar(50) primary key,
-- 	source_code bytea,
-- 	is_erc20 boolean default false,
-- 	erc20_version varchar(20),
-- 	status contract_status default 'waits processing'
-- )

-- update contract
-- 	set status = 'waits processing'

-- truncate contract;
select count(*) from contract