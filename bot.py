#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import langdetect 
import pyphen

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

pyphen.language_fallback('ru')

def start(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /start is issued."""
	if(update.message.from_user.language_code == 'ru'):
		update.message.reply_text('Привет! Этот бот автоматически формирует хайку/хокку в ответ на 17 слоговые сообщения.')
	else:
		update.message.reply_text('Hi! This bot automatically generates haiku/hokku in response to 17 syllable messages.')

def haikudetect(update: Update, context: CallbackContext) -> None:
	message = update.message.text
	words = message.split()
	# Checking words count
	if (len(words) < 3 or len(words) > 17): return
	# Loading pyphen dictionary
	dic = pyphen.Pyphen(lang=langdetect.detect(message))
	# Counting syllables
	syllable_count_in_message = 0
	syllable_count = 0
	line = 0
	haiku = ""
	for word in words:
		syllable_count += len(dic.inserted(word).split("-"))
		haiku += word + " "
		# First line must have 5 syllables, second 7 and third 5.
		if (((syllable_count >= 5) and (line % 2 == 0)) or ((syllable_count >= 7) and (line % 2 != 0))): 
			haiku += "\n"
			line += 1
			syllable_count_in_message += syllable_count
			syllable_count = 0
	# Checking for sallyables count in message
	if (syllable_count_in_message < 16 or syllable_count_in_message > 18): return
	# Appending author 
	try:
		haiku += "\n— " + update.message.from_user.first_name + " " + update.message.from_user.last_name
	except:
		haiku += "\n— @" + update.message.from_user.username
	# Posting haiku
	update.message.reply_text(haiku)

def main():
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater(config.telegram_token, use_context=True)

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(MessageHandler(Filters.text, haikudetect))

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
