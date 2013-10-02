class ClientManager(object):
    """
    The client manager maintains a collection of all the actual clients on the server.
    Its responsibilities are as follows;
        - Hold each client instance
        - On new connections:
          * pass the binding_protocol and the message to the client factory
          * store the resulting client
          * start the events bubbling up by letting the client know it is connected
        - On incoming data:
          * pass the client instance and the message to the message_processor
          * start the events bubbling up by passing the processed message to the client
        - On disconnections
          * stop holding the client instance
          * start the events bubbling up by letting the client know it is disconnected
    """
    def __init__(self, client_factory, message_processor):
        self.client_factory = client_factory
        self.message_processor = message_processor

        self.clients_by_identifier = {}
        self.clients_by_clientnum = {}

    def message_received(self, binding_protocol, message):
        message_type = message['type']
        if message_type == "connect":
            self.client_connected(binding_protocol, message)
        elif message_type == "receive":
            self.client_receive(binding_protocol, message)
        elif message_type == "disconnect":
            self.client_disconnected(binding_protocol, message)

    def client_connected(self, binding_protocol, message):
        client = self.client_factory.build_client(binding_protocol, message)
        if client is None: return

        self.clients_by_identifier[client.identifier] = client
        self.clients_by_clientnum[client.cn] = client
        
        client.connected()

    def client_receive(self, binding_protocol, message):
        identifier = message['ident']
        client = self.clients_by_identifier.get(identifier, None)
        if client is None: return
        
        processed_messages = self.message_processor.process(client, message)
        
        for processed_message in processed_messages:
            client.message_received(*processed_message)

    def client_disconnected(self, binding_protocol, message):
        identifier = message['ident']
        client = self.clients_by_identifier.get(identifier, None)
        if client is None: return
        
        client.disconnected()
        
    def disconnect_all(self, disconnect_type, message):
        for client in self.clients_by_clientnum.itervalues():
            client.disconnect(disconnect_type, message)
