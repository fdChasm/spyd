from spyd.protocol import swh
from spyd.registry_manager import register


@register('room_player_event_handler')
class GameChatHandler(object):
    event_type = 'game_chat'

    @staticmethod
    def handle(room, player, text):
        if text[0] == "#":
            room.command_executer.execute(room, player.client, text)
        else:
            swh.put_text(player.state.messages, text)
            room.event_subscription_fulfiller.publish('spyd.game.player.chat', {'player': player.uuid, 'room': room.name, 'text': text, 'scope': 'room'})
