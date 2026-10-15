from fastapi import FastAPI,HTTPException
import grpc
import schema_pb2_grpc
import schema_pb2

app = FastAPI()

def get_grpc_stub():
    channel = grpc.insecure_channel('localhost:50051')
    stub = schema_pb2_grpc.ItemServiceStub(channel)
    return stub

@app.get("/items/(item_id}")
def read_item(item_id: int):
    try:
        stub = get_grpc_stub()
        response = stub.GetItem(schema_pb2.ItemRequest(item_id=item_id))
        return {
            "item_id": response.item_id,
            "name": response.name,
            "price": response.price
        }
        
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC Error: {e.details()}")