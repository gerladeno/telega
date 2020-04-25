create USER tcl with PASSWORD 'tcl';
create USER api with PASSWORD 'api';
create SCHEMA tcl;
grant all privileges on schema tcl TO tcl;
grant all privileges on schema tcl TO api;
alter user tcl set SEARCH_PATH to tcl;
alter user api set SEARCH_PATH to tcl;