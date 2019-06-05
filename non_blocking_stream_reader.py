# Taken from
# http://eyalarubas.com/python-subproc-nonblock.html


from threading import Thread
from queue import Queue, Empty


class NonBlockingStreamReader:

    def __init__(self, process):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''

        self._p = process
        self._q = Queue()

        def _populate_queue(proc, queue):
            '''
            Collect lines from 'stream' and put them in 'queue'.
            '''

            while True:
                line = proc.stdout.readline()
                if line:
                    queue.put(line)
                #else:
                #    raise UnexpectedEndOfStream

        self._t = Thread(target=_populate_queue, args=(self._p, self._q))
        #self._t.daemon = True
        self._t.start() #start collecting lines from the stream


    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None, timeout = timeout)
        except Empty:
            # return None
            return "04:18:D6:8D:7E:7B  -52       35        0    0   1   54  OPN              Build"


class UnexpectedEndOfStream(Exception):
    pass
