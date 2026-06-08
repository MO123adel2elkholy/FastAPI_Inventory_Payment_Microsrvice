from main import redis, Order
import time

key = 'refund_order'
group = 'payment-group'
consumer = 'payment-consumer-1'

try:
    # ensure stream and group exist
    redis.xgroup_create(key, group, id='0', mkstream=True)
except Exception as e:
    print('xgroup_create:', e)

while True:
    try:
        # correct arg order: (group, consumer, {stream: '>'}, ...)
        results = redis.xreadgroup(group, consumer, {key: '>'}, count=1, block=2000)

        if results:
            for stream, messages in results:
                for message_id, message in messages:
                    obj = {k: v for k, v in message.items()}
                    order_pk = obj.get('pk') or obj.get('id')
                    try:
                        order = Order.get(order_pk)
                        order.status = 'refunded'
                        order.save()
                        redis.xack(key, group, message_id)
                        print('order refunded:', order_pk)
                    except Exception as e:
                        print('refund processing error:', e)

    except Exception as e:
        print('consumer error:', e)

    time.sleep(1)
