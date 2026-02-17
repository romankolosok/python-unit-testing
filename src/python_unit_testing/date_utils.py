"""
Date utility functions.
"""

MIN_YEAR = 1900
MAX_YEAR = 2100


def _is_leap_year(y: int) -> bool:
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)


def nextDate(year: int, month: int, day: int) -> tuple[int, int, int]:
    """
    Calculate the next date given a year, month, and day.

    Args:
        year: Year (1900-2100)
        month: Month (1-12)
        day: Day of month (1-31, depending on month)

    Returns:
        Tuple of (year, month, day) representing the next date.

    Raises:
        ValueError: If the input date is invalid or out of bounds.
    """
    if year < MIN_YEAR or year > MAX_YEAR:
        raise ValueError(f"Year must be between {MIN_YEAR} and {MAX_YEAR}")

    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if _is_leap_year(year):
        days_in_month[1] = 29
    max_days = days_in_month[month - 1]

    if day < 1 or day > max_days:
        raise ValueError(f"Day must be between 1 and {max_days} for month {month}")

    next_day = day + 1
    next_month = month
    next_year = year

    if next_day > days_in_month[month - 1]:
        next_day = 1
        next_month = month + 1
        if next_month > 12:
            next_month = 1
            next_year = year + 1
            if next_year > MAX_YEAR:
                raise ValueError(
                    f"Cannot calculate next date: year would exceed {MAX_YEAR}"
                )

    return (next_year, next_month, next_day)


def nextWeek(year: int, month: int, day: int) -> tuple[int, int, int]:
    """
    Calculate the date 7 days after the given date.

    Args:
        year: Year (1900-2100)
        month: Month (1-12)
        day: Day of month (1-31, depending on month)

    Returns:
        Tuple of (year, month, day) representing the date one week later.

    Raises:
        ValueError: If the input date is invalid or out of bounds.
    """
    result = (year, month, day)
    for _ in range(7):
        result = nextDate(*result)
    return result
