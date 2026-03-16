WITH 
brands_models(id, brand, model) AS (
    VALUES 
    (1,'Toyota','Camry'), (2,'Toyota','Corolla'),
    (3,'Honda','Civic'), (4,'Honda','CR-V'),
    (5,'BMW','3 Series'), (6,'BMW','X5'),
    (7,'Audi','A4'), (8,'Audi','Q5'),
    (9,'Mercedes-Benz','C-Class'), (10,'Mercedes-Benz','E-Class'),
    (11,'Kia','Sportage'), (12,'Kia','Rio'),
    (13,'Hyundai','Solaris'), (14,'Hyundai','Tucson'),
    (15,'Lada','Vesta'), (16,'Lada','Granta'),
    (17,'Ford','Focus'), (18,'Ford','Mondeo'),
    (19,'Volkswagen','Golf'), (20,'Skoda','Octavia'),
    (21,'Nissan','Qashqai'), (22,'Mazda','6'),
    (23,'Subaru','Outback'), (24,'Renault','Megane'),
    (25,'Peugeot','308'), (26,'Citroen','C4'),
    (27,'Opel','Astra'), (28,'Chevrolet','Cruze'),
    (29,'Jeep','Cherokee'), (30,'Mitsubishi','Outlander')
),
bodies(id, body_type) AS (
    VALUES (1,'седан'),(2,'хэтчбек'),(3,'внедорожник'),
    (4,'универсал'),(5,'купе'),(6,'лифтбек')
),
fuels(id, fuel) AS (
    VALUES (1,'бензин'),(2,'дизель'),(3,'гибрид'),(4,'электро'),(5,'газ')
),
trans(id, transmission) AS (
    VALUES (1,'автомат'),(2,'механика'),(3,'вариатор'),(4,'робот')
),
params(n) AS (VALUES (300)),
seq(i) AS (
    SELECT 1 FROM params 
    UNION ALL 
    SELECT i+1 FROM seq, params WHERE i+1 <= (SELECT n FROM params)
),
cars_data AS (
    SELECT 
        bm.brand,
        bm.model,
        1995 + ABS(RANDOM()) % 30 AS year,
        10000000 + ABS(RANDOM()) % 109900000 AS price,
        b.body_type,
        ABS(RANDOM()) % 400001 AS mileage,
        50 + ABS(RANDOM()) % 451 AS power,
        f.fuel,
        t.transmission
    FROM seq AS rid
    JOIN brands_models AS bm ON bm.id = ((rid.i - 1) % 30) + 1
    JOIN bodies AS b ON b.id = ((rid.i * 1 - 1) % 6) + 1
    JOIN fuels AS f ON f.id = ((rid.i * 7 - 1) % 5) + 1
    JOIN trans AS t ON t.id = ((rid.i * 11 - 1) % 4) + 1
    order by random()
)
INSERT INTO cars (brand, model, year, price, body_type, mileage, power, fuel, transmission)
SELECT * FROM cars_data;

