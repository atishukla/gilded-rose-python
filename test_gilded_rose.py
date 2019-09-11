# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


def get_gilded_rose(items):
    gilded_rose = GildedRose(items)
    return gilded_rose


class GildedRoseTest(unittest.TestCase):

    def setUp(self):
        self.items = []

    def test_regular_item_decrease_by_one(self):
        self.items.append(Item(name="+5 Dexterity Vest", sell_in=10, quality=20))
        get_gilded_rose(self.items).update_quality()
        item = self.items[0]

        expected = [
            {'sell_in': 9, 'quality': 19}
        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    def test_repr_string_for_coverage(self):
        self.items.append(Item(name="+5 Dexterity Vest", sell_in=10, quality=20))
        result = get_gilded_rose(self.items)
        reprs = result.__repr__
        self.assertTrue(result)
        self.assertIsNotNone(reprs)

    def test_quality_degrades_twice_when_SellIn_date_passes(self):
        self.items.append(Item(name="Elixir of the Mongoose", sell_in=-1, quality=7))
        # Not sure about this condition but since it is like this lets keep it
        self.items.append(
            Item(name="Aged Brie", sell_in=-1, quality=0))
        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': -2, 'quality': 5},
            {'sell_in': -2, 'quality': 0},
        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    def test_quality_increases_for_certain_items(self):
        self.items.append(Item(name="Aged Brie", sell_in=20, quality=30))
        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=20, quality=30))
        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': 19, 'quality': 31},
            {'sell_in': 19, 'quality': 31}
        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    def test_quality_of_an_item_is_never_negative(self):
        self.items.append(Item(name="Elixir of the Mongoose", sell_in=5, quality=0))
        self.items.append(Item(name="+5 Dexterity Vest", sell_in=10, quality=0))
        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': 4, 'quality': 0},
            {'sell_in': 9, 'quality': 0}
        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    def test_sulfras_legendary_never_sold_or_decrease_in_quality(self):
        self.items.append(Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=45))
        self.items.append(Item(name="Sulfuras, Hand of Ragnaros", sell_in=5, quality=80))
        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': 0, 'quality': 45},
            {'sell_in': 5, 'quality': 80}
        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    def test_quality_increases_by_two_with_ten_days_or_less_for_backstage(self):
        # boundary case 10 days
        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=11, quality=22))
        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20))
        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=9, quality=24))
        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': 10, 'quality': 23},
            {'sell_in': 9, 'quality': 22},
            {'sell_in': 8, 'quality': 26}
        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    def test_quality_increases_by_three_with_five_days_or_less_for_backstage(self):

        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=22))
        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=6, quality=20))
        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=4, quality=24))
        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': 4, 'quality': 25},
            {'sell_in': 5, 'quality': 22},
            {'sell_in': 3, 'quality': 27},
        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    def test_quality_becomes_zero_after_the_concert_for_backstage(self):
        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=22))

        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': -1, 'quality': 0}
        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    def test_quality_never_exceeds_fifty(self):
        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49))
        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49))
        self.items.append(
            Item(name="Aged Brie", sell_in=-1, quality=49))
        self.items.append(
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=50))

        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': 9, 'quality': 50},
            {'sell_in': 4, 'quality': 50},
            {'sell_in': -2, 'quality': 50},
            {'sell_in': 9, 'quality': 50}
        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    def test_sulfaras_quality_is_eighty_and_never_decrease(self):
        self.items.append(
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=10, quality=80))
        self.items.append(
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=1, quality=80))

        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': 10, 'quality': 80},
            {'sell_in': 1, 'quality': 80}

        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    # Conjured Item test

    @unittest.skip
    def test_conjured_item_decrease_quality_twice_as_fast_as_normal(self):
        self.items.append(
            Item(name="Conjured Mana Cake", sell_in=3, quality=6))
        self.items.append(
            Item(name="+5 Dexterity Vest", sell_in=3, quality=6))

        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': 2, 'quality': 4},
            {'sell_in': 2, 'quality': 5}

        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    @unittest.skip
    def test_conjured_item_quality_never_negative(self):
        self.items.append(
            Item(name="Conjured Mana Cake", sell_in=0, quality=0))

        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': -1, 'quality': 0}

        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])

    @unittest.skip
    def test_conjured_item_quality_decrease_four_times_after_sellin(self):
        self.items.append(
            Item(name="Conjured Mana Cake", sell_in=0, quality=10))

        get_gilded_rose(self.items).update_quality()

        expected = [
            {'sell_in': -1, 'quality': 6}
        ]

        for index, expectation in enumerate(expected):
            item = self.items[index]
            self.assertEqual(item.quality, expectation['quality'])
            self.assertEqual(item.sell_in, expectation['sell_in'])


if __name__ == '__main__':
    unittest.main()
