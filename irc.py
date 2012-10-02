import socket
import settings
import api

class IRCConnection():
    channel = settings.CHANNEL

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
            try:
                quit = self.eventLoop()
            except:
                pass


    def ping(self):
        self.ircsock.send("PONG :Pong\n")


    def sendmsg(self, chan, msg):
        self.ircsock.send("PRIVMSG %s :%s\n" % (chan, msg))


    def joinchan(self, chan):
        self.ircsock.send("JOIN %s\n" % chan)


    def hello(self, chan=None):
        if not chan:
            chan = self.channel

        self.ircsock.send("PRIVMSG %s :Hello!\n" % (chan,))


    def usage(self, chan=None):
        if not chan:
            chan = self.channel

        msg = "PRIVMSG %s :" % (chan,)
        msg += "help, "
        msg += "about, "
        msg += "arrivals <stopid>, "
        msg += "stopsby <address>, "
        msg += "lastSeen <stopID> <BusRoute>\n"
        self.ircsock.send(msg)


    def about(self, chan=None):
        if not chan:
            chan = self.channel

        msg_base = "PRIVMSG %s :" % (chan,)
        msg1 = msg_base + "Trilbot by Thomas Schreiber <thomas@ubiquill.com>\n"
        msg2 = msg_base + "Find me on github at http://github.com/ubiquill/tribot\n"
        msg3 = msg_base + "Try '\msg tribot help' for a list of commands\n"
        self.ircsock.send(msg1)
        self.ircsock.send(msg2)
        self.ircsock.send(msg3)


    def arrivals(self, command, chan=None):
        if not chan:
            chan = self.channel

        stopID = command.strip('\n\r')

        arrivals = api.getArrivals(stopID)

        if len(arrivals) > 0:
            for arrival in arrivals:
                self.ircsock.send(
                    "PRIVMSG %s :%s\n" % (chan, arrival)
                )
        else:
            self.ircsock.send(
                    "PRIVMSG %s :No results found\n" % (chan,)
                )


    def stopsby(self, address, chan=None):
        if not chan:
            chan = self.channel

        stops = api.stopsByAddr(address)

        if len(stops) > 0:
            for stop in stops:
                self.ircsock.send(
                    "PRIVMSG %s :%s\n" % (chan, stop)
                )
        else:
            self.ircsock.send(
                    "PRIVMSG %s :No results found\n" % (chan,)
                )


    def lastSeen(self, command, chan=None):
        if not chan:
            chan = self.channel

        args = command.split()

        if len(args) > 1:
            result = api.busLastSeen(args[0], args[1])
        else:
            result = "Sorry, no information found."

        self.ircsock.send(
                "PRIVMSG %s :%s\n" % (chan, result)
            )


    def eventLoop(self):
        ircmsg = self.ircsock.recv(2048).strip('\n\r')
        print(ircmsg)

        # Check if server is pinging
        if ircmsg.find("PING :") != -1:
            self.ping()

        # Is this a message I can see?
        pm = ircmsg.find("PRIVMSG")
        if pm != -1:
            command = ""

            startOffset = pm + 8 # Pos of "PRIVMSG" plus its len and a space
            endOffset = startOffset + len(settings.NICK)
            if ircmsg[startOffset:endOffset] == settings.NICK:
                # This is a priv msg
                username = ircmsg[1:ircmsg.find("!")]
                chan = username
                # Command is now just what the other party entered
                command = ircmsg[startOffset + len(settings.NICK) + 2:]
            else:
                # This is in the channel
                # actMsg is now what the other party entered
                actMsg = ircmsg[startOffset + len(self.channel) + 2:]

                # Am I being addressed?
                if actMsg[:len(settings.NICK)] == settings.NICK:
                    # Command without my nick and the following space
                    command = actMsg[len(settings.NICK) + 1:]
                    chan = self.channel

            if command != "":
                if command[:5].lower() == "hello":
                    self.hello(chan)
                elif command[:4].lower() == "help":
                    self.usage(chan)
                elif command[:5].lower() == "about":
                    self.about(chan)
                elif command[:8].lower() == "arrivals":
                    self.arrivals(command[9:], chan)
                elif command[:7].lower() == "stopsby":
                    self.stopsby(command[8:], chan)
                elif command[:8].lower() == "lastseen":
                    self.lastSeen(command[9:], chan)
                elif command.strip('\n\r') == settings.QUIT_CODE:
                    return True
                else:
                    self.ircsock.send(
                            "PRIVMSG %s :wat?\n" % (chan,)
                        )

        return False


if __name__ == "__main__":
    connection = IRCConnection()
