from spyd.registry_manager import register


@register('award')
class Champion(object):
    left_weight = 7
    award_text = "Champion"

    @staticmethod
    def is_client_eligible(client):
        return client.state.flags > 0 and not client.state.is_spectator

    @staticmethod
    def get_stat_from_client(client):
        return client.state.flags

    @staticmethod
    def format_stat(stat):
        return str(stat)

    @staticmethod
    def is_valid_mode(mode_name):
        return mode_name[-3:] == 'ctf'
