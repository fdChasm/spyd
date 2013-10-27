from spyd.registry_manager import register


@register('award')
class FragMonger(object):
    left_weight = 10
    award_text = "Frag Monger"

    @staticmethod
    def is_client_eligible(client):
        return client.state.frags > 0 and not client.state.is_spectator

    @staticmethod
    def get_stat_from_client(client):
        return client.state.frags

    @staticmethod
    def format_stat(stat):
        return str(stat)

    @staticmethod
    def is_valid_mode(mode_name):
        return True
