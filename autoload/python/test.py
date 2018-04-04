#!/usr/bin/env python3
#
# test.py
#

from threading import Thread 
from subprocess import Popen, PIPE

# TODO: cleanup
tscwatch_thread = None

# vim -> py -> 
#           -> th1 -> call tsc & wait 
class TscWatchThread(Thread):

    CMD = ['tsc', '--watch']

    def __init__(self, args):
        Thread.__init__(self)
        self.args = args
        self.proc = None

    def run(self):
        cmd = self.CMD + self.args
        self.proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        while True:
            try:
                line = self.proc.stdout.readline()
                if line == b'':
                    break
                s = line.decode('utf-8').strip()
                if s != '':
                    print(s)
            except:
                break

    def stop(self):
        self.proc.kill()

# tscwatch_start:
def tscwatch_start(args):
    global tscwatch_thread
    if tscwatch_thread:
        print('Already started')
    else:
        tscwatch_thread = TscWatchThread(args)
        tscwatch_thread.start()

# tscwatch_stop:
# TODO: autoexec stop on vim exit.
def tscwatch_stop():
    global tscwatch_thread
    if tscwatch_thread:
        tscwatch_thread.stop()
        tscwatch_thread.join()
        tscwatch_thread = None
    else:
        pass

'''
if __name__ == '__main__':
    tscwatch_start(['test.ts'])
    input('')
    tscwatch_stop()
'''
