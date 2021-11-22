#!/usr/bin/env python3

import os
import re
import sys
import subprocess
from multiprocessing import Process, Queue

from color_print import color_print
from date_help import date_help
from net_connect import net_connect


def worker(task, output):
    for task_type, task_url in iter(task.get, (None, None)):
        # if task[0] == 'html':
        #    self.search_html_link(task[1])
        #    output.put(task[1] + 'done')
        if task_type == 'audio':
            subprocess.run(["wget", "-nc", task_url])
            output.put(task_url + ' done')


class parallel_down:
    start_url = "https://www.dictionary.com/e/word-of-the-day/"
    html_regex = '(' + start_url + '[^"&#;]+\-([0-9]{4})\-([0-9]{2})\-([0-9]{2})/)'
    audio_regex = '(https://[^"&#;]+([0-9]{2})([0-9]{2})([0-9]{4}).*\.m4a)'

    def __init__(self, *args, **kwargs):

        # too many is not a good thing
        cpu_core = os.cpu_count()
        if cpu_core >= 8:
            self.workers = cpu_core // 2
        else:
            self.workers = cpu_core

        # create queues
        self.task_queue = Queue()
        self.done_queue = Queue()

        self.html_links = {}
        self.audio_links = {}

        self.print = color_print().color_print

        if not args:
            self.date_help = date_help()
        else:
            self.date_help = date_help(args[0], args[1])

        self.last_url = self.start_url
        self.last_date = self.date_help.sys_date()
        self.stop_date = self.date_help.stop_date()

        self.threads = [None] * self.workers

        # filename should be passed
        self.file = open(kwargs['file'], "a+")

    def search_page(self, html):

        res = re.findall(self.html_regex, html)
        for url, year, month, day in res:
            self.print("@page link .. " + url)
            page_date = year + month + day
            # using string compare to simplify things
            if page_date < self.last_date:
                self.last_date = page_date
                self.last_url = url

            if self.date_help.is_valid(year, month, day):
                if page_date not in self.html_links:
                    self.html_links[page_date] = url

    def search_audio(self, html):

        res = re.findall(self.audio_regex, html)
        for url, month, day, year in res:
            if self.date_help.is_valid(year, month, day):
                self.print('@@@ audio link ... ' + url)
                self.file.write(url + '\n')
                key = year + month + day
                if key not in self.audio_links:
                    self.audio_links[key] = url
                    self.task_queue.put(('audio', url))

    def search_html_link(self, url):

        net = net_connect()
        while True:
            self.print("@url .. " + url)
            self.print("@last_date .. " + self.last_date)
            self.print("@stop_date .. " + self.stop_date)
            if self.last_date <= self.stop_date:
                self.print("*** all collected ***")
                break
            self.print("### audio count " + str(len(self.audio_links)))

            html = net.read(url)
            if html:
                self.search_page(html)
                url = self.last_url
                self.search_audio(html)

    def search_audio_link(self):

        net = net_connect()
        for key, url in self.html_links.items():
            if key not in self.audio_links:
                html = net.read(url)
                self.search_audio(html)

    def main(self):

        self.search_html_link(self.last_url)
        # we need this
        self.search_audio_link()

        # done
        for i in range(self.workers):
            self.task_queue.put((None, None))

    def run(self):

        # Submit tasks
        # for task in urls:
        # print(task)
        #    task_queue.put(task)

        # Start worker processes
        for i in range(self.workers):
            self.threads[i] = Process(target=worker, args=(
                self.task_queue, self.done_queue))
            self.threads[i].start()

        self.main()

        self.file.close()

        # Get and print results
        # print('Unordered results:')
        # for i in range(len(urls)):
        #    print('\t', done_queue.get())

        # Add more tasks using `put()`
        # for task in TASKS2:
        #    task_queue.put(task)

        # Get and print some more results
        # for i in range(len(TASKS2)):
        #    print('\t', done_queue.get())

        # Tell child processes to stop
        # for i in range(workers):
        #    task_queue.put('STOP')

        # self.search_html_link()
        # self.search_audio_link()

        # for k, link in self.audio_links.items():
        #    print("download audio ...... " + link)
        #    subprocess.run(["wget", "-nc", link])

    def watch(self):
        pass
        # while True:
        #    self.print("audio link count " + str(len(self.audio_links)))
        #    self.print(self.done_queue.get())


if __name__ == '__main__':

    print(sys.argv)

    if len(sys.argv) >= 4:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        down = parallel_down(year, month, file=sys.argv[3])
    else:
        down = parallel_down(file=sys.argv[1])

    down.run()
    for i in range(down.workers):
        down.threads[i].join()
