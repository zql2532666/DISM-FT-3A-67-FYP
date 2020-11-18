from socket import socket, AF_INET, SOCK_DGRAM,SOCK_STREAM
import socket
from time import time, ctime, sleep
import sys
import multiprocessing
import threading
import json
from configparser import ConfigParser

config = ConfigParser()
# honeyagent.conf is generated by the deployment bash script
config.read('honeyagent.conf')


#C2 SERVER INFO
SERVER_IP = config['C2-SERVER']['SERVER_IP']                    
SERVER_HB_PORT = int(config['HEARTBEATS']['SERVER_HB_PORT'])            
HELLO_INTERVAL = int(config['HEARTBEATS']['HELLO_INTERVAL'])               
SERVER_HANDSHAKE_PORT = int(config['C2-SERVER']['SERVER_HANDSHAKE_PORT'])


# HONEYNODE INFO
TOKEN = config['HONEYNODE']['TOKEN']
HONEYNODE_NAME = config['HONEYNODE']['HONEYNODE_NAME']
HONEYNODE_IP = config['HONEYNODE']['IP']
HONEYNODE_SUBNET_MASK = config['HONEYNODE']['SUBNET_MASK']
HONEYNODE_HONEYPOT_TYPE = config['HONEYNODE']['HONEYPOT_TYPE']
HONEYNODE_NIDS_TYPE = config['HONEYNODE']['NIDS_TYPE']
HONEYNODE_DEPLOYED_DATE = config['HONEYNODE']['DEPLOYED_DATE']
HONEYNODE_COMMAND_PORT = int(config['HONEYNODE']['COMMAND_PORT'])



handshake_data = {
    "token": TOKEN,
    "honeynode_name": HONEYNODE_NAME,
    "ip_addr": HONEYNODE_IP,
    "subnet_mask": HONEYNODE_SUBNET_MASK,
    "honeypot_type": HONEYNODE_HONEYPOT_TYPE,
    "nids_type": HONEYNODE_NIDS_TYPE,
    "deployed_date": HONEYNODE_DEPLOYED_DATE,
    "msg": "HANDSHAKE"
}

handshake_data_json = json.dumps(handshake_data)
# data might get lost if u send over udp, think about sending the web api directly or 
# have a tcp port sitting on the main server, listening for handshake data

def listen_for_commands():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("listening for commands")
            s.bind(('127.0.0.1',HONEYNODE_COMMAND_PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Command received from {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                data = data.decode('utf-8')
                data = json.loads(data)
                print(data)
                """
                    the command should look like 
                    {"command" : "handshake"}
                """
    except socket.error as e:
        print(f"Error creating commmand Socket\n {e}")


def process_command_from_c2(command):
    if (command == "handshake"):
        # send data to flask api end point 
        # ... call the http end point here
        # on the flask, check if there is a duplicate token/ip address, 
        #   if there is , update the status of the honeynode as, active. 
        #   If not, add this as a new honeypot
        print("handshake")
    elif (command == "kill"):
        # kill the honeyagent program + hp feeds
        print("kill")

def perform_handshake():
    print("handshake")

def kill():
    print("kill")