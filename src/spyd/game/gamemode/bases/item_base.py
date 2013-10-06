from spyd.protocol import swh
from cube2common.constants import item_types
from spyd.game.map.item import Item, UnusedItemSlot

class ItemBase(object):
    def __init__(self, room, map_meta_data):
        self.room = room
        
        self.items = None

        if map_meta_data is not None:
            item_list = []
            for ent in map_meta_data.get('ents', []):
                if item_types.has_value(ent['type']):
                    item_dict = {'item_type': ent['type'], 'item_index': ent['id']}
                    item_list.append(item_dict)
    
            self._load_item_list(item_list)
        
    @property
    def got_items(self):
        return self.items is not None
            
    def initialize_player(self, cds, player):
        if self.items is not None:
            swh.put_itemlist(cds, self.items)

    def on_player_item_list(self, player, item_list):
        if not self.got_items:
            self._load_item_list(item_list)

    def on_player_pickup_item(self, player, item_index):
        if self.items is None: return
        if item_index < len(self.items) and item_index >= 0:
            item = self.items[item_index]
            if isinstance(item, Item):
                item.pickup(player)

    def _load_item_list(self, item_list):
        self.items = []
        i = 0
        for item_dict in item_list:
            n = item_dict['item_index']
            while i < n:
                self.items.append(UnusedItemSlot(i))
                i += 1

            item = Item(self.room, self.room._game_clock, n, item_dict['item_type'])
            self.items.append(item)
            i += 1
