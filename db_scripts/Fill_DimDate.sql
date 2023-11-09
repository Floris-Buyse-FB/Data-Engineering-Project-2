-- Insert into DimDate table
INSERT INTO DimDate (
    fullDate,
    dayOfMonth,
    dayOfYear,
    dayOfWeek,
    dayName,
    monthNumber,
    monthName,
    year
)
SELECT
    currentDate AS fullDate,
    DAY(currentDate) AS dayOfMonth,
    DATEPART(DAYOFYEAR, currentDate) AS dayOfYear,
    DATEPART(WEEKDAY, currentDate) AS dayOfWeek,
    DATENAME(WEEKDAY, currentDate) AS dayName,
    MONTH(currentDate) AS monthNumber,
    DATENAME(MONTH, currentDate) AS monthName,
    YEAR(currentDate) AS year
FROM (
    SELECT DATEADD(DAY, number - 1, CAST('1750-01-01' AS DATE)) AS currentDate
    FROM master.dbo.spt_values
    WHERE type = 'P' AND number BETWEEN 1 AND DATEDIFF(DAY, '1750-01-01', '2026-01-01')
) AS DateSequence;
