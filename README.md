Tested under Ubuntu 14.04. 
--------------------------

GUI - app. Gives info about internet provider's balance (once per day, valid for internet provider tis-dialog.ru(Kaliningrad)), local weather (gets data from openweathermap.org, every 15 mins by default).

USAGE:
------
Specify correct path to python-binary on the head.

Open weather_widget.py and modify three parameters for your needs:

TIS_LOGIN = 'put your login here' 

TIS_PASSWD = 'put your password here'

API_OpenWeather = 'put your APPID here from openweathermap.org'

RUN:
----
chmod +x weather_widget.py

./weather_widget.py
