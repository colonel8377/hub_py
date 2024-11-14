import grpc

from src.hub_py.generated.hub_event_pb2 import HubEventType
from src.hub_py.generated.request_response_pb2 import SubscribeRequest
from src.hub_py.generated.rpc_pb2_grpc import HubServiceStub


# Initialize the peer log CSV file with headers if it does not exist


# Define your gRPC client class
class EventClient:
    def __init__(self, server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = HubServiceStub(self.channel)

    def subscribe_to_events(self):
        # Create a SubscribeRequest
        request = SubscribeRequest(event_types=[HubEventType.HUB_EVENT_TYPE_MERGE_MESSAGE], from_id=0)

        # Call the Subscribe method, which returns a stream
        response_stream = self.stub.Subscribe(request)

        # Iterate over the response stream
        try:
            for response in response_stream:
                self.handle_event(response)
        except grpc.RpcError as e:
            print(f"gRPC error occurred: {e.code()} - {e.details()}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            self.channel.close()

    def handle_event(self, event):
        # Process the event
        print("Received event:", event)

if __name__ == "__main__":
    client = EventClient("43.198.202.142:2283")  # Replace with your server address
    client.subscribe_to_events()