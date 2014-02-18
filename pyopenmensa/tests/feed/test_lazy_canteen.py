# -*- coding: UTF-8 -*-
import pytest
from datetime import date

from pyopenmensa.feed import LazyBuilder


@pytest.fixture
def canteen():
    return LazyBuilder()


def test_date_converting(canteen):
    day = date(2013, 3, 7)
    assert canteen.dayCount() == 0
    canteen.setDayClosed('2013-03-07')
    assert canteen.dayCount() == 1
    canteen.setDayClosed(day)
    assert canteen.dayCount() == 1
    canteen.setDayClosed('07.03.2013')
    assert canteen.dayCount() == 1


def test_has_meals_for(canteen):
    day = date(2013, 3, 7)
    assert canteen.hasMealsFor(day) is False
    canteen._days[day] = {'Hausgericht': ('Gulash', [], {})}
    assert canteen.hasMealsFor(day) is True
    canteen.setDayClosed(day)
    assert canteen.hasMealsFor(day) is False


def test_add_meal(canteen):
    day = date(2013, 3, 7)
    canteen.addMeal(day, 'Hauptgericht', 'Gulasch')
    assert canteen.hasMealsFor(day)


def test_to_long_meal_name(canteen):
    day = date(2013, 3, 7)
    canteen.addMeal(day, 'Hauptgericht', 'Y'*251)
    canteen.hasMealsFor(day)


def test_caseinsensitive_notes(canteen):
    day = date(2013, 3, 7)
    canteen.legendKeyFunc = lambda v: v.lower()
    canteen.setLegendData(legend={'f': 'Note'})
    canteen.addMeal(day, 'Test', 'Essen(F)')
    assert canteen._days[day]['Test'][0] == ('Essen', ['Note'], {})
