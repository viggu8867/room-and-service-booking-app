CREATE DATABASE Room;
USE Room;

CREATE TABLE Guest (
    GuestID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(50),
    Address VARCHAR(100),
    Phone VARCHAR(15) Check (Phone REGEXP '^[0-9+\\-()]*$'),
    Age INT
);

CREATE TABLE Room(
    RoomNumber INT PRIMARY KEY,
    RoomType VARCHAR(50),
    Price DECIMAL(10, 2),
    Availability ENUM('Available', 'Occupied', 'Under Maintenance') NOT NULL
);

CREATE TABLE Reservation(
    ReservationID VARCHAR(20) PRIMARY KEY,
    CheckInDate DATE,
    CheckOutDate DATE,
    GuestID VARCHAR(20),
    RoomNumber INT,
    FOREIGN KEY (GuestID) REFERENCES Guest(GuestID) ON DELETE CASCADE,
    FOREIGN KEY (RoomNumber) REFERENCES Room(RoomNumber)
);

CREATE TABLE Staff(
    StaffID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(50),
    Age INT,
    Position VARCHAR(50),
    Salary DECIMAL(10, 2)
);

CREATE TABLE Service (
    ServiceID VARCHAR(20) PRIMARY KEY,
    ServiceName VARCHAR(50),
    ServicePrice DECIMAL(10, 2)
);

CREATE TABLE Booking (
    BookingID VARCHAR(20) PRIMARY KEY,
    ReservationID VARCHAR(20),
    ServiceID VARCHAR(20),
    Date DATE,
    No_of_People INT,
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID) ON DELETE CASCADE,
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID)
);

CREATE TABLE Payments (
    PaymentID VARCHAR(20) PRIMARY KEY,
    ReservationID VARCHAR(20),
    Amount DECIMAL(10, 2),
    PaymentDate DATE,
    PaymentMethod ENUM('Credit/Debit Card','UPI','Cash') DEFAULT 'UPI',
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID) ON DELETE CASCADE
);

CREATE TABLE GuestFeedback (
    FeedbackID VARCHAR(20) PRIMARY KEY,
    GuestID VARCHAR(20),
    Feedback TEXT,
    Rating ENUM('1','2','3','4','5') NOT NULL,
    FOREIGN KEY (GuestID) REFERENCES Guest(GuestID) ON DELETE CASCADE
);

CREATE TABLE User (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50),
    Password VARCHAR(50) UNIQUE,
    Privileges ENUM('admin', 'standard') DEFAULT 'standard'
);

INSERT INTO User VALUES (1,'Shashank','Shan@123','admin');
INSERT INTO Guest VALUES('G01','Vignesh','Like Home PG,Besides PES University Back Gate,Dwaraka Nagar,Bengaluru','9036130794',20),
						('G02','Puneeth','Maruti PG,Besides PES University Back Gate,Dwaraka Nagar,Bengaluru','90561307286',25),
                        ('G03','Samrudh','Akshay PG,Besides PES University Back Gate,Dwaraka Nagar,Bengaluru','9033134774',29),
                        ('G04','Shashank Bellad','Veereshwar Nilaya,Dwaraka Nagar,Bengaluru','9006135764',21),
                        ('G05','Shreyas P Hiremath','Skyline Apartment,Dwaraka Nagar,Bengaluru','9038134794',33);
                        
INSERT INTO Room VALUES (100,'Single Room',2000.00,'Available'),
						(101,'Double Room',3500.00,'Available'),
                        (102,'Double Room',3500.00,'Occupied'),
                        (103,'Double Room',3500.00,'Occupied'),
                        (104,'Triple Room',5000.00,'Available'),
                        (200,'Single Room',2000.00,'Occupied'),
                        (201,'Double Room',3500.00,'Available'),
                        (202,'Double Room',3500.00,'Available'),
                        (203,'Double Room',3500.00,'Available'),
                        (204,'Triple Room',5000.00,'Occupied'),
                        (300,'Single Room',2000.00,'Available'),
                        (301,'Double Room',3500.00,'Available'),
                        (302,'Double Room',3500.00,'Occupied'),
                        (303,'Double Room',3500.00,'Available'),
                        (304,'Triple Room',5000.00,'Available'),
                        (400,'Single Room',2000.00,'Available'),
                        (401,'Double Room',3500.00,'Available'),
                        (402,'Double Room',3500.00,'Available'),
                        (403,'Double Room',3500.00,'Available'),
                        (404,'Double Room',5000.00,'Available');

INSERT INTO Reservation VALUES  ('R001','2023-11-02','2023-11-05','G01',103),
								('R002','2023-11-02','2023-11-05','G02',102),
                                ('R003','2023-11-04','2023-11-08','G03',302),
                                ('R004','2023-11-06','2023-11-09','G04',204),
                                ('R005','2023-11-01','2023-11-03','G05',200);

INSERT INTO Staff VALUES('S01','Ramesh Sharma',35,'Housekeeping',12000.00),
						('S02','Suresh Sharma',35,'Housekeeping',52000.00),
                        ('S03','Ravi',33,'Waiter',12000.00),
                        ('S04','Ram Nayak',32,'Room Attendant',12000.00),
                        ('S05','Aakash Patil',35,'Receptionist',10000.00),
                        ('S06','Roshan Singh',40,'Assistant Manager',15000.00),
                        ('S07','Krishna',38,'',15000.00),
                        ('S08','Aryan Gupta',28,'Waiter',10000.00),
                        ('S09','Priya Varma',30,'Room Attendant',10000.00),
                        ('S10','Pooja Das',33,'Receptionist',12000.00);
                        
