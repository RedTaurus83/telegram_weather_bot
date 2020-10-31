from pyowm.owm import OWM
import telebot
from pyowm.utils.config import get_default_config
import datetime


config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('3171d33eb8ec7865bab3cac0af96ee01', config_dict)
bot = telebot.TeleBot("1075949051:AAETVjmXII-N5QAd-jzJv3ahZRxORqvKJNk")


@bot.message_handler(content_types=['text'])
def send_echo(message):
    if message.text[0] == '/':
        message.text = message.text[1:]
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(message.text)
    weather = observation.weather
    wind_speed = weather.wind()['speed']
    temp = weather.temperature('celsius')["temp"]
    sunrise = weather.sunrise_time(timeformat='date')
    sunset = weather.sunset_time(timeformat='date')
    h3_forecast = mgr.forecast_at_place(message.text, '3h').forecast
    current_time = datetime.datetime.now().time()
    print(current_time.strftime('%H:%M:%S'))
    time_03 = datetime.datetime.strptime('03:00:00', '%H:%M:%S').time()
    time_06 = datetime.datetime.strptime('06:00:00', '%H:%M:%S').time()
    time_09 = datetime.datetime.strptime('09:00:00', '%H:%M:%S').time()
    time_12 = datetime.datetime.strptime('12:00:00', '%H:%M:%S').time()
    time_15 = datetime.datetime.strptime('15:00:00', '%H:%M:%S').time()
    time_18 = datetime.datetime.strptime('18:00:00', '%H:%M:%S').time()
    time_21 = datetime.datetime.strptime('21:00:00', '%H:%M:%S').time()
    timestamps = [time_03, time_06, time_09, time_12, time_15, time_18, time_21]
    counter = 8
    hour_forecast = []
    for t in timestamps:
        if t < current_time:
            counter -= 1
    for weathers in h3_forecast:
        hour_forecast.append(
            str(weathers.reference_time(timeformat='date').time()) + ": " + str(weathers.detailed_status)
            + ", температура воздуха: " +
            str(weathers.temperature('celsius')["temp"]) + "°C.\n")
        counter -= 1
        if counter == 0:
            break
    for i in hour_forecast:
        print(i)
    answer = "Всё время отображается в формате UTC.\n"
    answer += "В городе " + message.text + " сейчас " + weather.detailed_status + "." + "\n"
    answer += "Текущая температура " + str(temp) + "°." + "\n"
    answer += "Скорость ветра: " + str(wind_speed) + " м/с.\n"
    answer += "Восход солнца сегодня в " + str(sunrise.time()) + " , а заход в " + str(sunset.time()) + "\n"
    answer += "Погода на остаток дня:\n"
    for i in hour_forecast:
        answer += i

    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
