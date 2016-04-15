# water-monitor



The goal of this project is to form a development community around the STORC facility on the CSU Sacramento campus. 
The STORC (Sustainable Technology Optimization and Research Center) 
is a facility geared towards the research and implementation of sustainable technology. 
More information can be found here:

http://www.csus.edu/storc/

The water-monitor project is aimed at producing a relatively inexpensive, 
scalable, and scientifically precise water monitoring solution for hydroponic and aquaponic food production systems. 
Providing invaluable experimental feedback for cutting edge research in the field of aquaponics.

 Version 0.1 is deprecated.

The current system uses an arduino UNO for real-time sensor control, and the Raspberry Pi 3 for database management and web interface display. The RPi.GPIO module in Python is not suitable for real time control. Under the limited use of the original system it performed adequately, but as the intervals on the sensor queries became shorter, a different solution was needed and the Raspberry Pi could no longer be used by itself.

