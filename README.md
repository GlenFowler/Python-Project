# Python-Project Version 1.1

Description
===========
You would to know about different information of your network devices, such IOS routers or Nexus
devices.
With this script you can collect data from your devices:
	
	You can know all available devices in the network. For each device, You can know:
		hardware version,
		OS version running on the device,
		management ip address,
		password
		modules which are installed on the device - and status of each module

	You can know the topology
	You can see the interface description and interface status for each interface on each device.


Utilization
===========
Add to the same directory password.txt, range.txt and database.txt files, together with the other python files:

	password.txt ---> Different passwords use by the routers.
	
	range.txt ----> IP address range for management.
	
	database.txt ---> SQL database credentials.
	
	*pcs.txt ---> If there is any pc in the same range you can add his IP here.

Save all in the same directory and execute main.py

Example:
	
	$ python3 main.py
	

Version 1.1: You only need to change the credentials in the file database.txt

*No longer available, Version 1.0: You need also to configure a SQL data base to save the data from devices. Change the values in
			 savedataSQL.py, takedataSQL.py and createSQLdb.py


You can create the DB table with the script createSQLdb.py.

Modules needed:

	colorama
	
	paramiko
	
	pymysql
	
	networkx
	
	matplotlib


Development
===========

Help and fixes welcome!

	- Domingo Fernandez Piriz
	- Laura Muñoz Parejo
	- Javier Ortiz Bonilla
	- Glen Fernandez Fowler

Fixes
-----------

	Fix 1# --> DB selection: Fixed a problem when change DB hosting.
	Fix 2# --> Added a solution if change the IP management range.


