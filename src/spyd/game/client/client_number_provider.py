import heapq

class ClientNumberProvider(object):
    def __init__(self, max_clients):
        self.cn_pool = list(range(max_clients))
        heapq.heapify(self.cn_pool)

    def acquire_cn(self):
        return heapq.heappop(self.cn_pool)

    def release_cn(self, cn):
        heapq.heappush(self.cn_pool, cn)

class ClientNumberHandle(object):
    def __init__(self, client_number_handle_provider):
        self._client_number_provider = client_number_handle_provider
        self.cn = self._client_number_provider.acquire_cn()

    def release(self):
        if self.cn is None: return
        self._client_number_provider.release_cn(self.cn)
        self.cn = None

class ClientNumberHandleProvider(object):
    def __init__(self, client_number_handle_provider):
        self._client_number_provider = client_number_handle_provider

    def acquire_cn_handle(self):
        return ClientNumberHandle(self._client_number_provider)

def get_client_number_handle_provider(config):
    room_bindings = config.get('room_bindings', {})
    max_client_sum = 0
    for room_binding in room_bindings.itervalues():
        max_client_sum += room_binding.get('maxclients', 0)

    client_number_provider = ClientNumberProvider(max_client_sum)

    return ClientNumberHandleProvider(client_number_provider)
