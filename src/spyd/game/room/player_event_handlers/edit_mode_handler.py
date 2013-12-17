from cube2protocol.cube_data_stream import CubeDataStream
from spyd.protocol import swh
from spyd.registry_manager import register


@register('room_player_event_handler')
class EditModeHandler(object):
    event_type = 'edit_mode'

    @staticmethod
    def handle(room, player, editmode):
        with room.broadcastbuffer(1, True, [player]) as cds:
            tm = CubeDataStream()
            swh.put_editmode(tm, editmode)
            swh.put_clientdata(cds, player.client, str(tm))
