import sys
from threading import Thread
from google_trans_new import google_translator
from pyosc import Server, Client

class DownThread(Thread):
    def __init__(self, textinput, dest='en', osc_client=None):
        Thread.__init__(self)
        self.textinput = textinput
        self.dest = dest
        self.osc_client = osc_client
        print(self.dest, " <-- ", self.textinput)

    def run(self):
        translation = google_translator().translate(self.textinput, lang_tgt=self.dest)
        print(" --> ", translation)
        self.osc_client.send('/result',translation)

class GoogleTrans:

    def __init__(self, osc_server_port=7860, osc_client_host='127.0.0.1', osc_client_port=7861):
        self.dest = 'en'
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
        print("Translate", message)
        thd = DownThread(message, self.dest, self.osc_client);
        thd.start();

if __name__ == '__main__':

    print(google_translator().translate('สวัสดีจีน',lang_tgt='en'))
    if len(sys.argv) == 1:
        GoogleTrans();
    elif len(sys.argv) == 4:
        GoogleTrans(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        print('usage: %s <pyosc-server-port> <pyosc-client-host> <pyosc-client-port>')
