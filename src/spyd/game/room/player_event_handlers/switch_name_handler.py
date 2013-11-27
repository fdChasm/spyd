from spyd.protocol import swh
from spyd.registry_manager import register


@register('room_player_event_handler')
class SwitchNameHandler(object):
    event_type = 'switch_name'

    @staticmethod
    def handle(room, player, name):
        player.name = name
        swh.put_switchname(player.state.messages, name)
        # with room.broadcastbuffer(1, True) as cds:
        #    tm = CubeDataStream()
        #    swh.put_switchname(tm, "aaaaa")
        #    swh.put_clientdata(cds, player.client, str(tm))
