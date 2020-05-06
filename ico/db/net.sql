CREATE DATABASE net 
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE TABLE net.tw (
tweet_id bigint(20) NOT NULL PRIMARY KEY,
screen_name varchar(24),
tweet_at datetime,
born datetime,
urls varchar(1024),
symbols varchar(512),
description varchar(320),
username varchar(64),
text varchar(320),
followers bigint(10),
friends bigint(10),
source varchar(128),
location varchar(256),
statuses_count bigint(20),
time_zone varchar(48),
utc_offset varchar(24),
user_id bigint(20),
verified bool,
in_reply_to_screen_name varchar(512),
in_reply_to_status_id bigint(20),
in_reply_to_user_id bigint(20),
user_mentions varchar(2048),
logged datetime,
profile_img varchar(256),
bg_color varchar(6),
banner_url varchar(128),
link_color varchar(6),
url varchar(256));


CREATE TABLE net.loc (
meta varchar(128),
account varchar(128),
address varchar(128),
account_created datetime,
account_updated datetime,
owner varchar(128),
altnames varchar(256),
city varchar(64),
state varchar(64),
usr_co varchar(64),
adm_co varchar(64),
born datetime,
emails varchar(256),
updated datetime,
admin_title varchar(128),
notes varchar(256),
logged datetime);

CREATE TABLE net.rev (
pack varchar(256),
assess bigint(10),
rate bigint(4),
area varchar(48),
mgr varchar(128),
rank bigint(2),
attend varchar(6),
owner varchar(128),
found datetime);
