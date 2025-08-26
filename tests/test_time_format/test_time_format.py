from datetime import datetime

import detroit as d3


def test_time_format_coerce():
    f = d3.time_format("%c")
    assert f(datetime(1990, 1, 1)) == "Mon Jan  1 00:00:00 1990"
    assert f(datetime(1990, 1, 2)) == "Tue Jan  2 00:00:00 1990"
    assert f(datetime(1990, 1, 3)) == "Wed Jan  3 00:00:00 1990"
    assert f(datetime(1990, 1, 4)) == "Thu Jan  4 00:00:00 1990"
    assert f(datetime(1990, 1, 5)) == "Fri Jan  5 00:00:00 1990"
    assert f(datetime(1990, 1, 6)) == "Sat Jan  6 00:00:00 1990"
    assert f(datetime(1990, 1, 7)) == "Sun Jan  7 00:00:00 1990"


def test_time_format_abbreviated_weekdays():
    f = d3.time_format("%a")
    assert f(datetime(1990, 1, 1)) == "Mon"
    assert f(datetime(1990, 1, 2)) == "Tue"
    assert f(datetime(1990, 1, 3)) == "Wed"
    assert f(datetime(1990, 1, 4)) == "Thu"
    assert f(datetime(1990, 1, 5)) == "Fri"
    assert f(datetime(1990, 1, 6)) == "Sat"
    assert f(datetime(1990, 1, 7)) == "Sun"


def test_time_format_weekday():
    f = d3.time_format("%A")
    assert f(datetime(1990, 1, 1)) == "Monday"
    assert f(datetime(1990, 1, 2)) == "Tuesday"
    assert f(datetime(1990, 1, 3)) == "Wednesday"
    assert f(datetime(1990, 1, 4)) == "Thursday"
    assert f(datetime(1990, 1, 5)) == "Friday"
    assert f(datetime(1990, 1, 6)) == "Saturday"
    assert f(datetime(1990, 1, 7)) == "Sunday"


def test_time_format_abbreviated_months():
    f = d3.time_format("%b")
    assert f(datetime(1990, 1, 1)) == "Jan"
    assert f(datetime(1990, 2, 1)) == "Feb"
    assert f(datetime(1990, 3, 1)) == "Mar"
    assert f(datetime(1990, 4, 1)) == "Apr"
    assert f(datetime(1990, 5, 1)) == "May"
    assert f(datetime(1990, 6, 1)) == "Jun"
    assert f(datetime(1990, 7, 1)) == "Jul"
    assert f(datetime(1990, 8, 1)) == "Aug"
    assert f(datetime(1990, 9, 1)) == "Sep"
    assert f(datetime(1990, 10, 1)) == "Oct"
    assert f(datetime(1990, 11, 1)) == "Nov"
    assert f(datetime(1990, 12, 1)) == "Dec"


def test_time_format_months():
    f = d3.time_format("%B")
    assert f(datetime(1990, 1, 1)) == "January"
    assert f(datetime(1990, 2, 1)) == "February"
    assert f(datetime(1990, 3, 1)) == "March"
    assert f(datetime(1990, 4, 1)) == "April"
    assert f(datetime(1990, 5, 1)) == "May"
    assert f(datetime(1990, 6, 1)) == "June"
    assert f(datetime(1990, 7, 1)) == "July"
    assert f(datetime(1990, 8, 1)) == "August"
    assert f(datetime(1990, 9, 1)) == "September"
    assert f(datetime(1990, 10, 1)) == "October"
    assert f(datetime(1990, 11, 1)) == "November"
    assert f(datetime(1990, 12, 1)) == "December"


def test_time_format_zero_pad():
    f = d3.time_format("%d")
    assert f(datetime(1990, 1, 1)) == "01"


def test_time_format_space_pad():
    f = d3.time_format("%e")
    assert f(datetime(1990, 1, 1)) == " 1"


def test_time_format_two_digit_year():
    f = d3.time_format("%g")
    assert f(datetime(2018, 12, 30, 0)) == "18"  # Sunday
    assert f(datetime(2018, 12, 31, 0)) == "19"  # Monday
    assert f(datetime(2019, 1, 1, 0)) == "19"


def test_time_format_four_digit_year():
    f = d3.time_format("%G")
    assert f(datetime(2018, 12, 30, 0)) == "2018"  # Sunday
    assert f(datetime(2018, 12, 31, 0)) == "2019"  # Monday
    assert f(datetime(2019, 1, 1, 0)) == "2019"


