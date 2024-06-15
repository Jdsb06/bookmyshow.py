create table bookmyshow.user
(
    user_id   int          not null
        primary key,
    user_name varchar(100) not null,
    phone     varchar(30)  not null,
    pass_word varchar(100) not null,
    city      varchar(20)  not null
);

