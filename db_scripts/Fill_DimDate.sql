SET NOCOUNT ON

TRUNCATE TABLE DIM_Date

DECLARE @CurrentDate DATE = '1750-01-01'
DECLARE @EndDate DATE = '2025-12-31'

WHILE @CurrentDate < @EndDate
BEGIN
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
    Select 
      DATE = @CurrentDate,
      Day = DAY(@CurrentDate),
      [DayOfYear] = DATENAME(dy, @CurrentDate),
      WEEKDAY = DATEPART(dw, @CurrentDate),
      WeekDayName = DATENAME(dw, @CurrentDate),
      [Month] = MONTH(@CurrentDate),
      [MonthName] = DATENAME(mm, @CurrentDate),
      [Year] = YEAR(@CurrentDate),

   SET @CurrentDate = DATEADD(DD, 1, @CurrentDate)
END