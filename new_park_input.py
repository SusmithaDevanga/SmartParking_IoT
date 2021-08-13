import paho.mqtt.client as mqttClient
import time
import random
import math
import sys
import json

#time.sleep(10)
check_park=0
result=""
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker smart_park")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed Return Code : ",rc)
 
#to store whether they are free or not        
n=int(sys.argv[1])
#print(" n is ",n)
#time.sleep(20)
to_dict={}
for i in range(1,n+1):
    to_dict[i]=''


global sentornot

def on_message(client, userdata, message):
    #storing into the index 'X' of dictionary when HQ receive message from UAV 'X'
    global available_slots
    global sentornot
    global unpark_found
    global already_parked
    str_payload = str(message.payload)
    
    rec_prkstr= str(message.topic)
    rec_prkid = int(rec_prkstr[-1])
    if("parking/output" in rec_prkstr):
        check_park=1
        if("free" in str_payload):
                 
            available_slots=available_slots+(rec_prkstr[-1])+"  "
             #print("gone here   ")
        elif("already" in str_payload):
             already_parked=rec_prkid
    
    
             #available_slots=str_payload[1:-1]
    
    # print(str(to_dic))
    elif("unpark/output" in rec_prkstr):

        unpark_found=1
        str_payload= str_payload[2:]
      
        print("check out from parking lot: ",rec_prkid,":::: vehicle number: ",str_payload[:-3])

    elif("display/output" in rec_prkstr):
        str_payload= str_payload[2:]
        print("parking lot:",rec_prkid," ===>  vehicle number:",str_payload[:-3])



#time.sleep(20)


Connected = False  # global variable for the state of the connection
client_name="smart_park"
broker_address = "127.0.0.1"  # Broker address
port = 1883  # Broker port

#time.sleep(20)


client = mqttClient.Client(client_name)  # create new instance


client.on_connect = on_connect  # attach function to callback

client.connect(host= broker_address, port=port)  # connect to broker
client.on_message = on_message  # attach function to callback


client.loop_start()  # start the loop

while Connected != True:  # Wait for connection
    time.sleep(0.1)

client.subscribe("parking/output/+")
client.subscribe("unpark/output/+")
client.subscribe("display/output/+")


global unpark_found
unpark_found=0
count=0
time_seq=0
new_str=""
#print("susmi")
#test=input()
#print(test)
print("\nenter 0-freespace  1-park  2-display   3-unpark  4-exit");
msg_topic=""
park_check=0
free_check=0
unpark_check=0
global available_slots
global already_parked
already_parked=0
available_slots=""

while (1):
    user_input= input();
    user_input=(int)(user_input)
    sentornot=0
    park_check=0
    free_check=0
    unpark_check=0
    unpark_found=0
    already_parked=0
    if(user_input==0):
        #print("entered in freespace")
        curr_loc="freespace";
        msg_topic="parking/input/"        
        free_check=1
    elif(user_input==1):
        print("\nenter vehicle number: ")
        curr_loc=input();
        msg_topic="parking/input/"
        park_check=1
    elif(user_input==2):
        print("\nenter vehicle number: ")
        curr_loc=input();
        msg_topic="display/input"
    elif(user_input==3):
        print("\nenter vehicle number: ")
        curr_loc=input();
        msg_topic="unpark/input/"
        unpark_check=1
    elif(user_input==4):
        curr_loc=""
        msg_topic="exit/input"
        client.publish(msg_topic,curr_loc)
        break
    
    #print('\n\npublishing ',curr_loc)
    
    client.publish(msg_topic,curr_loc)
    
    
    time.sleep(3)
    if(int(unpark_check)==1 and (int)(unpark_found)==0):
        print("there is no vehicle available with the given number")
        
    if(int(free_check)==1):
         print("available slots are : ",available_slots)
         available_slots=""
         
         
    if(int(park_check)==1):
        #time.sleep(3)
       # print("entered")
        if(available_slots in ""):
            print("all slots are full please wait sometime")
        elif(already_parked!=0):
            #print("HELLO entered here")
            #time.sleep(3)
            print("already parked in slot number ",already_parked)
            time.sleep(3)
            
            
        else:
            print("available slot are : ",available_slots,"\nplease enter preferrable slot number")
            pre_slot=input()
            if(pre_slot not in available_slots):
                print("already occupied, not possible to park your vehicle")
            else:
                pre_slot=int(pre_slot)
            
                print("going to store in lot",pre_slot)
                #publish
                client.publish("parking/select/",pre_slot)
        available_slots=""
        
    sentornot=0
    time.sleep(3)
    print("\n----------------------\nenter  0-freespace 1-park  2-display   3-unpark   4-exit");
    

print("exiting")
client.disconnect()
client.loop_stop()
time.sleep(200)


