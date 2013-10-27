from spyd.registry_manager import register


@register('award')
class Pursuer(object):
    left_weight = 6
    award_text = "Pursuer"

    @staticmethod
    def is_client_eligible(client):
        return client.state.flag_returns > 0 and not client.state.is_spectator

    @staticmethod
    def get_stat_from_client(client):
        return client.state.flag_returns

    @staticmethod
    def format_stat(stat):
        return str(stat)

    @staticmethod
    def is_valid_mode(mode_name):
        return mode_name[-3:] == 'ctf'
