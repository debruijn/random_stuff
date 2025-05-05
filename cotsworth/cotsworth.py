from datetime import date, timedelta


class IFLDate:

    DAYS_PER_MONTH = 28
    MONTH_NAME_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Sol", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self, year: int, month: int, day: int):
        # TODO: check validity of input
        self.year = year
        self.month = month
        self.day = day

    @staticmethod
    def fromisoformat(date_string: str) -> "IFLDate":
        return IFLDate(*tuple(int(x) for x in date_string.split('-')))

    @staticmethod
    def fromgregoriandate(date_obj: date):
        days_from_start_year = (date_obj - date(date_obj.year - 1, 12, 31)).days
        return IFLDate.fromyearday(date_obj.year, days_from_start_year)

    @staticmethod
    def fromyearday(year, day):
        month, day = divmod(day, IFLDate.DAYS_PER_MONTH)
        if day == 0:
            day = IFLDate.DAYS_PER_MONTH
            month -= 1
        if month + 1 > 6 and IFLDate.year_has_leap_day(year):
            if day > 1:
                if month+1 == 14:
                    return IFLDate(year, 13, 29)
                return IFLDate(year, month+1, day-1)
            if month > 6:
                return IFLDate(year, month, 28)
            else:
                return IFLDate(year, month, 29)
        if month + 1==14:
            return IFLDate(year, 13, 29)
        return IFLDate(year, month+1, day)

    def toyearday(self) -> int:
        return (self.month-1) * IFLDate.DAYS_PER_MONTH + self.day + self.after_leap_day()

    def togregoriandate(self) -> date:
        return date(self.year-1, 12, 31) + timedelta(days=self.toyearday())

    def toisofromat(self) -> str:
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    def pretty_print(self):
        if self.day == 29:
            if self.month == 6:
                return f"Leap Day of {self.year}"
            else:
                return f"Year Day of {self.year}"
        if self.day in [1, 21]:
            return f"{self.day}st of {self.MONTH_NAME_SHORT[self.month-1]}, {self.year}"
        if self.day in [2, 22]:
            return f"{self.day}nd of {self.MONTH_NAME_SHORT[self.month-1]}, {self.year}"
        if self.day in [3, 23]:
            return f"{self.day}rd of {self.MONTH_NAME_SHORT[self.month-1]} {self.year}"
        return f"{self.day}th of {self.MONTH_NAME_SHORT[self.month-1]}, {self.year}"

    def __str__(self) -> str:
        return self.toisofromat()

    def __add__(self, other: timedelta) -> "IFLDate":
        return IFLDate.fromgregoriandate(self.togregoriandate() + other)

    def __sub__(self, other: "timedelta | IFLDate | date") -> "IFLDate | timedelta":
        if type(other) == timedelta:
            return IFLDate.fromgregoriandate(self.togregoriandate() - other)
        elif type(other) == date:
            return self.togregoriandate() - other
        else:
            return self.togregoriandate() - other.togregoriandate()

    @staticmethod
    def year_has_leap_day(year):
        try:
            date(year, 2, 29)
            return True
        except ValueError:
            return False

    def after_leap_day(self):
        if self.month <= 6:
            return False
        return IFLDate.year_has_leap_day(self.year)

    def __eq__(self, other: "IFLDate | date"):
        if type(other) == date:
            return self.togregoriandate() == other
        return self.togregoriandate() == other.togregoriandate()
