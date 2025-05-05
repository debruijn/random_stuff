from datetime import date, timedelta
import pytest
from cotsworth import IFLDate, BetterDate

@pytest.mark.parametrize("ifl_date_str,gregorian_date_str",
                         [("2025-01-01", "2025-01-01"),
                          ("2025-02-01", "2025-01-29"),
                          ("2025-06-01", "2025-05-21"),
                          ("2025-13-01", "2025-12-03"),
                          ("2025-13-29", "2025-12-31"),
                          ("2024-01-01", "2024-01-01"),
                          ("2024-02-01", "2024-01-29"),
                          ("2024-06-01", "2024-05-20"),
                          ("2024-06-29", "2024-06-17"),
                          ("2024-13-01", "2024-12-03"),
                          ("2024-13-29", "2024-12-31")
                          ])
def test_days_conversion(ifl_date_str, gregorian_date_str):
    ifl_date = IFLDate.fromisoformat(ifl_date_str)
    greg_date = date.fromisoformat(gregorian_date_str)

    assert ifl_date.togregoriandate() == greg_date
    assert IFLDate.fromgregoriandate(greg_date) == ifl_date
    assert ifl_date == greg_date

@pytest.mark.parametrize("date1,date2,diff",
                         [("2025-01-01", "2025-01-01", 0),
                          ("2025-01-01", "2025-02-01", 28),
                          ("2023-01-01", "2024-01-01", 365),
                          ("2024-01-01", "2025-01-01", 366),
                          ("2024-06-01", "2024-07-01", 29),
                          ("2025-06-01", "2025-07-01", 28),
                          ("2025-13-01", "2026-01-01", 29),
                          ])
def test_differences(date1, date2, diff):
    date1 = IFLDate.fromisoformat(date1)
    date2 = IFLDate.fromisoformat(date2)
    diff = timedelta(days=diff)
    assert date2 - date1 == diff
    assert date1 + diff == date2


@pytest.mark.parametrize("better_date_str,gregorian_date_str",
                         [("2025-01-01", "2025-01-01"),
                          ("2025-02-01", "2025-01-29"),
                          ("2025-06-01", "2025-05-21"),
                          ("2025-13-01", "2025-12-03"),
                          ("2025-14-01", "2025-12-31"),
                          ("2024-01-01", "2024-01-01"),
                          ("2024-02-01", "2024-01-29"),
                          ("2024-06-01", "2024-05-20"),
                          ("2024-07-01", "2024-06-17"),
                          ("2024-13-01", "2024-12-02"),
                          ("2024-14-02", "2024-12-31")
                          ])
def test_days_conversion_betterdate(better_date_str, gregorian_date_str):
    better_date = BetterDate.fromisoformat(better_date_str)
    greg_date = date.fromisoformat(gregorian_date_str)

    assert better_date.togregoriandate() == greg_date
    assert IFLDate.fromgregoriandate(greg_date) == better_date
    assert better_date == greg_date

@pytest.mark.parametrize("date1,date2,diff",
                         [("2025-01-01", "2025-01-01", 0),
                          ("2025-01-01", "2025-02-01", 28),
                          ("2023-01-01", "2024-01-01", 365),
                          ("2024-01-01", "2025-01-01", 366),
                          ("2024-06-01", "2024-07-01", 28),
                          ("2025-06-01", "2025-07-01", 28),
                          ("2025-13-01", "2026-01-01", 29),
                          ])
def test_differences(date1, date2, diff):
    date1 = BetterDate.fromisoformat(date1)
    date2 = BetterDate.fromisoformat(date2)
    diff = timedelta(days=diff)
    assert date2 - date1 == diff
    assert date1 + diff == date2

