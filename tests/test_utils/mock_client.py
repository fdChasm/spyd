from mock import Mock
from spyd.game.client.client import Client


def mock_client(cn=0):
    client = Mock(spec=Client)
    client.cn = cn
    return client
