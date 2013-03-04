import cherrypy

from controller import Controller

class User(Controller):
    
    def list(self):
        """Return the list of users."""
        ModUser = self.server.get_model("auth.User")
        return self.render("auth.user.list", users=ModUser.get_all())
    
    @Controller.model_id("auth.User")
    def view(self, user):
        user = user.display_representation(["id", "username"])
        return self.render("auth.user.view", user=user)
    
    def new(self):
        return self.render("auth.user.new")
    
    def create(self, username=None, password=None):
        """Create a user."""
        ModUser = self.server.get_model("auth.User")
        infos = {}
        if username:
            infos["username"] = username
        if password:
            infos["password"] = ModUser.hash_password(password, "sha1")
        infos["salt"] = ModUser.generate_salt()
        user = ModUser(**infos)
        user = user.display_representation(["id", "username"])
        return self.render("auth.user.view", user=user)
    
    @Controller.model_id("auth.User")
    def edit(self, user):
        user = user.display_representation(["id", "username"])
        return self.render("auth.user.edit", user=user)
    
    @Controller.model_id("auth.User")
    def update(self, user, username=None, password=None):
        if username:
            user.username = username
        if password:
            user.update_password(password)
        user = user.display_representation(["id", "username"])
        return self.render("auth.user.view", user=user)
    
    @Controller.model_id("auth.User")
    def delete(self, user):
        user.delete()
        raise cherrypy.HTTPRedirect("/users")
