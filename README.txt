
**************** This code has been done in Windows OS******************
Requirements:
1. HiveMQ - it is MQTT broker (Downlad: https://www.hivemq.com/downloads/hivemq/)
2. python3
3. Mosquitto library (pip install paho-mqtt)

Step1: Open the folder named "Project_Files"
        It will contain files: "goto.ps1", "assign.ps1", "input_windows.py", "new_park_input.py", "new_smart_park.py"


	Code Flow : goto.ps1 ---> input_windows.py ---> assign.ps1 ---> new_park_input.py ---> new_smart_park.py

        File description:
	"goto.ps1" : This file executes "input_windows.py" ; after "input_windows.py" takes input for number of slots it will automatically executes "assign.ps1"

        "input_windows.py" : This file takes input as a number of parking slots to be used for parking system. Further it
                             will create shell script file named "assign.ps1", and other txt files for parking and output.txt
                             file for storing parking logs.

	"assign.ps1" : 	This shell script contains commands to open all instance required for parking system

        "new_park_input.py" : It takes users choice from available options park,unpark,free space, dispaly, exit as input.
                             According to users input program will publish message for its subscriber using mqtt as protocol
                             on HiveMq server.

        "new_smart_park.py" : This program file perform the parking system functionality based on topic subscribed.

        

Step2: Open and run the hivemq broker in the browser 
	    a. Open the hivemq-4.2.2 folder and open bin folder and run the run.bat file as administrator.
	    b. Open browser and type "localhost:8080"
	    c. username- admin
	       password- hivemq

Step3: Open cmd and go to directory where "Project_Files" folder present and run file "goto.ps1"
        command:  .\goto.ps1 

	[* "input_windows.py" will run by asking enter number for parking slots ---please enter the number of parking slots you needed.]
	

Step4: After sccussfully completion of above all steps, instances for parking slots and user display will be open.
        Now you can provide your choice to use parking system.

Step5: open "output.txt" file under folder "Project_Files" which will display parking lots.

NOTE : -
	If powershell gives error like "not digitally signed" please type this command 
	"Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"
	then "y" when it asks for confirmation.
	Now perform step 3.

