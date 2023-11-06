-- Create the DimDate table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'DimDate')
BEGIN
    CREATE TABLE DimDate (
        fullDate DATE PRIMARY KEY,
        dayOfMonth INT,
        dayOfYear INT,
        dayOfWeek INT,
        dayName VARCHAR(10),
        monthNumber INT,
        monthName VARCHAR(10),
        year INT
    );

    -- Add a unique constraint on the fullDate column
    ALTER TABLE DimDate
    ADD CONSTRAINT UC_DimDate_FullDate UNIQUE (fullDate);
END

-- Populate the DimDate table with dates from January 1, 1930, to January 1, 2025
DECLARE @StartDate DATE = '1930-01-01';
DECLARE @EndDate DATE = '2025-01-01';

WHILE @StartDate < @EndDate
BEGIN
    INSERT INTO DimDate (fullDate, dayOfMonth, dayOfYear, dayOfWeek, dayName, monthNumber, monthName, year)
    VALUES (
        @StartDate,
        DATEPART(DAY, @StartDate),
        DATEPART(DAYOFYEAR, @StartDate),
        DATEPART(WEEKDAY, @StartDate),
        DATENAME(DW, @StartDate),
        DATEPART(MONTH, @StartDate),
        DATENAME(MONTH, @StartDate),
        DATEPART(YEAR, @StartDate)
    );

    SET @StartDate = DATEADD(DAY, 1, @StartDate);
END
