import logging, os

from telebot.types import Document
from jproperties import Properties


download_dir = "/tmp"
user = 397071083


class Tgh:

    def __init__(self, bot):
        self.bot = bot
        configs = Properties()
        with open('tgh.properties', 'rb') as read_prop:
            configs.load(read_prop)

        self.user = int(configs.get("USER").data)
        self.path = configs.get("PATH").data


    def auth(self, user_id: str) -> bool:
        return self.user == user_id

    def process_torrent(self, doc: Document):
        file_name: str = doc.file_name
        file_id = doc.file_id
        file_id_info = self.bot.get_file(doc.file_id)
        downloaded_file = self.bot.download_file(file_id_info.file_path)

        if file_name.endswith(".torrent"):
            with open(self.path + "/" + file_name, "wb") as fd:
                fd.write(downloaded_file)

    def process_url(self, url: str):
        try:
            cmd = f"transmission-remote -a  {url}"
            os.system(cmd)
        except Exception as ex:
            logging.error(f"{cmd}")








