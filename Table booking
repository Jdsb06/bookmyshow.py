create table if not exists bookmyshow.booking
(
    Booking_id  int auto_increment
        primary key,
    user_id     int            not null,
    user_name   varchar(100)   not null,
    show_id     int            not null,
    num_tickets int            not null,
    Total_price decimal(10, 2) null,
    constraint booking_ibfk_2
        foreign key (show_id) references bookmyshow.shows (show_id),
    constraint booking_user_user_id_fk
        foreign key (user_id) references bookmyshow.user (user_id)
);

create index show_id
    on bookmyshow.booking (show_id);
