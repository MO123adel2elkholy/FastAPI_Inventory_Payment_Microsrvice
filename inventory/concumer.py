from main import redis, Product
import time

key = 'order_completed2'
group = 'inventory-group'
consumer = 'inventory-consumer-1'

try:
    # create group even if stream doesn't exist
    redis.xgroup_create(key, group, id='0', mkstream=True)
except Exception as e:
    print('xgroup_create:', e)

while True:
    try:
        results = redis.xreadgroup(group, consumer, {key: '>'}, count=1, block=2000)

        if results:
            for stream, messages in results:
                for message_id, message in messages:
                    obj = {k: v for k, v in message.items()}
                    try:
                        product = Product.get(obj['product_id'])
                        product.quantity = product.quantity - int(obj['quantity'])
                        product.save()
                        redis.xack(key, group, message_id)
                        print('order processed: success fully ', obj)
                    except Exception as e:
                        print('processing error:', e)
                        #  this is uesd for Handling refund order if somtiing wrong with the product like delete the product 
                        redis.xadd('refund_order', obj, '*')  # sending refunded event to payment srvice 

    except Exception as e:
        print('consumer error:', e)

    time.sleep(0.1)
