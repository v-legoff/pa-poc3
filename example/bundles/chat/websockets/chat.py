from plugins.websocket.handler import WebSocketHandler

import cgi
import re

# Constants
VALID_PSEUDO = re.compile(r"^[A-Za-z0-9_.-]{4,12}$")

class Chat(WebSocketHandler):
    
    """Class containing the Chat web socket handler."""
    
    ws_point = "/ws"
    pseudos = {}
    functions = {
        "setpseudo": {"pseudo": str},
        "message": {"message": str},
    }
    
    def opened(self):
        """The connection has succeeded."""
        WebSocketHandler.opened(self)
        self.update_online()
    
    def closed(self, code, reason="A client left without explanation."):
        """The client closes the connection."""
        WebSocketHandler.closed(self, code, reason)
        if self in self.pseudos:
            pseudo = self.pseudos[self]
            del self.pseudos[self]
            self.send_to_connected(pseudo + " left the room.")
            self.update_online()
    
    def handle_setpseudo(self, pseudo):
        """Change the pseudo."""
        new = True
        if self in self.pseudos:
            old_pseudo = self.pseudos[self]
            new = False
        
        if self.can_use_pseudo(pseudo):
            self.pseudos[self] = pseudo
            self.send_JSON("setpseudo", pseudo=pseudo, newpseudo=new)
            self.update_online()
            if new:
                welcome = pseudo + " entered the room."
                self.send_message("You are now connected as {}.".format(pseudo))
                self.send_to_connected(welcome, self)
            elif old_pseudo != pseudo:
                message = old_pseudo + " is now known as " + pseudo + "."
                self.send_to_connected(message)
        
    def handle_message(self, message):
        """Handle the message function."""
        pseudo = self.pseudos.get(self)
        if pseudo is None:
            error = "You are not connected yet!"
            self.send_JSON("error", message=error)
            return
        
        message = "<" + pseudo + "> " + message
        self.send_to_connected(message)
    
    def update_online(self):
        """Send to all clients the number of connected clients."""
        pseudos = list(self.pseudos.values())
        pseudos.sort()
        for ws_handler in self.handlers:
            ws_handler.send_JSON("update_online", nb_online=len(self.pseudos),
                    pseudos=pseudos)
    
    def send_to_connected(self, message, *exceptions, escape=True):
        """Send a message to all connected clients.
        
        Note that, a connected client is not a connected socket.
        The chat clients are considered 'connected' when they have
        a pseudo set.
        
        """
        for ws_handler in self.pseudos:
            if ws_handler not in exceptions:
                ws_handler.send_message(message, escape=escape)
    
    def send_message(self, message, escape=True):
        """Send the message to the client using JSON.
        
        If 'escape' is True, the message will be escaped (<>&).
        
        """
        if escape:
            message = cgi.escape(message)
        
        self.send_JSON("message", message=message)
    
    def can_use_pseudo(self, pseudo):
        """Return whether this client can use this pseudo."""
        pseudos = [p.lower() for p in self.pseudos.values()]
        if pseudo.lower() in pseudos:
            self.send_JSON("error", message="This pseudo is already used.")
            return False
        
        if VALID_PSEUDO.search(pseudo) is None:
            self.send_JSON("error", message="This pseudo is not valid.")
            return False
        
        return True
