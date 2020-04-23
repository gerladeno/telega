create USER tcl with PASSWORD 'tcl';
create USER api with PASSWORD 'api';
grant all privileges on DATABASE postgres TO tcl;
grant all privileges on DATABASE postgres TO api;
create SCHEMA tcl;
alter user tcl set SEARCH_PATH to tcl;
alter user api set SEARCH_PATH to tcl;