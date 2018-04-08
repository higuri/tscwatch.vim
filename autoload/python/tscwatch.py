#!/usr/bin/env python3
#
# tscwatch.py
#

import re
from threading import Thread 
from subprocess import Popen, PIPE

# TODO: cleanup
tscwatch_thread = None

# TscWatchThread:
class TscWatchThread(Thread):

    CMD = ['tsc', '--watch']
    PAT_START = re.compile(
            r'\d{2}:\d{2}:\d{2} - .*Starting .*compilation.*\.\.\.')
    PAT_END = re.compile(
            r'\d{2}:\d{2}:\d{2} - Compilation complete\.')
    PAT_ERROR = re.compile(
            r'(.+)\((\d+),(\d+)\): (.*)')

    def __init__(self, args):
        Thread.__init__(self)
        self.args = args
        self.proc = None

    def run(self):
        cmd = self.CMD + self.args
        self.proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        isTscFailed = False
        while True:
            try:
                line = self.proc.stdout.readline()
                if line == b'':
                    break
                s = line.decode('utf-8').strip()
                if s == '':
                    continue
                if self.PAT_START.search(s) is not None:
                    isTscFailed = False
                    # clear
                    vim.command('call setqflist([], "r")')
                    # set title
                    vim.command('call setqflist([], "r", ' +
                        '{"title": "%s"})' % ' '.join(cmd))
                elif self.PAT_END.search(s) is not None:
                    if isTscFailed:
                        vim.command('copen')
                    else:
                        print('[OK] %s' % ' '.join(cmd))
                else:
                    if not isTscFailed:
                        isTscFailed = True
                    m = self.PAT_ERROR.search(s)
                    if m is not None:
                        # add error item
                        vim.command('call setqflist([{' +
                                '"filename": "%s",' % (m.group(1)) + 
                                '"lnum": %s,' % (m.group(2)) +
                                '"col": %s,' % (m.group(3)) + 
                                '"text": "%s"' % (m.group(4)) +
                                '}])')
                    else:
                        # unknown pattern
                        vim.command('caddexpr "%s"' % s)
                vim.command('redraw')
            except:
                break

    def stop(self):
        self.proc.kill()

# tscwatch_start:
def tscwatch_start(args):
    global tscwatch_thread
    if tscwatch_thread and tscwatch_thread.is_alive():
        print('Already started')
        return
    tscwatch_thread = TscWatchThread(args)
    tscwatch_thread.start()

# tscwatch_stop:
def tscwatch_stop():
    global tscwatch_thread
    if tscwatch_thread is None:
        return
    if tscwatch_thread.is_alive():
        tscwatch_thread.stop()
        tscwatch_thread.join()
    tscwatch_thread = None

"""
if __name__ == '__main__':
    tscwatch_start(['test.ts'])
    input('')
    tscwatch_stop()
"""
