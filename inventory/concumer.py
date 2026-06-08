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
                    except Exception as e:
                        print('processing error:', e)
                        redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print('consumer error:', e)

    time.sleep(0.1)