def test_time_format_hour_24h():
    f = d3.time_format("%H")
    assert f(datetime(1990, 1, 1, 0)) == "00"
    assert f(datetime(1990, 1, 1, 13)) == "13"


def test_time_format_hour_12h():
    f = d3.time_format("%I")
    assert f(datetime(1990, 1, 1, 0)) == "12"
    assert f(datetime(1990, 1, 1, 13)) == "01"


def test_time_format_year_number():
    f = d3.time_format("%j")
    assert f(datetime(1990, 1, 1)) == "001"
    assert f(datetime(1990, 6, 1)) == "152"
    assert f(datetime(2010, 3, 13)) == "072"
    assert f(datetime(2010, 3, 14)) == "073"  # DST begins
    assert f(datetime(2010, 3, 15)) == "074"
    assert f(datetime(2010, 11, 6)) == "310"
    assert f(datetime(2010, 11, 7)) == "311"  # DST ends
    assert f(datetime(2010, 11, 8)) == "312"


def test_time_format_months_number():
    f = d3.time_format("%m")
    assert f(datetime(1990, 1, 1)) == "01"
    assert f(datetime(1990, 10, 1)) == "10"


def test_time_format_minute_number():
    f = d3.time_format("%M")
    assert f(datetime(1990, 1, 1, 0, 0)) == "00"
    assert f(datetime(1990, 1, 1, 0, 32)) == "32"


def test_time_format_AM_PM():
    f = d3.time_format("%p")
    assert f(datetime(1990, 1, 1, 0)) == "AM"
    assert f(datetime(1990, 1, 1, 13)) == "PM"

    def test_time_format_quarter():
        f = d3.time_format("%q")
        assert f(datetime(1990, 1, 1)) == "1"
        assert f(datetime(1990, 4, 1)) == "2"
        assert f(datetime(1990, 7, 1)) == "3"
        assert f(datetime(1990, 10, 1)) == "4"


def test_time_format_seconds():
    f = d3.time_format("%S")
    assert f(datetime(1990, 1, 1, 0, 0, 0)) == "00"
    assert f(datetime(1990, 1, 1, 0, 0, 32)) == "32"
    f2 = d3.time_format("%0S")
    assert f2(datetime(1990, 1, 1, 0, 0, 0)) == "00"
    assert f2(datetime(1990, 1, 1, 0, 0, 32)) == "32"


def test_time_format_pad_seconds():
    f = d3.time_format("%_S")
    assert f(datetime(1990, 1, 1, 0, 0, 0)) == " 0"
    assert f(datetime(1990, 1, 1, 0, 0, 3)) == " 3"
    assert f(datetime(1990, 1, 1, 0, 0, 32)) == "32"


def test_time_format_no_pad_seconds():
    f = d3.time_format("%-S")
    assert f(datetime(1990, 1, 1, 0, 0, 0)) == "0"
    assert f(datetime(1990, 1, 1, 0, 0, 3)) == "3"
    assert f(datetime(1990, 1, 1, 0, 0, 32)) == "32"


def test_time_format_week_numbers():
    f = d3.time_format("%u")
    assert f(datetime(1990, 1, 1, 0)) == "1"
    assert f(datetime(1990, 1, 7, 0)) == "7"
    assert f(datetime(2010, 3, 13, 23)) == "6"


def test_time_format_zero_pad_seconds():
    f = d3.time_format("%S")
    assert f(datetime(1990, 1, 1, 0, 0, 0)) == "00"
    assert f(datetime(1990, 1, 1, 0, 0, 32)) == "32"
    f2 = d3.time_format("%0S")
    assert f2(datetime(1990, 1, 1, 0, 0, 0)) == "00"
    assert f2(datetime(1990, 1, 1, 0, 0, 32)) == "32"


def test_time_format_space_pad_seconds():
    f = d3.time_format("%_S")
    assert f(datetime(1990, 1, 1, 0, 0, 0)) == " 0"
    assert f(datetime(1990, 1, 1, 0, 0, 3)) == " 3"
    assert f(datetime(1990, 1, 1, 0, 0, 32)) == "32"


def test_time_format_no_pad_seconds_2():
    f = d3.time_format("%-S")
    assert f(datetime(1990, 1, 1, 0, 0, 0)) == "0"
    assert f(datetime(1990, 1, 1, 0, 0, 3)) == "3"
    assert f(datetime(1990, 1, 1, 0, 0, 32)) == "32"


