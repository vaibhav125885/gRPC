import grpc
from concurrent import futures 
import schema_pb2
import schema_pb2_grpc

class ItemServiceServicer(schema_pb2_grpc.ItemServiceServicer):
    def GetItem(self, request, context):
        items = {
            1: {"name": "Laptop", "price": 2000.5},
            2: {"name": "Watch", "price":849038.46}
        }
        
        item = items.get(request.item_id, {"name":"Unknown item", "Price": 0.0})
        
        return schema_pb2.ItemResponse(
            item_id = request.item_id,
            name= item["name"],
            price= item["price"],
        )
        
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schema_pb2_grpc.add_ItemServiceServicer_to_server(ItemServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Server has running om Port: 50051")
    server.start()
    server.wait_for_termination()
    
if __name__ == '__main__':
    serve()