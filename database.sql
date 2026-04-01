-- ============================================================
-- Farmer-Crop-Instructor Training Management System
-- Database: Microsoft SQL Server (SSMS)
-- Run this entire script in SSMS Query Window
-- ============================================================

-- Create and use the database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'farmer_training_db')
    CREATE DATABASE farmer_training_db;
GO

USE farmer_training_db;
GO

-- -----------------------------------------------
-- Table: Farmers
-- -----------------------------------------------
IF OBJECT_ID('FarmerTraining', 'U') IS NOT NULL DROP TABLE FarmerTraining;
IF OBJECT_ID('Training',       'U') IS NOT NULL DROP TABLE Training;
IF OBJECT_ID('Farmers',        'U') IS NOT NULL DROP TABLE Farmers;
IF OBJECT_ID('Crops',          'U') IS NOT NULL DROP TABLE Crops;
IF OBJECT_ID('Instructors',    'U') IS NOT NULL DROP TABLE Instructors;
GO

CREATE TABLE Farmers (
    FarmerID  INT IDENTITY(1,1) PRIMARY KEY,
    Name      NVARCHAR(100) NOT NULL,
    Village   NVARCHAR(100) NOT NULL,
    Phone     NVARCHAR(15),
    LandArea  DECIMAL(10, 2)   -- in acres
);
GO

-- -----------------------------------------------
-- Table: Crops
-- -----------------------------------------------
CREATE TABLE Crops (
    CropID   INT IDENTITY(1,1) PRIMARY KEY,
    CropName NVARCHAR(100) NOT NULL,
    Season   NVARCHAR(50)  NOT NULL
);
GO

-- -----------------------------------------------
-- Table: Instructors
-- -----------------------------------------------
CREATE TABLE Instructors (
    InstructorID   INT IDENTITY(1,1) PRIMARY KEY,
    Name           NVARCHAR(100) NOT NULL,
    Specialization NVARCHAR(100),
    Organization   NVARCHAR(150)
);
GO

-- -----------------------------------------------
-- Table: Training
-- -----------------------------------------------
CREATE TABLE Training (
    TrainingID   INT IDENTITY(1,1) PRIMARY KEY,
    CropID       INT  NOT NULL,
    InstructorID INT  NOT NULL,
    Date         DATE NOT NULL,
    Location     NVARCHAR(150),
    CONSTRAINT FK_Training_Crop       FOREIGN KEY (CropID)       REFERENCES Crops(CropID),
    CONSTRAINT FK_Training_Instructor FOREIGN KEY (InstructorID) REFERENCES Instructors(InstructorID)
);
GO

-- -----------------------------------------------
-- Table: FarmerTraining (Many-to-Many)
-- -----------------------------------------------
CREATE TABLE FarmerTraining (
    FarmerID   INT NOT NULL,
    TrainingID INT NOT NULL,
    CONSTRAINT PK_FarmerTraining PRIMARY KEY (FarmerID, TrainingID),
    CONSTRAINT FK_FT_Farmer   FOREIGN KEY (FarmerID)   REFERENCES Farmers(FarmerID),
    CONSTRAINT FK_FT_Training FOREIGN KEY (TrainingID) REFERENCES Training(TrainingID)
);
GO

-- -----------------------------------------------
-- Sample Data
-- -----------------------------------------------
INSERT INTO Farmers (Name, Village, Phone, LandArea) VALUES
('Ravi Kumar',   'Anantapur', '9876543210', 4.50),
('Lakshmi Devi', 'Kurnool',   '9812345678', 2.75),
('Srinivas Rao', 'Nellore',   '9898765432', 6.00),
('Padma Reddy',  'Guntur',    '9765432198', 3.25),
('Venkat Naidu', 'Vizag',     '9745612398', 5.10);
GO

INSERT INTO Crops (CropName, Season) VALUES
('Rice',      'Kharif'),
('Wheat',     'Rabi'),
('Cotton',    'Kharif'),
('Groundnut', 'Rabi'),
('Sunflower', 'Zaid');
GO

INSERT INTO Instructors (Name, Specialization, Organization) VALUES
('Dr. Asha Mehta',    'Soil Management', 'ICAR Hyderabad'),
('Prof. Ramesh Babu', 'Crop Protection', 'Agriculture University'),
('Dr. Sunita Yadav',  'Organic Farming', 'KVK Kurnool'),
('Mr. Kishore Kumar', 'Drip Irrigation', 'State Agri Dept');
GO

INSERT INTO Training (CropID, InstructorID, Date, Location) VALUES
(1, 1, '2025-06-15', 'Community Hall, Anantapur'),
(2, 2, '2025-11-20', 'Panchayat Office, Kurnool'),
(3, 3, '2025-07-10', 'Agriculture Centre, Guntur'),
(4, 4, '2025-12-05', 'Farmers Cooperative, Nellore');
GO

INSERT INTO FarmerTraining (FarmerID, TrainingID) VALUES
(1, 1), (2, 1), (3, 1),
(2, 2), (4, 2),
(1, 3), (3, 3), (5, 3),
(4, 4), (5, 4), (1, 4);
GO

-- Verify all tables
SELECT 'Farmers'       AS [Table], COUNT(*) AS Rows FROM Farmers
UNION ALL
SELECT 'Crops',         COUNT(*) FROM Crops
UNION ALL
SELECT 'Instructors',   COUNT(*) FROM Instructors
UNION ALL
SELECT 'Training',      COUNT(*) FROM Training
UNION ALL
SELECT 'FarmerTraining',COUNT(*) FROM FarmerTraining;
GO
