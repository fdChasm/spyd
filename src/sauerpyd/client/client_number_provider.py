import heapq

class ClientNumberProvider(object):
    def __init__(self, max_clients):
        self.cn_pool = list(range(max_clients))
        heapq.heapify(self.cn_pool)
        
    def acquire_cn(self):
        return heapq.heappop(self.cn_pool)
    
    def release_cn(self, cn):
        heapq.heappush(self.cn_pool, cn)

def get_client_number_provider(config):
    room_bindings = config.get('room_bindings', {})
    max_client_sum = 0
    for room_binding in room_bindings.itervalues():
        max_client_sum += room_binding.get('maxclients', 0)
    return ClientNumberProvider(max_client_sum)