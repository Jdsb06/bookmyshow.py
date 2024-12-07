-- ====================================================
-- IMPORTANT NOTES:
-- 1. This SQL script is executed by `setup.py` to:
--    - Create the `bookmyshow` database and tables.
--    - Populate the tables with sample data.
-- 2. Ensure this file is in the same directory as `setup.py`.
-- 3. If you modify the schema, re-run `setup.py` to apply changes.
-- ====================================================


CREATE DATABASE IF NOT EXISTS bookmyshow;
USE bookmyshow;

create table if not exists bookmyshow.user
(
    user_id   int          not null
        primary key,
    user_name varchar(100) not null,
    phone     varchar(30)  not null,
    pass_word varchar(100) not null,
    city      varchar(20)  not null
);

create table if not exists bookmyshow.shows
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

insert into bookmyshow.shows (show_id, Title, Genre, ticket_price, Rating, Duration, Date, available_seats)
values  (101, 'Jawan', 'Movie', 110.00, 9.90, '02:49:35', '2023-11-09', 134),
        (102, 'Oppenheimer', 'Movie', 110.00, 7.90, '02:25:35', '2023-10-09', 102),
        (103, 'RRR', 'Movie', 120.00, 8.80, '02:31:23', '2023-10-23', 154),
        (104, 'Carry On Jatta 3', 'Movie', 110.00, 7.20, '02:15:23', '2023-09-11', 120),
        (105, 'Gaurav Kapoor Live', 'Comedy Shows', 130.00, 8.20, '01:05:23', '2023-11-11', 93),
        (106, 'The Bassi Show', 'Comedy Shows', 130.00, 8.90, '01:00:23', '2023-10-21', 138),
        (107, 'Harsh Gujral Live', 'Comedy Shows', 130.00, 9.20, '00:50:23', '2023-11-21', 110),
        (108, 'Shubhh Still Rollin', 'Concert', 150.00, 8.20, '00:59:23', '2024-11-21', 147),
        (110, 'Tiger 3', 'Movie', 200.00, 8.10, '02:35:00', '2023-12-18', 95),
        (111, 'Marvels', 'Movie', 180.00, 7.30, '01:44:52', '2023-11-15', 130),
        (112, 'Abhishek Upmanyu LIVE', 'Comedy Shows', 220.00, 9.20, '01:45:00', '2023-11-15', 85),
        (113, 'Coca-Cola Chandigarh', 'Concert', 180.00, 9.50, '06:00:00', '2023-11-25', 150),
        (114, 'Ed Sheeran', 'Concert', 600.00, 9.20, '02:00:00', '2024-03-16', 200),
        (115, 'Sagar Waali Qawwali', 'Concert', 300.00, 8.50, '04:00:00', '2023-12-24', 99),
        (116, '12th Fail', 'Movie', 190.00, 9.50, '02:27:54', '2023-10-27', 96);
