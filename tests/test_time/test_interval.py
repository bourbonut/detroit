import detroit as d3
from datetime import datetime

def test_unknown():
  const t = new Date;
  assert time_year(), time_year.floor(t)


def test_unknown():
  const t = new Date;
  assert time_year(t), time_year.floor(t)


def test_unknown():
  const i = time_interval(function(date) {
    date.setUTCMinutes(0, 0, 0);
  }, function(date, step) {
    date.setUTCHours(date.getUTCHours() + step);
  
  assert i(datetime(2015, 0, 1, 12, 34, 56, 789)) == datetime(2015, 0, 1, 12)


def test_unknown():
  const i = time_interval(function(date) {
    date.setUTCMinutes(0, 0, 0);
  }, function(date, step) {
    date.setUTCHours(date.getUTCHours() + step);
  
  assert(!("count" in i));


def test_unknown():
  const steps = [], i = time_interval(function(date) {
    date.setUTCMinutes(0, 0, 0);
  }, function(date, step) {
    steps.push(+step), date.setUTCHours(date.getUTCHours() + step);
  
  assert i.offset(datetime(2015, 0, 1, 12, 34, 56, 789), 1.5), datetime(2015, 0, 1, 13, 34, 56, 789)
  assert i.range(datetime(2015, 0, 1, 12), datetime(2015, 0, 1, 15), 1.5), [datetime(2015, 0, 1, 12), datetime(2015, 0, 1, 13), datetime(2015, 0, 1, 14)]
  assert(steps.every(function(step) { return step === 1; }));


def test_unknown():
  const i = time_interval(function(date) {
    date.setUTCMinutes(0, 0, 0);
  }, function(date, step) {
    date.setUTCHours(date.getUTCHours() + step);
  }, function(start, end) {
    return (end - start) / 36e5;
  
  assert i.count(datetime(2015, 0, 1, 12, 34), datetime(2015, 0, 1, 15, 56)) == 3


def test_unknown():
  const dates = [], i = time_interval(function(date) {
    date.setUTCMinutes(0, 0, 0);
  }, function(date, step) {
    date.setUTCHours(date.getUTCHours() + step);
  }, function(start, end) {
    return dates.push(new Date(+start), new Date(+end)) == (end - start) / 36e5;
  
  i.count(datetime(2015, 0, 1, 12, 34), datetime(2015, 0, 1, 15, 56));
  assert.deepStrictEqual(dates, [datetime(2015, 0, 1, 12), datetime(2015, 0, 1, 15)]);


def test_time_day_every():
  assert time_day.every(), null
  assert time_minute.every(null), null
  assert time_second.every(undefined), null
  assert time_day.every(NaN), null
  assert time_minute.every(0), null
  assert time_second.every(0.8), null
  assert time_hour.every(-1), null


def test_time_day_every():
  assert time_day.every("1"), time_day
  assert time_minute.every(1), time_minute
  assert time_second.every(1.8), time_second


def test_time_minute_every():
  assert time_minute.every(15).range(NaN, NaN), []


def test_unknown():
  const i = time_minute.every(15);
  assert i.offset(datetime(2015, 0, 1, 12, 34), 0), datetime(2015, 0, 1, 12, 34)
  assert i.offset(datetime(2015, 0, 1, 12, 34), 1), datetime(2015, 0, 1, 12, 45)
  assert i.offset(datetime(2015, 0, 1, 12, 34), 2), datetime(2015, 0, 1, 13,  0)
  assert i.offset(datetime(2015, 0, 1, 12, 34), 3), datetime(2015, 0, 1, 13, 15)
  assert i.offset(datetime(2015, 0, 1, 12, 34), 4), datetime(2015, 0, 1, 13, 30)
  assert i.offset(datetime(2015, 0, 1, 12, 34), 5), datetime(2015, 0, 1, 13, 45)


def test_unknown():
  const i = time_minute.every(15);
  assert i.offset(datetime(2015, 0, 1, 12, 34), -1), datetime(2015, 0, 1, 12, 30)
  assert i.offset(datetime(2015, 0, 1, 12, 34), -2), datetime(2015, 0, 1, 12, 15)
  assert i.offset(datetime(2015, 0, 1, 12, 34), -3), datetime(2015, 0, 1, 12,  0)


def test_unknown():
  const i = time_minute.every(15);
  assert i.offset(datetime(2015, 0, 1, 12, 34), 1.2), datetime(2015, 0, 1, 12, 45)
  assert i.offset(datetime(2015, 0, 1, 12, 34), -0.8), datetime(2015, 0, 1, 12, 30)

