import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)

INVENTORY_HOST = os.environ.get("INVENTORY_HOST", "127.0.0.1")
INVENTORY_PORT = os.environ.get("INVENTORY_PORT", "8000")

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    try: 
       return Order.get(pk)
    except:
        print("Somthing Wrong get had haoend ")
        raise HTTPException( status_code=204,detail=f"Product with this id  {pk}is aleready deleted ")

@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()

    req = requests.get('http://%s:%s/products/%s' % (INVENTORY_HOST, INVENTORY_PORT, body['id']))
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    background_tasks.add_task(order_completed, order) # simulating Payment processor taking  littil time for process your order 

    order.save()

    return order

def order_completed(order: Order):
    time.sleep(10)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed2', order.dict(), '*')



