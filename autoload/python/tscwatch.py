#!/usr/bin/env python3
#
# tscwatch.py
#

import re
from threading import Thread 
from subprocess import Popen, PIPE

"""
class Stub(): pass
vim = Stub()
vim.command = print
"""

# TODO: cleanup
tscwatch_thread = None

# TscWatchQuickFix:
class TscWatchQuickFix(object):

    # init()
    def init(self, title=""):
        # clear
        vim.command('call setqflist([], "r")')
        # set title
        vim.command('call setqflist([], "r", ' +
            '{"title": "%s"})' % title)

    # open()
    def open(self):
        vim.command('copen')

    # close()
    def close(self):
        vim.command('cclose')

    # append()
    def append(self,
        filename="", line=0, col=0, desc=""):
        vim.command('call setqflist([{' +
                '"filename": "%s",' % (filename) +
                '"lnum": %d,' % (line) +
                '"col": %d,' % (col) +
                '"text": "%s"' % (desc) +
                '}], "a")')

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
        qf = TscWatchQuickFix()
        qf.init(title=' '.join(cmd))
        isTscFailed = False
        while True:
            line = self.proc.stdout.readline()
            if line == b'':
                break
            s = line.decode('utf-8').strip()
            if s == '':
                continue
            if self.PAT_START.search(s) is not None:
                isTscFailed = False
                qf.init(title=' '.join(cmd))
            elif self.PAT_END.search(s) is not None:
                if isTscFailed:
                    qf.open()
                else:
                    qf.close()
                    print('Done: %s' % ' '.join(cmd))
            else:
                if not isTscFailed:
                    isTscFailed = True
                m = self.PAT_ERROR.search(s)
                if m is not None:
                    # append error.
                    qf.append(
                        filename=m.group(1),
                        line=int(m.group(2)),
                        col=int(m.group(3)),
                        desc=m.group(4))
                else:
                    # unknown pattern
                    qf.append(desc=s)
                    qf.open()
            vim.command('redraw')

    def stop(self):
        self.proc.kill()

# _tscwatch_is_running:
def _tscwatch_is_running():
    global tscwatch_thread
    return (tscwatch_thread is not None and
        tscwatch_thread.is_alive())

# tscwatch_start:
def tscwatch_start(args):
    global tscwatch_thread
    if _tscwatch_is_running():
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

# tscwatch_is_running:
def tscwatch_is_running():
    if _tscwatch_is_running():
        print(1);
    else:
        print(0);

"""
if __name__ == '__main__':
    #  tscwatch_start(['test.ts'])
    tscwatch_start([])
    input('')
    tscwatch_stop()
"""
