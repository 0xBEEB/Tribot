import socket
import settings
import api

class IRCConnection():
    def __init__(self, channel=settings.CHANNEL):
        self.channel = channel
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ircsock.connect((settings.SERVER, settings.PORT))
        self.ircsock.send(
            "USER %s %s %s :This is a python bot\n" % (
                settings.NICK,
                settings.NICK,
                settings.NICK
            )
        )
        self.ircsock.send("NICK %s\n" % (settings.NICK,))

        self.joinchan(self.channel)

        quit = False
        while not quit:
            quit = self.eventLoop()

    def ping(self):
        self.ircsock.send("PONG :Pong\n")

    def sendmsg(self, chan, msg):
        self.ircsock.send("PRIVMSG %s :%s\n" % (chan, msg))

    def joinchan(self, chan):
        self.ircsock.send("JOIN %s\n" % chan)

    def hello(self):
        self.ircsock.send("PRIVMSG %s :Hello!\n" % (self.channel,))

    def usage(self):
        self.ircsock.send(
                "PRIVMSG %s :arrivals <stopid>, stopsby <address>\n" % (self.channel,)
            )

    def arrivals(self, command):
        stopID = command.strip('\n\r')

        arrivals = api.arrivals(stopID)

        for arrival in arrivals:
            self.ircsock.send(
                "PRIVMSG %s :%s\n" % (self.channel, arrival)
            )

    def stopsby(self, address):
        stops = api.stopsByAddr(address)

        for stop in stops:
            self.ircsock.send(
                "PRIVMSG %s :%s\n" % (self.channel, stop)
            )

    def eventLoop(self):
        ircmsg = self.ircsock.recv(2048).strip('\n\r')
        print(ircmsg)

        if ircmsg.find("PING :") != -1:
            self.ping()
        pm = ircmsg.find("PRIVMSG")
        if pm != -1:
            actMsg = ircmsg[pm + 8 + len(self.channel) + 2:]
            print actMsg
            if actMsg[:len(settings.NICK)] == settings.NICK:
                command = actMsg[len(settings.NICK) + 1:]
                if command[:5].lower() == "hello":
                    self.hello()
                elif command[:4].lower() == "help":
                    self.usage()
                elif command[:8].lower() == "arrivals":
                    self.arrivals(command[9:])
                elif command[:7].lower() == "stopsby":
                    self.stopsby(command[8:])
                elif command[:4].lower() == "quit":
                    return True

        return False


if __name__ == "__main__":
    connection = IRCConnection()
