import telebot, logging
from typing import Optional
from telebot.types import Document,Message
from tgh.hand import Tgh


name = "ImBotikBot"
token = "5323433052:AAGVd2Tiq6q_vv38cxFffkE6UHEb6TrJEBY"

logging.basicConfig(encoding='utf-8', format='%(asctime)s %(levelname)s %(message)s',  level=logging.DEBUG)

class Bot:

    def __init__(self):
        self.bot = telebot.TeleBot(f'{token}')
        text_handle = lambda msg: self.get_text_message(msg)
        doc_handle = lambda msg: self.get_doc(msg)

        self.bot.message_handler(content_types=['text'])(text_handle)
        self.bot.message_handler(content_types=['document'])(doc_handle)
        self.hand = Tgh(self.bot)

    def run(self):
        logging.info("Bot started polling")
        self.bot.polling(none_stop=True, interval=0)

    def get_text_message(self, message: Optional[Message]):
        try:
            logging.info(f" {message.from_user} recieved = {message}")
            if not self.hand.auth(message.from_user.id):
                return

#            if message.text.endswith(".torrent"):
#                logging.info(f" {message.from_user} recieved torrent URL = {message.text}")
#                self.hand.process_url(message.text)

            self.hand.process_url(message.text)

            self.bot.send_message(message.from_user.id, "Ok")
        except Exception as err:
            logging.error(err)


    def get_doc(self,message: Optional[Document]):
        try:
            if not self.hand.auth(message.from_user.id):
                return
            logging.info(f" {message.from_user} recieved file {message.document}")

            file_name: str = message.document.file_name
            if not file_name.endswith(".torrent"):
                logging.info(f" {message.from_user} unknown type of file {message.document}")
                self.bot.send_message(message.from_user.id, f"Dont know file type of {file_name}")

            self.hand.process_torrent(message.document)
            self.bot.send_message(message.from_user.id, "Processing started")

        except Exception as err:
            logging.error(err)


if __name__ == "__main__":
    Bot().run()