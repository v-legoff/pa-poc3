import cherrypy

from controller import Controller

class Chat(Controller):
    
    def index(self):
        return self.render("chat.index")
    
    def ws(self):
        pass
