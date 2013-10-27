from spyd.registry_manager import register


@register('award')
class DeadEye(object):
    left_weight = 9
    award_text = "Dead Eye"

    @staticmethod
    def is_client_eligible(client):
        return client.state.frags > 10 and not client.state.is_spectator

    @staticmethod
    def get_stat_from_client(client):
        return client.state.acc_percent

    @staticmethod
    def format_stat(stat):
        if stat is Ellipsis: return "inf"
        return "{:.2f}%".format(stat)

    @staticmethod
    def is_valid_mode(mode_name):
        return True
