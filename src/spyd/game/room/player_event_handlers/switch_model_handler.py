from spyd.protocol import swh
from spyd.registry_manager import register
from spyd.utils.constrain import constrain_range


@register('room_player_event_handler')
class SwitchModelHandler(object):
    event_type = 'switch_model'

    @staticmethod
    def handle(room, player, playermodel):
        constrain_range(playermodel, 0, 4, "playermodels")
        player.playermodel = playermodel
        swh.put_switchmodel(player.state.messages, playermodel)
