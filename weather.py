import telebot
import pyowm
from pyowm.commons.exceptions import NotFoundError

# Initialize the OWM and the Telegram bot
owm = pyowm.OWM('')
bot = telebot.TeleBot("") 

@bot.message_handler(content_types=['text'])
def send_echo(message):
    mgr = owm.weather_manager()
    try:
        # Try to get weather data for the city
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        status = w.detailed_status

        # Formulate the response
        answer = f"In {message.text}, the temperature is {temp}°C and the weather is {status}.\n"

        # Provide clothing advice
        if temp < 10:
            answer += "Wear warm clothes like a coat."
        elif temp < 20:
            answer += "It's a bit chilly, wear something warm."
        else:
            answer += "It's warm, wear what you want."

    except NotFoundError:
        # If the city is not found, send an error message
        answer = "Sorry, I couldn't find the city you're looking for. Please check the spelling."

    # Send the response to the user
    bot.send_message(message.chat.id, answer)

# Start the bot
bot.polling(none_stop=True)

 