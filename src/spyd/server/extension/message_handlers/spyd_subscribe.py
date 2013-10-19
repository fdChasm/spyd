from spyd.registry_manager import register
from spyd.permissions.functionality import Functionality

@register('gep_message_handler')
class SpydSubscribeMessageHandler(object):
    msgtype = 'gep.subscribe'
    execute = Functionality(msgtype)

    @classmethod
    def handle_message(cls, spyd_server, gep_client, message):
        event_stream = message.get('event_stream')
        event_handler = gep_client.on_subscribed_event
        
        subscription = spyd_server.event_subscription_fulfiller.subscribe(event_stream, event_handler)
        
        gep_client.event_subscriptions.append(subscription)
        
        gep_client.send({"msgtype": "gep.status", "status": "success"}, message.get('reqid'))
