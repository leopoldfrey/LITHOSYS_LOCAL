import sys
from threading import Thread
from googletrans import Translator
from pyosc import Server
from pyosc import Client

class DownThread(Thread):
    def __init__(self, textinput, dest='es', osc_client=None):
        Thread.__init__(self)
        self.textinput = textinput
        self.dest = dest
        self.osc_client = osc_client
        print(" <-- " + self.textinput)

    def run(self):
        translation = str(Translator().translate(self.textinput, dest=self.dest)).split("text=",1)[1].split(", pronunciation=")[0]
        print(" --> ", translation)
        self.osc_client.send('/result',translation)

class GoogleTrans:

    def __init__(self, osc_server_port=7860, osc_client_host='127.0.0.1', osc_client_port=7861):
        self.dest = 'es'
        self.osc_server = Server('127.0.0.1', osc_server_port, self.callback)
        self.osc_client = Client(osc_client_host, osc_client_port)

        print("GoogleTrans Ready")

    def callback(self, address, *args):
        if(address == '/dest'):
            self.dest = str(args[0])
            print ("-dest " + self.dest)
        elif(address == '/translate'):
            s = ""
            l = len(args)
            for x in range(0,l):
                s += str(args[x])
                if(x < (l-1)):
                    s += " "
            self.translate(s)
        else:
            print("callback : "+str(address))
            for x in range(0,len(args)):
                print("     " + str(args[x]))

    def translate(self, message):
        thd = DownThread(message, self.dest, self.osc_client);
        thd.start();

if __name__ == '__main__':
    if len(sys.argv) == 1:
        GoogleTrans();
    elif len(sys.argv) == 4:
        GoogleTrans(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        print('usage: %s <pyosc-server-port> <pyosc-client-host> <pyosc-client-port>')
