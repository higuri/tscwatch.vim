#!/usr/bin/env python3
#
# tscwatch.py
#

import re
from threading import Thread 
from subprocess import Popen, PIPE

if __name__ == '__main__':
    # for Debugging
    class Stub(): pass
    vim = Stub()
    vim.command = print
    vim.eval = lambda s: s
else:
    import vim

##
##  QuickFix
##
class QuickFix(object):

    # init()
    def init(self, title=''):
        # clear
        vim.command('call setqflist([], "r")')
        # set title
        vim.command('call setqflist([], "r", ' +
            '{"title": "%s"})' % title)

    # _escape()
    def _escape(self, s):
        return s.replace('\'', '\\\'').replace('"', '\\"')

    # open()
    def open(self):
        vim.command('copen')

    # close()
    def close(self):
        vim.command('cclose')

    # append()
    def append(self,
        filename='', line=0, col=0, desc=''):
        vim.command('call setqflist([{' +
                '"filename": "%s",' % (self._escape(filename)) +
                '"lnum": %d,' % (line) +
                '"col": %d,' % (col) +
                '"text": "%s"' % (self._escape(desc)) +
                '}], "a")')

##
##  TscWatchThread
##
class TscWatchThread(Thread):

    PAT_START = re.compile(
            r'\d{2}:\d{2}:\d{2} - .*Starting .*compilation.*\.\.\.')
    PAT_END = re.compile(
            r'\d{2}:\d{2}:\d{2} - Compilation complete\.')
    PAT_ERROR = re.compile(
            r'(.+)\((\d+),(\d+)\): (.*)')

    def __init__(self, cmds=[]):
        Thread.__init__(self)
        self.cmds = cmds
        self.proc = None

    def run(self):
        self.proc = Popen(self.cmds, stdout=PIPE, stderr=PIPE)
        procname = ' '.join(self.cmds)
        qf = QuickFix()
        qf.init(title=procname)
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
                qf.init(title=procname)
            elif self.PAT_END.search(s) is not None:
                if isTscFailed:
                    qf.open()
                else:
                    qf.close()
                    print('Done: %s' % procname)
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


##
##  TscWatchRunner
##
class TscWatchRunner(object):

    def __init__(self):
        self.tsc_thread = None

    # _is_running:
    def _is_running(self):
        return (self.tsc_thread is not None and
            self.tsc_thread.is_alive())

    # start:
    #  cmd: TypeScript compiler (e.g. 'tsc' or 'npx tsc')
    #  arg: argument string to tsc (e.g. 'foo.ts --noImplicitAny')
    def start(self, cmd='tsc', arg=''):
        if self._is_running():
            print('Already started')
            return
        # arg -> arg
        # * str -> list
        # * Vim variables (e.g. '%') -> value
        args = [vim.eval('expand("%s")' % s)
            for s in arg.split(' ') if s != '']
        cmds = cmd.split(' ') + ['--watch'] + args
        self.tsc_thread = TscWatchThread(cmds)
        self.tsc_thread.start()

    # stop:
    def stop(self):
        if self.tsc_thread is None:
            return
        if self.tsc_thread.is_alive():
            self.tsc_thread.stop()
            self.tsc_thread.join()
        self.tsc_thread = None

    # restart
    def restart(self):
        if self._is_running():
            cmds = self.tsc_thread.cmds
            self.stop()
            self.tsc_thread = TscWatchThread(cmds)
            self.tsc_thread.start()
        else:
            print('Not started')

    # is_running:
    def is_running(self):
        if self._is_running():
            print(1);
        else:
            print(0);


if __name__ == '__main__':
    tscwatch = TscWatchRunner()
    tscwatch.start('npx tsc', 'test.ts')
    input('')
    tscwatch.stop()
