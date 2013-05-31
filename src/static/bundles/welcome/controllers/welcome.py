from controller import Controller

class Welcome(Controller):

    def home(self):
        return self.render("{bundle}.home")
