create table bookmyshow.shows
(
    show_id         int            not null
        primary key,
    Title           varchar(100)   not null,
    Genre           varchar(30)    not null,
    ticket_price    decimal(10, 2) not null,
    Rating          decimal(10, 2) not null,
    Duration        time           not null,
    Date            date           not null,
    available_seats int            not null
);

