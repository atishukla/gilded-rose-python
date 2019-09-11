# -*- coding: utf-8 -*-


class GildedRose(object):

    aged_brie = "Aged Brie"
    backstage = "Backstage passes to a TAFKAL80ETC concert"
    sulfuras = "Sulfuras, Hand of Ragnaros"

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            # Code updating only sell_in
            self.update_sell_in(item)

            if item.name != self.aged_brie and item.name != self.backstage:
                if item.name != self.sulfuras:
                    self.update_item_quality(item, -1)
            else:

                # Replacing this is distorting the identation for if statement
                self.update_item_quality(item, 1)
                if item.name == self.backstage:
                    if item.sell_in < 11:
                        self.update_item_quality(item, 1)
                    if item.sell_in < 6:
                        self.update_item_quality(item, 1)

            if item.sell_in < 0:
                if item.name == self.aged_brie:
                    self.update_item_quality(item, 1)
                elif item.name == self.backstage:
                    self.update_item_quality(item, -item.quality)
                elif item.name == self.sulfuras:
                    pass

                else:
                    self.update_item_quality(item, -1)

    def update_item_quality(self, item, quality_delta):
        if item.quality < 50 and item.quality > 0:
            item.quality += quality_delta

    def update_sell_in(self, item):
        if item.name != self.sulfuras:
            item.sell_in -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
