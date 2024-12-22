DELETE FROM doctor_locations;
DELETE FROM doctors;
DELETE FROM locations;

INSERT INTO doctors(id, first_name, last_name) VALUES (0, 'Jane', 'Wright');
INSERT INTO doctors(id, first_name, last_name) VALUES (1, 'Joseph', 'Lister');

INSERT INTO locations(id, address) VALUES (0, '1 Park St');
INSERT INTO locations(id, address) VALUES (1, '2 University Ave');

INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (0, 0, 0);
INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (1, 1, 0);
INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (2, 1, 1);
