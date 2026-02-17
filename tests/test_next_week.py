import random

import pytest

from python_unit_testing.date_utils import MAX_YEAR, MIN_YEAR, nextWeek

MONTHS_31_EXCEPT_DECEMBER = [1, 3, 5, 7, 8, 10]
MONTHS_30 = [4, 6, 9, 11]


class TestNextWeek:
    class TestValidInput:
        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_30),
                        d := random.randint(1, 21),
                    ),
                    (y, m, d + 7),
                ),
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := 2,
                        d := random.randint(1, 21),
                    ),
                    (y, m, d + 7),
                ),
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := 12,
                        d := random.randint(1, 21),
                    ),
                    (y, m, d + 7),
                ),
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        d := random.randint(1, 21),
                    ),
                    (y, m, d + 7),
                ),
            ],
        )
        def test_day_between_1_and_21(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_30),
                        d := 22,
                    ),
                    (y, m, d + 7),
                ),
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := 12,
                        d := 22,
                    ),
                    (y, m, d + 7),
                ),
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        d := 22,
                    ),
                    (y, m, d + 7),
                ),
            ],
        )
        def test_day_22_m_31_m_30(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        def test_day_22_feb_common_year(self):
            assert nextWeek(2025, 2, 22) == (2025, 3, 1)

        def test_day_22_feb_leap_year(self):
            assert nextWeek(2020, 2, 22) == (2020, 2, 29)

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_30),
                        d := 23,
                    ),
                    (y, m, d + 7),
                ),
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := 12,
                        d := 23,
                    ),
                    (y, m, d + 7),
                ),
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        d := 23,
                    ),
                    (y, m, d + 7),
                ),
            ],
        )
        def test_day_23_m_31_m_30(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        def test_day_23_feb_common_year(self):
            assert nextWeek(2025, 2, 23) == (2025, 3, 2)

        def test_day_23_feb_leap_year(self):
            assert nextWeek(2020, 2, 23) == (2020, 3, 1)

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR - 1),
                        m := 12,
                        d := 24,
                    ),
                    (y, m, d + 7),
                ),
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        d := 24,
                    ),
                    (y, m, d + 7),
                ),
            ],
        )
        def test_day_24_m_31(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_30),
                        24,
                    ),
                    (y, m + 1, 1),
                ),
            ],
        )
        def test_day_24_m_30(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        def test_day_24_feb_common_year(self):
            assert nextWeek(2025, 2, 24) == (2025, 3, 3)

        def test_day_24_feb_leap_year(self):
            assert nextWeek(2020, 2, 24) == (2020, 3, 2)

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        25,
                    ),
                    (y, m + 1, 1),
                ),
            ],
        )
        def test_day_25_m_31_except_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_30),
                        25,
                    ),
                    (y, m + 1, 2),
                ),
            ],
        )
        def test_day_25_m_30(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                ((y := random.randint(MIN_YEAR, MAX_YEAR - 1), 12, 25), (y + 1, 1, 1)),
            ],
        )
        def test_day_25_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        def test_day_25_feb_common_year(self):
            assert nextWeek(2025, 2, 25) == (2025, 3, 4)

        def test_day_25_feb_leap_year(self):
            assert nextWeek(2020, 2, 25) == (2020, 3, 3)

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        26,
                    ),
                    (y, m + 1, 2),
                ),
            ],
        )
        def test_day_26_m_31_except_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_30),
                        26,
                    ),
                    (y, m + 1, 3),
                ),
            ],
        )
        def test_day_26_m_30(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                ((y := random.randint(MIN_YEAR, MAX_YEAR - 1), 12, 26), (y + 1, 1, 2)),
            ],
        )
        def test_day_26_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        def test_day_26_feb_common_year(self):
            assert nextWeek(2025, 2, 26) == (2025, 3, 5)

        def test_day_26_feb_leap_year(self):
            assert nextWeek(2020, 2, 26) == (2020, 3, 4)

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        27,
                    ),
                    (y, m + 1, 3),
                ),
            ],
        )
        def test_day_27_m_31_except_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_30),
                        27,
                    ),
                    (y, m + 1, 4),
                ),
            ],
        )
        def test_day_27_m_30(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                ((y := random.randint(MIN_YEAR, MAX_YEAR - 1), 12, 27), (y + 1, 1, 3)),
            ],
        )
        def test_day_27_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        def test_day_27_feb_common_year(self):
            assert nextWeek(2025, 2, 27) == (2025, 3, 6)

        def test_day_27_feb_leap_year(self):
            assert nextWeek(2020, 2, 27) == (2020, 3, 5)

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        28,
                    ),
                    (y, m + 1, 4),
                ),
            ],
        )
        def test_day_28_m_31_except_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_30),
                        28,
                    ),
                    (y, m + 1, 5),
                ),
            ],
        )
        def test_day_28_m_30(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                ((y := random.randint(MIN_YEAR, MAX_YEAR - 1), 12, 28), (y + 1, 1, 4)),
            ],
        )
        def test_day_28_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        def test_day_28_feb_common_year(self):
            assert nextWeek(2025, 2, 28) == (2025, 3, 7)

        def test_day_28_feb_leap_year(self):
            assert nextWeek(2020, 2, 28) == (2020, 3, 6)

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        29,
                    ),
                    (y, m + 1, 5),
                ),
            ],
        )
        def test_day_29_m_31_except_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_30),
                        29,
                    ),
                    (y, m + 1, 6),
                ),
            ],
        )
        def test_day_29_m_30(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                ((y := random.randint(MIN_YEAR, MAX_YEAR - 1), 12, 29), (y + 1, 1, 5)),
            ],
        )
        def test_day_29_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        def test_day_29_feb_leap_year(self):
            assert nextWeek(2020, 2, 29) == (2020, 3, 7)

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        30,
                    ),
                    (y, m + 1, 6),
                ),
            ],
        )
        def test_day_30_m_31_except_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_30),
                        30,
                    ),
                    (y, m + 1, 7),
                ),
            ],
        )
        def test_day_30_m_30(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                ((y := random.randint(MIN_YEAR, MAX_YEAR - 1), 12, 30), (y + 1, 1, 6)),
            ],
        )
        def test_day_30_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                (
                    (
                        y := random.randint(MIN_YEAR, MAX_YEAR),
                        m := random.choice(MONTHS_31_EXCEPT_DECEMBER),
                        31,
                    ),
                    (y, m + 1, 7),
                ),
            ],
        )
        def test_day_31_m_31_except_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

        @pytest.mark.parametrize(
            "input_date, expected_date",
            [
                ((y := random.randint(MIN_YEAR, MAX_YEAR - 1), 12, 31), (y + 1, 1, 7)),
            ],
        )
        def test_day_31_december(self, input_date, expected_date):
            assert nextWeek(*input_date) == expected_date

    class TestInvalidInput:
        """Test cases for invalid/impossible date combinations from the decision table"""

        def test_feb_29_common_year(self):
            """February 29 in a common (non-leap) year is impossible"""
            with pytest.raises(ValueError):
                nextWeek(2023, 2, 29)  # 2023 is not a leap year

        def test_feb_30_leap_year(self):
            """February 30 in a leap year is impossible"""
            with pytest.raises(ValueError):
                nextWeek(2024, 2, 30)  # Even leap years don't have Feb 30

        def test_feb_30_common_year(self):
            """February 30 in a common year is impossible"""
            with pytest.raises(ValueError):
                nextWeek(2023, 2, 30)

        def test_feb_31_leap_year(self):
            """February 31 in a leap year is impossible"""
            with pytest.raises(ValueError):
                nextWeek(2024, 2, 31)

        def test_feb_31_common_year(self):
            """February 31 in a common year is impossible"""
            with pytest.raises((ValueError, AssertionError)):
                nextWeek(2023, 2, 31)

        @pytest.mark.parametrize(
            "year, month",
            [
                (2024, 4),  # April
                (2024, 6),  # June
                (2024, 9),  # September
                (2024, 11),  # November
            ],
        )
        def test_day_31_in_30_day_months(self, year, month):
            """Day 31 in 30-day months is impossible"""
            with pytest.raises((ValueError, AssertionError)):
                nextWeek(year, month, 31)
