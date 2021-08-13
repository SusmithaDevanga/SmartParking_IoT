import paho.mqtt.client as mqttClient
import time
import random
import math
import sys
import json
import sqlite3
from sqlite3.dbapi2 import Cursor, Timestamp

#print("hello 0 ")
#time.sleep(10)
all_lots=[]
#print("hello  ")
str_lot=sys.argv[1]
n=int(str_lot[-1])
#print("check1 n is ", n)
#time.sleep(20)
for i in range(1,n+1):
    all_lots.append('lot'+str(i))

def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker",client_name)
            global Connected  # Use global variable
            Connected = True  # Signal connection
        else:
           print("Connection failed and returned",rc)


total_lots=n           
global curr_lot_loc
def display_slots():
    global curr_lot_loc
    s=str(pre_client)
    file_name="lot"+s+".txt"
    curr_lot_loc = open(file_name,"r") 
    into_rows= curr_lot_loc.readlines()
    with_spaces= (into_rows[-1])
    curr_status= with_spaces
    print(curr_status)
    return curr_status


def park_accordingly(vehicle_number):
    s=str(pre_client)
    file_name="lot"+s+".txt"
    curr_lot_loc = open(file_name,"a") 
    curr_lot_loc.write("\n")
    curr_lot_loc.write(vehicle_number)
    curr_lot_loc.write("\n")
    curr_lot_loc.close()


global vehicle_nbr_to_be_parked
def on_message(client, userdata, message):
    global exit1
    print('\n\n')
    
    str_topic= str(message.topic)
    str_payload = str(message.payload)
    str_payload=str_payload[2:]
    
    #this if process the  type 2 messages
    if("parking/input" in str_topic):
        #print("\nMessage Received is : " + str(message.payload))
        #print("Message Received on Topic " + str(message.topic))
        print("------display list for parking-----")
       
       #give all available lots
        #to display available slots
        
        to_list=str_payload.split()
        global vehicle_nbr_to_be_parked
        vehicle_nbr_to_be_parked=(to_list[0])[0:-1]
        

        lot_status= display_slots()
        if("freespace" in str_payload and "free" in lot_status):
            client.publish("parking/output/"+client_name,lot_status)
            
        elif(vehicle_nbr_to_be_parked in lot_status):
            lot_status="already parked in"+str(pre_client)
            #print("here its already here")
            client.publish("parking/output/"+client_name,lot_status)
            
        elif("free" in lot_status):
            client.publish("parking/output/"+client_name,lot_status)
     #   print('\')
       
    
    
    elif("unpark/input/" in str_topic):
        #print("\nMessage Received is : " + str(message.payload))
        #print("Message Received on Topic " + str(message.topic))
        print("-------unpark (checking only)--------")
        str_payload=str_payload[:-1]
        vehicle_num=(str_payload.split())[0]
        #print("have to unpark ",vehicle_num)
        
        #last_4_input=vehicle_num[-4:]
        #print("\nlast 4 digits input",last_4_input)
        lot_status=display_slots()
       
        if("free" not in lot_status):
            #print(vehicle_num)
            #print(lot_status)
            #print("compare ",vehicle_num is lot_status)
            #last_4_stored=lot_status[-5:]
            #print("\nlast 4 digits stored",last_4_stored)
            #print("type of veh", type(vehicle_num))
            #print("type of stored",type(lot_status))
            #if(int(last_4_input)==int(last_4_stored)):
                #print("2 type of veh", type(vehicle_num))
                #print("2 type of stored",type(lot_status))
                if(vehicle_num in lot_status):
                #sif(vehicle_num==lot_status):
                    print("\n given vehicle is stored in this lot i.e ",pre_client)
                    print("\n so UNPARK it")
                    file2= open("output.txt", "a")
                    file2.write(vehicle_num+"----UNPARK----"+client_name)
                    file2.write("\n")
                    file2.close()
                    park_accordingly("free")
                    client.publish("unpark/output/"+client_name,lot_status)
        
    elif("display/input" in str_topic):
        #print("\nMessage Received is : " + str(message.payload))
        #print("Message Received on Topic " + str(message.topic))
        print("-------display checking last 4 digits--------")
        str_payload=str_payload[:-1]
        vehicle_num=(str_payload.split())[0]
        last_4_input=vehicle_num[-4:]
        lot_status=display_slots()
        if("free" not in lot_status):
            last_4_stored=lot_status[-5:]
            #print("\nlast 4 digits stored",last_4_stored)
            if(int(last_4_input)==int(last_4_stored)):
                client.publish("display/output/"+client_name,lot_status)
                
    
    
    elif("parking/select" in str_topic):
        #print("\nMessage Received is : " + str(message.payload))
        #print("Message Received on Topic " + str(message.topic))
        #print("--------park(checking only)--------")
        #print("entered and payload is ",str_payload)
        lot_num=int(str_payload[0:1])
        #print("entered and payload is ",lot_num,"and pre client is ",pre_client)
        if(pre_client == lot_num):
            #print("u r mine ",vehicle_nbr_to_be_parked)
            print("PARKing vehicle number "+vehicle_nbr_to_be_parked)
            park_accordingly(vehicle_nbr_to_be_parked)
            file2= open("output.txt", "a")
            file2.write(vehicle_nbr_to_be_parked+"----PARK----"+client_name)
            file2.write("\n")
            file2.close()
    elif("exit/input" in str_topic):
        
        print("-------exit-------")
        exit1=0











        
Connected = False
client_name=sys.argv[1]
broker_address = "127.0.0.1"  # Broker address
port = 1883  # Broker port
user = "admin"  # Connection username
password = "hivemq"  # Connection password
           

print(client_name)
client = mqttClient.Client(client_name)  # create new instance


client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback


client.connect(host= broker_address, port=port)  # connect to broker


client.loop_start()  # start the loop

while Connected != True:  # Wait for connection
    time.sleep(0.2)




client.subscribe("parking/input/")
client.subscribe("unpark/input/")
client.subscribe("parking/select/")
client.subscribe("display/input")
client.subscribe("exit/input")

pre_client= int(client_name[-1])

loop_count=0

global exit1
exit1=1
while (exit1):
   
    
    
    time.sleep(6)
    
    
    
        
print("exiting")
client.disconnect()
client.loop_stop()
time.sleep(200)        
        
    