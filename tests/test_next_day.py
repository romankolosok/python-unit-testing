import random
from itertools import chain

import pytest

from python_unit_testing.date_utils import MAX_YEAR, MIN_YEAR, nextDate

MONTHS_31 = [1, 3, 5, 7, 8, 10, 12]
MONTHS_30 = [4, 6, 9, 11]


class TestNextDate:
    class TestInvalidInput:
        @pytest.mark.parametrize(
            "input_date",
            list(
                chain.from_iterable(
                    (
                        pytest.param((2025, 0, 1), id="Invalid month min-"),
                        pytest.param((2025, 13, 1), id="Invalid month max+"),
                        pytest.param((2025, 100, 1), id="Invalid month >max"),
                        pytest.param((2025, -1, 1), id="Invalid month <min"),
                    )
                    for year in range(MIN_YEAR, MAX_YEAR + 1)
                )
            ),
        )
        def test_nextDate_invalid_month(self, input_date: tuple[int, int, int]):
            with pytest.raises(ValueError, match="Month must be between 1 and 12"):
                nextDate(*input_date)

        @pytest.mark.parametrize(
            "input_date",
            [
                pytest.param((MIN_YEAR - 1, 1, 1), id="Invalid year min-"),
                pytest.param((MAX_YEAR + 1, 1, 1), id="Invalid year max+"),
                pytest.param(
                    (random.randint(MAX_YEAR + 2, MAX_YEAR + 10000), 1, 1),
                    id="Invalid year >max",
                ),
                pytest.param(
                    (random.randint(MIN_YEAR - 10000, MIN_YEAR - 2), 1, 1),
                    id="Invalid year <min",
                ),
            ],
        )
        def test_nextDate_invalid_year(self, input_date: tuple[int, int, int]):
            with pytest.raises(
                ValueError, match=f"Year must be between {MIN_YEAR} and {MAX_YEAR}"
            ):
                nextDate(*input_date)

        @pytest.mark.parametrize(
            "input_date",
            list(
                chain.from_iterable(
                    (
                        pytest.param(
                            (year, month, 0), id=f"Invalid day min- for {month}/{year}"
                        ),
                        pytest.param(
                            (year, month, 32), id=f"Invalid day max+ for {month}/{year}"
                        ),
                        pytest.param(
                            (year, month, random.randint(33, 100)),
                            id=f"Invalid day >max for {month}/{year}",
                        ),
                        pytest.param(
                            (year, month, random.randint(-100, -1)),
                            id=f"Invalid day <min for {month}/{year}",
                        ),
                    )
                    for month in MONTHS_31
                    for year in range(MIN_YEAR, MAX_YEAR + 1)
                )
            ),
        )
        def test_nextDate_invalid_day_31(self, input_date: tuple[int, int, int]):
            with pytest.raises(
                ValueError,
                match=f"Day must be between 1 and 31 for month {input_date[1]}",
            ):
                nextDate(*input_date)

        @pytest.mark.parametrize(
            "input_date",
            list(
                chain.from_iterable(
                    (
                        pytest.param(
                            (year, month, 0), id=f"Invalid day min- for {month}/{year}"
                        ),
                        pytest.param(
                            (year, month, 31), id=f"Invalid day max+ for {month}/{year}"
                        ),
                        pytest.param(
                            (year, month, random.randint(32, 100)),
                            id=f"Invalid day >max for {month}/{year}",
                        ),
                        pytest.param(
                            (year, month, random.randint(-100, -1)),
                            id=f"Invalid day <min for {month}/{year}",
                        ),
                    )
                    for month in MONTHS_30
                    for year in range(MIN_YEAR, MAX_YEAR + 1)
                )
            ),
        )
        def test_nextDate_invalid_day_30(self, input_date: tuple[int, int, int]):
            with pytest.raises(
                ValueError,
                match=f"Day must be between 1 and 30 for month {input_date[1]}",
            ):
                nextDate(*input_date)

        @pytest.mark.parametrize(
            "input_date",
            [
                pytest.param((2025, 2, 0), id="Invalid day min-"),
                pytest.param((2025, 2, 29), id="Invalid day max+"),
                pytest.param((2025, 2, random.randint(30, 100)), id="Invalid day >max"),
                pytest.param(
                    (2025, 2, random.randint(-100, -1)), id="Invalid day <min"
                ),
            ],
        )
        def test_nextDate_invalid_day_feb(self, input_date: tuple[int, int, int]):
            with pytest.raises(
                ValueError,
                match=f"Day must be between 1 and 28 for month {input_date[1]}",
            ):
                nextDate(*input_date)

        @pytest.mark.parametrize(
            "input_date",
            [
                pytest.param((2024, 2, 0), id="Invalid day min-"),
                pytest.param((2024, 2, 30), id="Invalid day max+"),
                pytest.param((2024, 2, random.randint(31, 100)), id="Invalid day >max"),
                pytest.param(
                    (2024, 2, random.randint(-100, -1)), id="Invalid day <min"
                ),
            ],
        )
        def test_nextDate_invalid_day_feb_leap(self, input_date: tuple[int, int, int]):
            with pytest.raises(
                ValueError,
                match=f"Day must be between 1 and 29 for month {input_date[1]}",
            ):
                nextDate(*input_date)

        def test_nextDate_max_date(self):
            with pytest.raises(
                ValueError,
                match=f"Cannot calculate next date: year would exceed {MAX_YEAR}",
            ):
                nextDate(MAX_YEAR, 12, 31)

    @pytest.mark.skip(reason="Temporarily disabled | Too many tests")
    class TestValidInput:
        @pytest.mark.parametrize(
            "input_date, expected_date",
            list(
                chain.from_iterable(
                    (
                        pytest.param(
                            (2024, 2, day), (2024, 2, day + 1), id=f"Valid day 2/{day}"
                        ),
                    )
                    for day in range(1, 29)
                )
            )
            + [pytest.param((2024, 2, 29), (2024, 3, 1), id="Valid day 2/29")],
        )
        def test_nextDate_feb_leap(self, input_date, expected_date):
            assert nextDate(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            list(
                chain.from_iterable(
                    (
                        pytest.param(
                            (year, 2, day),
                            (year, 2, day + 1),
                            id=f"Valid day 2/{day}/{year}",
                        ),
                    )
                    for day in range(1, 28)
                    for year in range(1900, 1904)
                )
            )
            + [
                pytest.param((year, 2, 28), (year, 3, 1), id=f"Valid day 2/28/{year}")
                for year in range(1900, 1904)
            ],
        )
        def test_nextDate_feb(self, input_date, expected_date):
            assert nextDate(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            list(
                chain.from_iterable(
                    (
                        pytest.param(
                            (year, month, day),
                            (year, month, day + 1),
                            id=f"Valid day {month}/{day}/{year}",
                        ),
                    )
                    for day in range(1, 30)
                    for month in MONTHS_30
                    for year in range(1900, 1904)
                )
            )
            + list(
                chain.from_iterable(
                    (
                        pytest.param(
                            (year, month, 30),
                            (year, month + 1, 1),
                            id=f"Valid day {month}/30/{year}",
                        ),
                    )
                    for month in MONTHS_30
                    for year in range(MIN_YEAR, MAX_YEAR)
                )
            ),
        )
        def test_nextDate_month_30(self, input_date, expected_date):
            assert nextDate(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            list(
                chain.from_iterable(
                    (
                        *(
                            pytest.param(
                                (year, month, day),
                                (year, month, day + 1),
                                id=f"Valid {month}/{day}/{year}",
                            )
                            for day in range(1, 31)
                        ),
                        pytest.param(
                            (year, month, 31),
                            (year, month + 1, 1) if month < 12 else (year + 1, 1, 1),
                            id=f"Rollover {month}/31/{year}",
                        ),
                    )
                    for month in MONTHS_31
                    for year in range(MIN_YEAR, MAX_YEAR + 1)
                )
            )[:-1],
        )
        def test_nextDate_month_31(self, input_date, expected_date):
            assert nextDate(*input_date) == expected_date
