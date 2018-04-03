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

    def __init__(self, arg):
        Thread.__init__(self)
        self.arg = arg
        self.proc = None

    def run(self):
        cmd = self.CMD + [self.arg]
        self.proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        while True:
            try:
                line = self.proc.stdout.readline()
                if line != b'':
                    s = line.strip()
                    if s != b'':
                        print(s)
                else:
                    break
            except:
                break

    def stop(self):
        self.proc.kill()

# tscwatch_start:
def tscwatch_start(arg):
    global tscwatch_thread
    tscwatch_thread = TscWatchThread(arg)
    tscwatch_thread.start()

# tscwatch_stop:
def tscwatch_stop():
    global tscwatch_thread
    tscwatch_thread.stop()
    tscwatch_thread.join()

"""
if __name__ == '__main__':
    tscwatch_start('test.ts')
    input('')
    tscwatch_stop()
"""
