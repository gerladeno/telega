create table chat (
    id          integer primary key,
    name        text
);

create table message(
    id          integer not null,
    version     integer,
    user_id     integer,
    act_date    date not null,
    create_date date not null,
    chat_id     integer,
    state       integer,
    content     text,
    foreign key (chat_id) references chat(id),
    foreign key (user_id) references users(id),
    unique(id, version)
);

create table users(
    id          integer primary key,
    name        text
);

create table monitored_chat(
    id          integer primary key,
    name        text,
    foreign key (name) references chat(name)
);