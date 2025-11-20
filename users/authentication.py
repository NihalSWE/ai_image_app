from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        user.user_type = validated_token.get("user_type")
        user.user_role = validated_token.get("user_role")
        return user
