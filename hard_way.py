from subprocess import PIPE, Popen, run
from NonBlockingStreamReader import NonBlockingStreamReader


try:
    run(['airmon-ng', 'check', 'kill'])
    run(['airmon-ng', 'start', 'wlan0'])

    dumpProc = Popen(['airodump-ng', 'wlan0mon'], stdout=PIPE)
    try:
        dumpReader = NonBlockingStreamReader(dumpProc.stdout)

        for _ in range(100):
            output = dumpReader.readline(0.1)
            print(output)
    finally:    
        dumpProc.terminate()

finally:
    run(['airmon-ng', 'stop', 'wlan0mon'])
    run(['service','NetworkManager','restart'])