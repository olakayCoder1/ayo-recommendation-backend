from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.models import User


class AccountProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_admin', 'created_at', 'role')

    def get_role(self, obj):
        # Check if the user is an admin, then assign the role as "admin", otherwise "user"
        return "admin" if obj.is_admin else "user"

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        # Check that new passwords match
        if data['new_password'] != data['confirm_new_password']:
            raise ValidationError("New passwords do not match.")
        return data
    



class UpdateTwoFactorAuthenticationRequestSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=(
        ('enable', 'Enable'),
        ('disable', 'Disable')
    ))
