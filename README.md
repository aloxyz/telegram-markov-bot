# telegram-markov-bot
This bot uses <a href="github.com/python-telegram-bot/python-telegram-bot">python-telegram-bot</a> and <a href="github.com/jsvine/markovify">markovify</a> to generate pseudo-random text based on context-specified markov chains given by command arguments.
`DB_PATH` specifies the directory where json files are located and then built to models. If not specified then no local models will be built.
### Usage
To start the bot:
`BOT_KEY="your key" DB_PATH='db' python3 bot.py`
