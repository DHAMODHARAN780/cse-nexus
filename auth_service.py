class AuthService:
    @staticmethod
    def validate_password(password):
        return len(password) >= 6

    @staticmethod
    def get_user_role_display(role):
        return "Administrator" if role == 'admin' else "Student"
