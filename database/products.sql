CREATE TABLE IF NOT EXISTS products(
id SERIAL PRIMARY KEY,
name TEXT,
price INT,
type TEXT,
role_id BIGINT,
status BOOLEAN DEFAULT TRUE
);

INSERT INTO products(name,price,type,status)
VALUES
('VIP Membership',1000,'ROLE',true),
('Genesis Pass',5000,'NFT',true);
