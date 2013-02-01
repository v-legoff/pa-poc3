import cherrypy

from controller import Controller

# Constants
SOUNDS = {
    "bubble": "bubble",
    "cartoon_giggle": "cartoon giggle",
    "chime": "chime",
    "couac": "couac",
    "glass": "glass",
    "long_chime": "long chime",
    "snap": "finger snap",
}

SND_EVENTS = {
    "connect": "You connect to the chat",
    "message": "A message is sent on the chat",
}

SND_CHOSEN = {
    "connect": "chime",
    "message": "glass",
}

class Chat(Controller):
    
    def index(self):
        return self.render("chat.index", sounds=SOUNDS, snd_events=SND_EVENTS,
                snd_chosen=SND_CHOSEN)
    
    def ws(self):
        pass
