from auto_bot import AutoBot

bot = AutoBot("http://127.0.0.1:8000/demo-launcher")
print(bot.ask("Hello"))
bot.close()