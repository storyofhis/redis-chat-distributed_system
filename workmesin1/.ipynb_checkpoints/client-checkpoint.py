import zmq
from threading import Thread, Event
import sys
import time
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

ipclient = config['DEFAULT']['ipfront']
ipserver = config['DEFAULT']['ipback']
portclient = config['DEFAULT']['port_req']
portserver = config['DEFAULT']['port_back']

clientName = sys.argv[1]
context = zmq.Context()

# Event to signal termination to client threads
terminate_event = Event()

def subscriber():
    sock = context.socket(zmq.SUB)
    sock.connect("tcp://%s:%s" % (ipserver, portserver))
    sock.setsockopt_string(zmq.SUBSCRIBE, "")

    while not terminate_event.is_set():
        time.sleep(1)
        try:
            pub_message = sock.recv_string(flags=zmq.NOBLOCK)
            if pub_message and ("[{}]:".format(clientName) not in pub_message):
                print("\n" + pub_message + "\n[" + clientName + "]>", end="")
        except zmq.Again:
            pass  # No message received

    print("ERROR: Server seems to be offline, abandoning.")

def lazy_pirate_sender():
    sender = context.socket(zmq.REQ)
    sender.connect("tcp://%s:%s" % (ipclient, portclient))
    retries = 3

    for _ in range(5):  # Attempt 5 messages
        retries = 3  # Reset retries for each message
        while retries > 0:
            try:
                message = input("[{0}] > ".format(clientName))
                message = "[%s]:  %s" % (clientName, message)
                sender.send_string(message, flags=zmq.NOBLOCK)
                
                if sender.poll(1000, zmq.POLLIN):
                    reply = sender.recv_string()
                    print(f"Received reply: {reply}")
                    break  # Successful send and receive
            except zmq.Again as e:
                print(f"No response from server, retrying... ({retries} retries left)")
                retries -= 1

        if retries == 0:
            print("Server seems to be offline, abandoning.")
            terminate_event.set()  # Set termination event
            break

# Start the subscriber thread
subscriber_thread = Thread(target=subscriber)
subscriber_thread.start()

# Start the sender (lazy pirate) thread
lazy_pirate_thread = Thread(target=lazy_pirate_sender)
lazy_pirate_thread.start()

# Wait for both threads to complete
subscriber_thread.join()
lazy_pirate_thread.join()