INSERT INTO Service VALUES  ('SER01','Room Service',4000.00),	
							('SER02','Transportation',3000.00),
                            ('SER03','Spa and Wellness',2500.00),
                            ('SER04','Entertainment',2000.00),
                            ('SER05','Internet',2000.00),
                            ('SER06','Recreational Facilities',3000.00),
                            ('SER07','Fitness',1000.00);

INSERT INTO Booking VALUES  ('B001','R001','SER01','2024-11-05',4),
							('B002','R001','SER05','2024-11-05',4),
							('B003','R001','SER06','2024-11-05',4),
                            ('B005','R003','SER01','2024-11-05',4),
                            ('B006','R003','SER02','2024-11-05',4),
                            ('B007','R003','SER03','2024-11-05',4),
                            ('B008','R004','SER01','2024-11-05',2),
                            ('B009','R004','SER05','2024-11-05',2),
							('B010','R005','SER01','2024-11-05',4),
                            ('B011','R005','SER05','2024-11-05',4);
                            
INSERT INTO Payments VALUES  ('P01','R001',10000.00,'2024-11-05','Cash'),
							('P02','R002',8000.00,'2024-11-05','Cash'),
                            ('P03','R003',10000.00,'2024-11-08','Cash'),
                            ('P04','R004',8000.00,'2024-11-09','Cash'),
                            ('P05','R005',6000.00,'2024-11-03','Cash');
							
INSERT INTO GuestFeedback VALUES('F01','G01','Great service and comfortable stay!','5'),
								('F02','G02','The staff was very helpful and friendly.','5'),
                                ('F03','G03','Good experience, but room cleanliness can be improved.','4'),
                                ('F04','G04','Good stay, expected more amenities.','4'),
                                ('F05','G05','Fantastic hotel, loved every moment of our stay!','5');

DELIMITER //

CREATE TRIGGER UpdateRoomAvailability
AFTER INSERT ON Reservation
FOR EACH ROW
BEGIN
    UPDATE Room
    SET Availability = 'Occupied'
    WHERE RoomNumber = NEW.RoomNumber;
END;
//

CREATE TRIGGER UpdateRoomAvailabilityOnUpdate
AFTER UPDATE ON Reservation
FOR EACH ROW
BEGIN
    -- Ensure the RoomNumber is changed
    IF OLD.RoomNumber != NEW.RoomNumber THEN
        -- Update the availability of the old room
        IF OLD.RoomNumber IS NOT NULL THEN
            UPDATE Room
            SET Availability = 'Available'
            WHERE RoomNumber = OLD.RoomNumber;
        END IF;

        -- Update the availability of the new room
        IF NEW.RoomNumber IS NOT NULL THEN
            UPDATE Room
            SET Availability = 'Occupied'
            WHERE RoomNumber = NEW.RoomNumber;
        END IF;
    END IF;
END;
//

CREATE TRIGGER UpdateRoomAvailabilityOnDelete
AFTER DELETE ON Reservation
FOR EACH ROW
BEGIN
    -- Set the room associated with the deleted reservation to 'Available'
    IF OLD.RoomNumber IS NOT NULL THEN
        UPDATE Room
        SET Availability = 'Available'
        WHERE RoomNumber = OLD.RoomNumber;
    END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE insert_admin_user(IN p_username VARCHAR(50),IN p_password VARCHAR(50))
BEGIN
    DECLARE admin_count INT;

    -- Check if the new user is being assigned admin privileges
    IF (SELECT COUNT(*) FROM User WHERE Privileges = 'admin') > 2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: There can be only be three user with admin privileges.';
    ELSE
        -- Insert the new user with admin privileges
        INSERT INTO User (Username, Password, Privileges) VALUES (p_username, p_password, 'admin');
        SELECT 'User with admin privileges inserted successfully.' AS Message;
    END IF;
END //
DELIMITER ;

DELIMITER //

CREATE PROCEDURE grant_admin_role(IN user_id_to_change VARCHAR(255),IN new_role ENUM('admin', 'standard'))
BEGIN
    DECLARE admin_count INT;

    -- Get the current count of users with admin privileges
    SELECT COUNT(*) INTO admin_count FROM User WHERE Privileges = 'admin';

    -- Check if the count is one and the user is already an admin
    IF new_role="standard" AND admin_count = 1 AND EXISTS (SELECT 1 FROM User WHERE Username = user_id_to_change AND Privileges = 'admin') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot remove the last admin user.';
	END IF;
	IF new_role = "admin" THEN 
		-- Check if the count exceeds three and the user is not already an admin
		IF admin_count >= 3 AND NOT EXISTS (SELECT 1 FROM User WHERE Username = user_id_to_change AND Privileges = 'admin') THEN
			SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Cannot grant admin role. Maximum admin count exceeded.';
		ELSE
			-- Update the user's role to admin
			UPDATE User SET Privileges = 'admin' WHERE Username = user_id_to_change;
		END IF;
    END IF;
END //

DELIMITER ;

