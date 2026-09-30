class Session:
    """
    Store the current authenticated user session
    and track failed login attempts.
    """

    def __init__(self):
        self.user = None
        self.failed_login_attempts = 0

    def login(self, user):
        """
        Store the authenticated user and reset
        failed login attempts.
        """
        self.user = user
        self.failed_login_attempts = 0

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

    def get_role(self):
        """
        Return the current user's role.
        """
        if not self.is_authenticated():
            return None

        return self.user.get("role")

    def is_admin(self):
        """
        Return True when the current user is an admin.
        """
        return self.get_role() == "admin"

    def record_failed_login(self):
        """
        Record one failed login attempt.
        """
        self.failed_login_attempts += 1

    def reset_failed_logins(self):
        """
        Reset failed login attempts.
        """
        self.failed_login_attempts = 0

    def get_failed_login_attempts(self):
        """
        Return the number of failed login attempts.
        """
        return self.failed_login_attempts
