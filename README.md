# Naukari-Daily-Resume-Update-Automation

This has created only for educational purpose.
This script daily updates the resume on your Naukri profile so as to increase your profiles visibility for recruiters. Once the script will be successfully executed you will be notified over the email.

#HOW TO USE :
- Clone the repository :
                git clone https://github.com/srivastavas08/Naukari-Daily-Resume-Update-Automation.git
- update the environment variables with your own credentials.
- Add your own resume in pdf format.
- Execute app.py

#Schedule the Python Script using the Windows Scheduler.
- Open the Windows Control Panel and then click on the Administrative Tools.
- Double-click on the Task Scheduler, and then choose the option to ‘Create Basic Task…’
- Type a name for your task (you can also type a description if needed), and then press Next. For instance, let’s name the task as: Run app.py
- Choose to start the task ‘Daily‘ since we wish to run the Python script daily at 6am. Also specify the start date and time (6am for our example)
- Select, Start a program, and then press Next
- Use the Browse button to find the batch file (naukari.bat) that runs the Python script. In our case:
                C:\Users\srivastavas08\Desktop\naukari.bat

Incase of any additional querries or concerns drop an email at srivastavas08@gmail.com.
