CREATE TABLE ico.tickers (
id varchar(128),
name varchar(128),
symbol varchar(10),
rank int,
price_usd decimal(9,2),
price_btc decimal(12,8),
24h_volume_usd bigint(20),
market_cap_usd bigint(20),
available_supply bigint(20),
total_supply bigint(20),
percent_change_1h decimal(5,2),
percent_change_24h decimal(5,2),
percent_change_7d decimal(5,2),
last_updated bigint(20),
logged datetime);