def test_time_format_week_day_number():
    f = d3.time_format("%u")
    assert f(datetime(1990, 1, 1, 0)) == "1"
    assert f(datetime(1990, 1, 7, 0)) == "7"
    assert f(datetime(2010, 3, 13, 23)) == "6"


def test_time_format_microseconds():
    f = d3.time_format("%f")
    assert f(datetime(1990, 1, 1, 0, 0, 0, 0)) == "000000"
    assert f(datetime(1990, 1, 1, 0, 0, 0, 432)) == "000432"


def test_time_format_zero_pad_week_day_number():
    f = d3.time_format("%U")
    assert f(datetime(1990, 1, 1, 0)) == "00"
    assert f(datetime(1990, 6, 1, 0)) == "21"
    assert f(datetime(2010, 3, 13, 23)) == "10"
    assert f(datetime(2010, 3, 14, 0)) == "11"  # DST begins
    assert f(datetime(2010, 3, 15, 0)) == "11"
    assert f(datetime(2010, 11, 6, 23)) == "44"
    assert f(datetime(2010, 11, 7, 0)) == "45"  # DST ends
    assert f(datetime(2010, 11, 8, 0)) == "45"
    assert f(datetime(2012, 1, 1, 0)) == "01"  # Sunday


def test_time_format_zero_pad_week_number():
    f = d3.time_format("%W")
    assert f(datetime(1990, 1, 1, 0)) == "01"  # Monday
    assert f(datetime(1990, 6, 1, 0)) == "22"
    assert f(datetime(2010, 3, 15, 0)) == "11"
    assert f(datetime(2010, 11, 8, 0)) == "45"


def test_time_format_week_numbers_2():
    f = d3.time_format("%V")
    assert f(datetime(1990, 1, 1, 0)) == "01"
    assert f(datetime(1990, 6, 1, 0)) == "22"
    assert f(datetime(2010, 3, 13, 23)) == "10"
    assert f(datetime(2010, 3, 14, 0)) == "10"  # DST begins
    assert f(datetime(2010, 3, 15, 0)) == "11"
    assert f(datetime(2010, 11, 6, 23)) == "44"
    assert f(datetime(2010, 11, 7, 0)) == "44"  # DST ends
    assert f(datetime(2010, 11, 8, 0)) == "45"
    assert f(datetime(2015, 12, 31, 0)) == "53"
    assert f(datetime(2016, 1, 1, 0)) == "53"


def test_time_format_localized_date():
    f = d3.time_format("%x")
    assert f(datetime(1990, 1, 1)) == "01/01/90"
    assert f(datetime(2010, 6, 1)) == "06/01/10"


def test_time_format_localized_time():
    f = d3.time_format("%X")
    assert f(datetime(1990, 1, 1, 12, 0, 0)) == "12:00:00"
    assert f(datetime(1990, 1, 1, 13, 34, 59)) == "13:34:59"


def test_time_format_two_digit_year_v2():
    f = d3.time_format("%y")
    assert f(datetime(1990, 1, 1)) == "90"
    assert f(datetime(2002, 1, 1)) == "02"


def test_time_format_four_digit_year_v2():
    f = d3.time_format("%Y")
    assert f(datetime(123, 1, 1)) == "123"
    assert f(datetime(1990, 1, 1)) == "1990"
    assert f(datetime(2002, 1, 1)) == "2002"


def test_time_format_time_zone():
    f = d3.time_format("%Z")
    assert f(datetime(1990, 1, 1)) == ""


def test_time_format_percentage():
    f = d3.time_format("%%")
    assert f(datetime(1990, 1, 1)) == "%"


# def test_time_format_multiples():
#     assert multi(datetime(1990, 0, 1, 0, 0, 0, 12)) == ".012"
#     assert multi(datetime(1990, 0, 1, 0, 0, 1,  0)) == ":01"
#     assert multi(datetime(1990, 0, 1, 0, 1, 0,  0)) == "12:01"
#     assert multi(datetime(1990, 0, 1, 1, 0, 0,  0)) == "01 AM"
#     assert multi(datetime(1990, 0, 2, 0, 0, 0,  0)) == "Tue 02"
#     assert multi(datetime(1990, 1, 1, 0, 0, 0,  0)) == "February"
#     assert multi(datetime(1990, 0, 1, 0, 0, 0,  0)) == "1990"
