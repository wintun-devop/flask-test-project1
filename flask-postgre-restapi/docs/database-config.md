# User Creation and Privileges Access
CREATE USER youruser WITH ENCRYPTED PASSWORD 'yourpass';
ALTER USER youruser WITH SUPERUSER;
ALTER USER youruser WITH CREATEDB;
ALTER USER youruser WITH REPLICATION;


# Create Database
psql -U DATABASE_USER_NAME -p 5432 -h DATABASE_HOST -d DATABASE_NAME

# Create Table with custom uuid
CREATE EXTENSION "uuid-ossp";
CREATE TABLE items (
   id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
   name varchar(255) NOT NULL,
   vendor varchar(100) NOT NULL,
   model varchar(100) NOT NULL,
   remark varchar(255) NOT NULL
);

INSERT INTO items (name,vendor,model,remark) VALUES ('HP Probox 440 G5','HP','HP-440G5','Mix Range');