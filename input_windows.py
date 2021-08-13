print("Enter number of slots to be used for parking: ")
slots=int(input())
print("--------------------------------------")

print("Total slots for parking are ",slots)

print("--------------------------------------")
for i in range(1,slots+1):
    file_name="lot"+str(i)+".txt"
    with open(file_name,'w') as f:
        f.write("free")
with open("assign.ps1",'w') as f:
    line="start powershell \"python new_smart_park.py lot"
    for j in range(1,slots+1):
        new_line=line+str(j)
        f.write(new_line+"\"\n")
    f.write("start powershell \"python new_park_input.py "+str(slots)+"\"")

#start powershell "python new_smart_park.py lot1"
#start powershell "python new_smart_park.py lot2"
#start powershell "python new_smart_park.py lot3"
#start powershell "python new_smart_park.py lot4"
#start powershell "python new_smart_park.py lot5"
#start powershell "python new_smart_park.py lot6"
#start powershell "python new_park_input.py 6"