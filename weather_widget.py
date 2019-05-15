#!/usr/bin/python3.4
#
# __author__ = Pavel Egorov
#
##########################################################
# These three parameters must be set individually
TIS_LOGIN = 'put your login here'
TIS_PASSWD = 'put your password here'
API_OpenWeather = 'put your APPID here'
##########################################################
#
from tkinter import *
import time
from tisdialog import ProviderBalance, get_weather
#
#
#Time delay in miliseconds, 15 min by default
TIME_DELAY = 15*60*1000


class Application(Frame):
    """ GUI - app. Gives info about internet provider's balance (once per day),
        local weather (got from openweathermap.org) (every 15 mins by default).
    """
    
    def __init__(self, master, login, passwd, appid, delay = TIME_DELAY):
        super(Application, self).__init__(master)
        # delay in milisecons between requests, no sence to set it < 5sec(=5000ms)
        self.__delay = delay if delay > 5000 else 5000
        self.__login = login # provider's login
        self.__passwd = passwd # provider's passwd
        self.__appid = appid # APPID from openweathermap.org
        
        self.grid()
        
        self.__create_widget_balance()
        self.__create_widget_weather()
        
        
    def __create_widget_balance(self):
        """ Creates Label with balance of internet provider """
        prov = ProviderBalance(self.__login, self.__passwd)
        self.balance_lbl = Label(self, text = 'Balance:\n' + prov.balance)
        self.balance_lbl.grid(row = 0, rowspan = 2)
        
    
    def __create_widget_weather(self):
        """ Creates Label with weather data and last update time """
        # get local weather from openweathermap.org
        local_weather = get_weather(self.__appid)

        # create and drow Label of weather data
        self.weather_lbl = Label(self, text = local_weather)
        self.weather_lbl.grid(row = 10, rowspan = 4)

        # create and drow Label of update time
        self.time_lbl = Label(self, text='\nUpdate:\n{}'.format(time.strftime('%H:%M:%S')))
        self.time_lbl.grid(row = 20, rowspan = 3)
        # recursively call function to update weather data
        self.time_lbl.after(self.__delay, self.__create_widget_weather)

# main function
def main():
    root = Tk()
    root.title('Widget')
    root.geometry('120x200')
    app = Application(root, TIS_LOGIN, TIS_PASSWD, API_OpenWeather)
    root.mainloop()


main()    
