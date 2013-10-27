from spyd.registry_manager import register


@register('award')
class LoneWolf(object):
    left_weight = 8
    award_text = "Lone Wolf"

    @staticmethod
    def is_client_eligible(client):
        return client.state.frags > 10 and not client.state.is_spectator

    @staticmethod
    def get_stat_from_client(client):
        return client.state.kpd

    @staticmethod
    def format_stat(stat):
        return str(stat)

    @staticmethod
    def is_valid_mode(mode_name):
        return True
