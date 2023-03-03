CREATE TABLE items (
   id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
   name varchar(255) NOT NULL,
   price numeric(20, 2) NOT NULL,
   qty integer NOT NULL
);