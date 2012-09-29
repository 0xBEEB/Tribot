APP_ID = 'MyTrimetAppId'
SERVER = "irc.cat.pdx.edu"
CHANNEL = "#trimet"
NICK = "tribot"
PORT = 6667

try:
    from local_settings import *
except ImportError:
    pass
