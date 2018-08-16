import unittest
from datetime import datetime, timedelta
from random import randint

from timewreport.interval import TimeWarriorInterval

import tests.testsupport as tests
from billwarrior.invoice import Invoice, ItemCategory, LineItem
from billwarrior.tag import Tag


class InvoiceTest(unittest.TestCase):
    def test_categories_should_return_list_of_tags(self):
        a, b, c = (
            tests.give_interval(tags=["meeting"]),
            tests.give_interval(tags=["pingpong"]),
            tests.give_interval(tags=["coding"]),
        )

        invoice = Invoice([a, b, c])
        categories = invoice.categories()

        self.assertCountEqual(["meeting", "pingpong", "coding"], categories)


class ItemCategoryTest(unittest.TestCase):
    def test_header_should_display_formatted_tag_as_category_string(self):
        tag = Tag('arbitrary tag name ', [])
        category = ItemCategory(tag)
        self.assertEqual(category.header, tag.name.strip().capitalize())


class LineItemTest(unittest.TestCase):
    def test_date_should_display_month_day_year_correctly_in_latex(self):
        day = datetime.today()
        line_item = LineItem(day, None, None)

        self.assertEqual(line_item.date, day.strftime("%B %d, %Y"))

    def test_duration_should_display_decimal_value_of_hours_worked(self):
        duration = timedelta(
            hours=randint(0, 8), minutes=randint(0, 59), seconds=randint(0, 59)
        )
        line_item = LineItem(datetime.today(), duration, None)

        totsec = duration.total_seconds()
        total = (
            totsec // 3600
            + (((totsec % 3600) // 60) / 60)
            + (((totsec % 3600) % 60) / 6000)
        )

        self.assertEqual(line_item.duration, "{:.2f}".format(total))

    def test_unit_price_should_be_displayed_as_is(self):
        unit_price = randint(0, 200) + randint(0, 99) * 0.1
        line_item = LineItem(datetime.today(), timedelta(), unit_price)

        self.assertEqual(line_item.unit_price, "{:.2f}".format(unit_price))

    def test_str_should_display_full_line_item_as_latex_output(self):
        line_item = LineItem(
            datetime.today(),
            timedelta(0, randint(0, 8) * 3600),
            randint(0, 200) + randint(0, 99) * 0.1,
        )

        self.assertEqual(
            line_item.__str__(),
            "\\hourrow{%s}{%s}{%s}"
            % (line_item.date, line_item.duration, line_item.unit_price),
        )
