import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather")
        self.setWindowIcon(QIcon("weather-icon.png"))   
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.button = QPushButton("Get Weather", self)
        self.weather_label = QLabel(self)
        self.temperature_label = QLabel("-", self)
        self.fltemperature_label = QLabel("Feels like: - ", self)
        self.emoji_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.button.clicked.connect(self.get_weather)
        self.city_input.setPlaceholderText("City Name")

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.fltemperature_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.weather_label.setAlignment(Qt.AlignCenter)

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.fltemperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.weather_label)

        # Background image
        self.bg_label = QLabel(self)
        pixmap = QPixmap("bg.jpg").scaled(self.size())  # Stretch to fit
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.lower()  # Send to back
        self.bg_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.bg_label.setStyleSheet("background-color: transparent;")

        self.city_label.setObjectName("city_label")
        self.fltemperature_label.setObjectName("fltemperature_label")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.weather_label.setObjectName("weather_label")
        self.button.setObjectName("button")
        self.city_input.setObjectName("city_input")
    
        self.setStyleSheet("""
                QPushButton, QLabel, QLineEdit { 
                    font-family: Calibri;
                    color: white;
                }

                QLabel#city_label {
                    font-size: 40px;
                    font-style: italic;
                }

                QLineEdit#city_input {
                    font-size: 30px;
                    color: black;
                }

                QPushButton#button {
                    font-size: 30px;
                    font-weight: bold;
                    color: black;
                }

                QLabel#temperature_label {
                    font-size: 60px;
                }

                QLabel#fltemperature_label {
                    margin-top: -25px;
                    padding-top: 0px;
                    font-size: 20px;
                }

                QLabel#emoji_label {
                    font-size: 90px;
                    font-family: 'Segoe UI Emoji';
                    background-color: transparent;
                }

                QLabel#weather_label {
                    font-size: 40px;
                    font-weight: bold;
                    font-style: italic;
                }
            """)
    def resizeEvent(self, event):
        # Resize background when window resizes
        self.bg_label.setPixmap(QPixmap("bg.jpg").scaled(self.size()))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
            
    def get_weather(self):
        # Tomorrow API
        # city = self.city_input.text()
        # api_key = "DjEy6FuDa2mnGkvG1oSjSgZf9Z64ZtY8"
        # url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={api_key}"

        #OpenWeatheMap API
        city = self.city_input.text()
        api_key = "c5d7f75a3fe671e2cd0ab433137d738b"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises error for 4xx/5xx responses

            weather_data = response.json()

            if response.status_code == 200:
                self.display_weather(weather_data)
            else:
                self.fltemperature_label.setText("⚠️ Unexpected error occurred.")
                self.temperature_label.setText(" ")
                self.emoji_label.setText("❓")

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                self.fltemperature_label.setText("📍Not Found")
                self.temperature_label.setText(" ")
                self.emoji_label.setText("❓")

            elif response.status_code == 401:
                self.fltemperature_label.setText("🔒Invalid Key")
                self.temperature_label.setText(" ")
                self.emoji_label.setText("❌")
            elif response.status_code == 429:
                self.fltemperature_label.setText("🚫Rate limit exceeded")
                self.temperature_label.setText(" ")
                self.emoji_label.setText("⏳")
            else:
                self.fltemperature_label.setText(f"⚠️HTTP error: {response.status_code}")
                self.temperature_label.setText(" ")
                self.emoji_label.setText("❓")

        except requests.exceptions.RequestException:
            self.fltemperature_label.setText("❌Network error")
            self.temperature_label.setText(" ")
            self.emoji_label.setText("📡")

    # Tomorrow API Weather Codes
    # @staticmethod
    # def get_emoji(weather_id):
    #     weather_emoji_map = {
    #                 0: "❓",              # Unknown
    #                 1000: "☀️",           # Clear, Sunny
    #                 1001: "☁️",           # Cloudy
    #                 1100: "🌤️",           # Mostly Clear
    #                 1101: "⛅",            # Partly Cloudy
    #                 1102: "🌥️",           # Mostly Cloudy
    #                 2000: "🌫️",           # Fog
    #                 2100: "🌁",           # Light Fog
    #                 4000: "🌦️",           # Drizzle
    #                 4001: "🌧️",           # Rain
    #                 4200: "🌦️",           # Light Rain
    #                 4201: "🌧️",           # Heavy Rain
    #                 5000: "❄️",           # Snow
    #                 5001: "🌨️",           # Flurries
    #                 5100: "🌨️",           # Light Snow
    #                 5101: "❄️",           # Heavy Snow
    #                 6000: "🌧️",           # Freezing Drizzle
    #                 6001: "🌧️",           # Freezing Rain
    #                 6200: "🌧️",           # Light Freezing Rain
    #                 6201: "🌧️",           # Heavy Freezing Rain
    #                 7000: "🧊",           # Ice Pellets
    #                 7101: "🧊",           # Heavy Ice Pellets
    #                 7102: "🧊",           # Light Ice Pellets
    #                 8000: "⛈️",           # Thunderstorm
    #             }
    #     return weather_emoji_map.get(weather_id, "❓")
    # @staticmethod
    # def get_description(weather_id):
    #     weather_emoji_map = {
    #                 0: "Unknown",
    #                 1000: "Clear, Sunny",
    #                 1100: "Mostly Clear",
    #                 1101: "Partly Cloudy",
    #                 1102: "Mostly Cloudy",
    #                 1001: "Cloudy",
    #                 2000: "Fog",
    #                 2100: "Light Fog",
    #                 4000: "Drizzle",
    #                 4001: "Rain",
    #                 4200: "Light Rain",
    #                 4201: "Heavy Rain",
    #                 5000: "Snow",
    #                 5001: "Flurries",
    #                 5100: "Light Snow",
    #                 5101: "Heavy Snow",
    #                 6000: "Freezing Drizzle",
    #                 6001: "Freezing Rain",
    #                 6200: "Light Freezing Rain",
    #                 6201: "Heavy Freezing Rain",
    #                 7000: "Ice Pellets",
    #                 7101: "Heavy Ice Pellets",
    #                 7102: "Light Ice Pellets",
    #                 8000: "Thunderstorm"
    #             }
    #     return weather_emoji_map.get(weather_id, "Unknown")
    
    #OpenWeatherMap
    @staticmethod
    def get_emoji(weather_id):
        weather_emoji_map = {
                # Thunderstorm (2xx)
                200: "⛈️", 201: "⛈️", 202: "⛈️", 210: "🌩️", 211: "🌩️", 212: "🌩️", 221: "🌩️", 230: "⛈️", 231: "⛈️", 232: "⛈️",

                # Drizzle (3xx)
                300: "🌦️", 301: "🌦️", 302: "🌦️", 310: "🌦️", 311: "🌦️", 312: "🌦️", 313: "🌦️", 314: "🌦️", 321: "🌦️",

                # Rain (5xx)
                500: "🌧️", 501: "🌧️", 502: "🌧️", 503: "🌧️", 504: "🌧️", 511: "🌧️🧊", 520: "🌦️", 521: "🌦️", 522: "🌦️", 531: "🌦️",

                # Snow (6xx)
                600: "🌨️", 601: "🌨️", 602: "🌨️", 611: "🌨️❄️", 612: "🌨️❄️", 613: "🌨️❄️", 615: "🌨️🌧️", 616: "🌨️🌧️",
                620: "🌨️", 621: "🌨️", 622: "🌨️",

                # Atmosphere (7xx)
                701: "🌫️", 711: "🌫️🚬", 721: "🌫️", 731: "🌬️🏜️", 741: "🌫️", 751: "🏜️", 761: "🌫️", 762: "🌋", 771: "🌬️", 781: "🌪️",

                # Clear & Clouds (800–804)
                800: "☀️", 801: "🌤️", 802: "⛅", 803: "🌥️", 804: "☁️"
                }
        return weather_emoji_map.get(weather_id, "❓")
    @staticmethod
    def get_description(weather_id):
        weather_description_map = {
                # Thunderstorm (2xx)
                200: "Thunderstorm with light rain",
                201: "Thunderstorm with rain",
                202: "Thunderstorm with heavy rain",
                210: "Light thunderstorm",
                211: "Thunderstorm",
                212: "Heavy thunderstorm",
                221: "Ragged thunderstorm",
                230: "Thunderstorm with light drizzle",
                231: "Thunderstorm with drizzle",
                232: "Thunderstorm with heavy drizzle",

                # Drizzle (3xx)
                300: "Light intensity drizzle",
                301: "Drizzle",
                302: "Heavy intensity drizzle",
                310: "Light intensity drizzle rain",
                311: "Drizzle rain",
                312: "Heavy intensity drizzle rain",
                313: "Shower rain and drizzle",
                314: "Heavy shower rain and drizzle",
                321: "Shower drizzle",

                # Rain (5xx)
                500: "Light rain",
                501: "Moderate rain",
                502: "Heavy intensity rain",
                503: "Very heavy rain",
                504: "Extreme rain",
                511: "Freezing rain",
                520: "Light intensity shower rain",
                521: "Shower rain",
                522: "Heavy intensity shower rain",
                531: "Ragged shower rain",

                # Snow (6xx)
                600: "Light snow",
                601: "Snow",
                602: "Heavy snow",
                611: "Sleet",
                612: "Light shower sleet",
                613: "Shower sleet",
                615: "Light rain and snow",
                616: "Rain and snow",
                620: "Light shower snow",
                621: "Shower snow",
                622: "Heavy shower snow",

                # Atmosphere (7xx)
                701: "Mist",
                711: "Smoke",
                721: "Haze",
                731: "Sand/dust whirls",
                741: "Fog",
                751: "Sand",
                761: "Dust",
                762: "Volcanic ash",
                771: "Squalls",
                781: "Tornado",

                # Clear & Clouds (800–804)
                800: "Clear sky",
                801: "Few clouds (11–25%)",
                802: "Scattered clouds (25–50%)",
                803: "Broken clouds (51–84%)",
                804: "Overcast clouds (85–100%)"
                }
        return weather_description_map.get(weather_id, "Unknown")
    
    def display_weather(self, weather_data):
        # weather_id = weather_data['data']['values']['weatherCode']
        # temperature = weather_data['data']['values']['temperature']
        # feels_like = weather_data['data']['values']['temperatureApparent']
        # emoji = self.get_emoji(weather_description)
        # description = self.get_description(weather_description)

        # self.emoji_label.setText(emoji)
        # self.weather_label.setText(description)
        # self.temperature_label.setText(f"{temperature}°C")
        # self.fltemperature_label.setText(f"Feels like: {feels_like}°C")

        # Extract values from OpenWeatherMap response
        weather_id = weather_data['weather'][0]['id']
        description = weather_data['weather'][0]['description'].capitalize()
        temperature = round(weather_data['main']['temp']) 
        feels_like = round(weather_data['main']['feels_like'])

        # Use your custom emoji and description functions
        emoji = self.get_emoji(weather_id)
        label_text = self.get_description(weather_id)

        # Update GUI labels
        self.emoji_label.setText(emoji)
        self.weather_label.setText(label_text or description)
        self.temperature_label.setText(f"{temperature}°C")
        self.fltemperature_label.setText(f"Feels like: {feels_like}°C")



        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = WeatherApp()
    clock.show()
    sys.exit(app.exec_())