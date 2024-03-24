from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    
    def create_user(self , email , password , **kwargs):
        
        if not email or not password :
            return ValueError("The email or pass is missing")
        
        email = self.normalize_email(email)
        user = self.model(email = email , **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    