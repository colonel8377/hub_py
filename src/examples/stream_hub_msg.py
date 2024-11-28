import grpc

from src.examples.utils import get_env_client
from src.hub_py.generated.hub_event_pb2 import HubEventType
from src.hub_py.generated.request_response_pb2 import SubscribeRequest, EventRequest, Empty
from src.hub_py.generated.rpc_pb2_grpc import HubServiceStub


# Initialize the peer log CSV file with headers if it does not exist


# Define your gRPC client class
class EventClient:
    def __init__(self, server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = HubServiceStub(self.channel)

    def subscribe_to_events(self, last_event_id):
        # Create a SubscribeRequest
        request = SubscribeRequest(event_types=[HubEventType.HUB_EVENT_TYPE_MERGE_MESSAGE], from_id=last_event_id)

        # Call the Subscribe method, which returns a stream
        response_stream = self.stub.Subscribe(request)

        # Iterate over the response stream
        try:
            for response in response_stream:
                self.handle_subscribe_event(response)
        except grpc.RpcError as e:
            print(f"gRPC error occurred: {e.code()} - {e.details()}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            self.channel.close()

    def handle_subscribe_event(self, event):
        # Process the event
        id = event.id
        merge_message_body = event.merge_message_body
        # merge_on_chain_event_body = event.merge_on_chain_event_body
        # merge_username_proof_body = event.merge_username_proof_body
        # prune_message_body = event.prune_message_body
        # revoke_message_body = event.revoke_message_body
        message = merge_message_body.message
        data = message.data
        message_type = data.type
        fid = data.fid
        timestamp = data.timestamp
        network = data.network

        print("Received event:", event)

if __name__ == "__main__":
    hub_client = get_env_client()
    print(hub_client.GetEvent(EventRequest()))
    # event_client = EventClient("43.198.202.142:2283")  # Replace with your server address
    # event_client.subscribe_to_events(last_event_id = 500105558921216)