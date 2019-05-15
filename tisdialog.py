#
# __author__ = Pavel Egorov
#
import requests, json
from bs4 import BeautifulSoup


class ProviderBalance():
    """ Returns current balance of the given user from its 
        internet provider's cabinet.
        
        Works just for internet provider Tis-Dialog(Kaliningrad).
    """
    
    # user cabinet
    URL = 'https://stats.tis-dialog.ru/'
    
    def __init__(self, login: str, passwd: str):
        self.__balance = '--.--'
        self.__url = ProviderBalance.URL
        self.__login = login
        self.__passwd = passwd
    
        
    @property
    def balance(self):
        self.__update_balance()
        return self.__balance
    
    
    def __str__(self):
        return 'Баланс:\n{}'.format(self.balance)
        
    
    def __update_balance(self):
        html = self.__get_html(self.__url)
        balance = self.__get_balance(html)
        if balance != '':
            self.__balance = balance
        else:
            print('Не удалось получить баланс')
            
        
    def __get_html(self, url: str) -> str:
        """ Returns html-page after login. 
            
            Parameter:
            ----------
            url - type string, url of internet provider's cabinet
        """
        
        auth_data = {'login': self.__login, 'passv': self.__passwd}
        #header = {'User-Agent': generate_user_agent()}
        try:
            #response = requests.post(url, headers=header, data=auth_data)
            response = requests.post(url, data=auth_data)
            if response.ok:
                return response.text
            print('Error: {}', response.status_code)
            return ''
        except Exception as err:
            print(err)
            return ''
    
    
    def __get_balance(self, html: str) -> str:
        """ Returns balance of specified user.
            
            Parameter:
            ----------
            html - type string, html-page with balance information
        """
        try:
            soup = BeautifulSoup(html, 'lxml')
            #получить список строк и взять предпоследнюю
            balance = soup.find('table', {'class': 'lkInfoTable'}).findAll('tr')[-2] 
            # из последней ячейки взять число, отделенное от остального пробелом, 
            # и подготовить к конвертации во float  
            balance = balance.findAll('td')[-1].text.split()[0].replace(',', '.').strip() 
            return balance.strip()
        except Exception as err:
            print(err)
            return ''
###########################
###########################        
def get_geocoord():
    """ Returns latitude and longitude based on ip-address
    """
    # service provides the required data
    url = 'https://ipinfo.io/'
    # initial values of latitude and longitude
    lat, lon = .0, .0
    
    try:
        resp = requests.get(url)
        if resp.ok:
            data = resp.json()
            lat, lon = data['loc'].split(',')
    except Exception as err:
        print(err)

    return (float(lat), float(lon))
#    
#
def get_weather(appid: str) -> str:
    """ Returns current weather information from openweathermap.org.
        Personal ID is required to use site's API.
        
        Parameter:
        ----------
        appid - type is string, personal ID from openweathermap.org
    """
    # initial values for temperature, clouds, description, city name
    temp, clouds, descr, city_name = '-- ', '-- ', '---', '---'
    
    # get geo coordinates
    lat, lon = get_geocoord()
    
    # make url for request
    url = 'http://api.openweathermap.org/data/2.5/weather?' + \
          'lat={}&lon={}&units=metric&lang=ru&APPID={}'.format(lat, lon, appid)

    try:      
        resp = requests.get(url)
        if resp.ok:
            weather = json.loads(resp.text) # current weather data
            temp = weather['main']['temp'] # temperature
            clouds = weather['clouds']['all'] # clouds
            descr = weather['weather'][0]['description'] # description line
            city_name = weather['name'] # city name
    except Exception as err:
        print(err)

    return '\n{}\nТем-ра: {}C\nОблачность: {}%\n{}'.format(city_name, temp, clouds, descr)
