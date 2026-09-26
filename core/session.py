class Session:
    """
    Store the current authenticated user session.
    """

    def __init__(self):
        self.user = None

    def login(self, user):
        """
        Store the authenticated user.
        """
        self.user = user

    def logout(self):
        """
        Clear the current session.
        """
        self.user = None

    def is_authenticated(self):
        """
        Return True when a user is logged in.
        """
        return self.user is not None

    def get_username(self):
        """
        Return the current username.
        """
        if not self.is_authenticated():
            return None

        return self.user.get("username")
