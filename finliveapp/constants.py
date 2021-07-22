
class UserType:
    SUPERUSER = "SUPERUSER"
    ADMIN = "ADMIN"
    VIEWER = "VIEWER"
    EDITOR = "EDITOR"

    @staticmethod
    def choices():
        return (
            (UserType.SUPERUSER, "Superuser"),
            (UserType.ADMIN, "Admin"),
            (UserType.EDITOR, "Editor"),
            (UserType.VIEWER, "Viewer"),
        )