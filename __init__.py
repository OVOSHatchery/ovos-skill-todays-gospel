import os
import subprocess
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from ovos_utils.file_utils import get_cache_directory
from ovos_utils.sound import play_audio as play_mp3
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill


class TodaysGospel(OVOSSkill):
    def initialize(self):
        self.p = None

    @intent_handler('gospel.todays.intent')
    def handle_gospel_todays(self, message):
        self.speak_dialog('gospel.todays')
        url = requests.get('https://evangeli.net/gospel')
        htmltext = url.text
        sp = BeautifulSoup(htmltext)
        mp3 = sp.find(title='listen').get('href')
        stream = '{}/stream'.format(get_cache_directory('TodaysGospelSkill'))
        # (Re)create Fifo
        if os.path.exists(stream):
            os.remove(stream)
        os.mkfifo(stream)
        self.log.debug('Running curl {}'.format(mp3))
        args = ['curl', '-L', quote(mp3, safe=":/"), '-o', stream]
        self.curl = subprocess.Popen(args)
        play_mp3(stream)
