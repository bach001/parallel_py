#!/usr/bin/env python3

import urllib.request
from urllib.error import HTTPError, URLError
import time
from socket import timeout as net_timeout
from color_print import color_print


class net_connect:
    """ we can replace this module with another one """

    def __init__(self, tries=100):

        self.tries = tries
        self.print = color_print().color_print

        self.print("net_connect module __init__")

    # Retrieve a single page and report contents
    def read(self, url, timeout=60):
        for i in range(self.tries):
            try:
                self.print("@@ " + url)
                # dev tools console > document.characterSet
                html = urllib.request.urlopen(url, timeout=timeout).read().decode('utf-8')
            except (net_timeout, ConnectionResetError) as e:
                time.sleep(3)
                continue
            except (HTTPError, URLError) as e:
                print(e)
                return None
            else:
                # for line in html.split('\n'):
                return html

        self.print("net loop done")
        # with urllib.request.urlopen(url, timeout=timeout) as conn:
        #    return conn.read()
