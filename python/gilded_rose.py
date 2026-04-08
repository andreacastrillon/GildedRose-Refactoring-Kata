# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def handle_item_quality_update(self, item, base_quality_degradation_factor):
        item_update_quality = item.quality

        if item.name == "Aged Brie":
            # “Aged Brie” actually increases in Quality the older it gets
            item_update_quality = item_update_quality + 1 * base_quality_degradation_factor
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            # “Backstage passes”, like aged brie, increases in Quality as its SellIn value approaches;
            # Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but Quality drops to 0 after the concert
            # if item.sell_in <= 10 and item.sell_in > 5:
            #     item_update_quality = item_update_quality + 2
            # elif item.sell_in <= 5 and item.sell_in > 0:
            #     item_update_quality = item_update_quality + 3
            # elif item.sell_in <= 0:
            #     item_update_quality = 0
            if item.sell_in <= 0:
                item_update_quality = 0
            else:
                item_update_quality = item_update_quality + 1 * base_quality_degradation_factor

                if item.sell_in <= 10:
                    item_update_quality = item_update_quality + 1 * base_quality_degradation_factor

                if item.sell_in <= 5:
                    item_update_quality = item_update_quality + 1 * base_quality_degradation_factor

        elif item.name != "Sulfuras, Hand of Ragnaros":
            # “Sulfuras”, being a legendary item, never has to be sold or decreases in Quality
            item_update_quality = item_update_quality - 1 * base_quality_degradation_factor

        if item_update_quality > 50 and item.name != "Sulfuras, Hand of Ragnaros":
            # The Quality of an item is never more than 50. Sulfuras never decreases in quality 
            item_update_quality = 50

        if item_update_quality < 0:
            # The Quality of an item is never negative
            item_update_quality = 0
        
        
        return item_update_quality
    
    def update_quality(self):
        for item in self.items:
            
            base_quality_degradation_factor = 1 # 2 in case we are dealing with and item thats past its sell date

            if item.name == "Conjured Mana Cake":
                # "Conjured" items degrade in Quality twice as fast as normal items
                base_quality_degradation_factor = base_quality_degradation_factor * 2

            if item.sell_in <= 0:
                # # Once the sell by date has passed, Quality degrades twice as fast
                base_quality_degradation_factor = base_quality_degradation_factor * 2                    

            if item.name == "Sulfuras, Hand of Ragnaros":
                continue # Sulfuras never decreases in quality and never has to be sold, so we skip the rest of the loop and move on to the next item   

            item_update_quality = self.handle_item_quality_update(item, base_quality_degradation_factor)

            # Finally, assign the potentially updated quality to the item
            item.quality = item_update_quality
            item.sell_in = item.sell_in - 1




class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
