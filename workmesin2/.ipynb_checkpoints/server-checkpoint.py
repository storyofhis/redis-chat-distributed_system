import zmq
import time
import configparser

from redis.sentinel import Sentinel

# Connect to Redis Sentinel
sentinels = [('192.168.1.7', 26379), ('192.168.1.7', 26380), ('192.168.1.7', 26381)]
service_name = 'mymaster'

def get_redis_sentinel():
    return Sentinel(sentinels, socket_timeout=0.1)

def get_master_conn():
    sentinel = get_redis_sentinel()
    return sentinel.master_for(service_name, socket_timeout=0.1)

redis_client = get_master_conn()

def store_in_redis(message):
    # Store the message in Redis with a key representing chat history
    # You can use Redis lists or other structures depending on your needs
    redis_client.lpush('chat_history', message)



config = configparser.ConfigParser()
config.read('config.cfg')

ipclient = config['DEFAULT']['ipfront']
ipserver = config['DEFAULT']['ipback']
portclient = config['DEFAULT']['port_req']
portserver = config['DEFAULT']['port_back']

context = zmq.Context()

def simulate_server():
    receiver = context.socket(zmq.REP)
    receiver.bind("tcp://%s:%s" % (ipclient, portclient))
    
    broadcaster = context.socket(zmq.PUB)
    broadcaster.bind("tcp://%s:%s" % (ipserver, portserver))
    
    retries = 3
    requests_received = 0

    for _ in range(5):  # Simulate processing 5 requests
        try:
            message = receiver.recv()
            broadcaster.send(message)
            print("[Server] Echo: " + message.decode())
            receiver.send(b"OK")  # Sending a response to the client
            requests_received += 1

            # Store the message in Redis
            store_in_redis(message.decode())

            if requests_received == 2:  # Simulate CPU overload after 2 requests
                print("Simulating CPU overload")
                time.sleep(3)
            elif requests_received == 4:  # Simulate crash after 4 requests
                print("Simulating a crash")
                raise Exception("Simulated Crash")

        except zmq.Again as e:
            print(f"No request received, retrying... ({retries} retries left)")
            retries -= 1
            if retries == 0:
                print("Server seems to be offline.")
                break
        except Exception as e:
            print(f"Exception: {str(e)}")
            break

    # Optionally, you can retrieve chat history from Redis at the end
    chat_history = redis_client.lrange('chat_history', 0, -1)
    print("Chat History in Redis:")
    for message in chat_history:
        print(message.decode())

    # Close Redis connection when done
    redis_client.close()
    receiver.close()
    broadcaster.close()
    context.term()

simulate_server()
