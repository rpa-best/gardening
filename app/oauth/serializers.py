from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken 
from .models import ChangePasswordUUID
from .validators import validate_phone

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "surname", "passport"]


class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "surname", "phone", "email"]


class ChangePasswordSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials"),
        "not_found_account": _("User not found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.SlugRelatedField(slug_field=self.username_field, queryset=User.objects.filter(is_active=True), write_only=True)
        self.fields['message'] = serializers.CharField(read_only=True)


    def validate(self, attrs):
        self.user = attrs[self.username_field]
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        self.user.send_reset_password()
        return {
            'message': _('Send message to email success')
        }


class ChangePasswordVerifySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uuid'] = serializers.SlugRelatedField(slug_field='uuid', queryset=ChangePasswordUUID.objects.all(), write_only=True)
        self.fields['message'] = serializers.CharField(read_only=True)

    def validate(self, attrs):
        uuid: ChangePasswordUUID = attrs['uuid']
        uuid.validate()
        return {
            'message': _('UUID verified')
        }


class ChangePasswordPerformSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uuid'] = serializers.SlugRelatedField(slug_field='uuid', queryset=ChangePasswordUUID.objects.all(), write_only=True)
        self.fields['password1'] = serializers.CharField(write_only=True)
        self.fields['password2'] = serializers.CharField(write_only=True)
        self.fields['message'] = serializers.CharField(read_only=True)

    def validate(self, attrs):
        password1: str = attrs.pop('password1')
        password2: str = attrs.pop('password2')
        uuid: ChangePasswordUUID = attrs['uuid']
        uuid.validate()
        if not password1 == password2:
            raise exceptions.ValidationError({'password2': [_("Passwords must be equels")]}, "password1_not_equel_password2")
        attrs['password'] = password1
        return attrs
    
    def create(self, validated_data):
        uuid: ChangePasswordUUID = validated_data.pop('uuid')
        uuid.change_password(**validated_data)
        return {
            "message": _('Password changed')
        }
    

class CreateUserLegalSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    phone = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    surname = serializers.CharField(write_only=True)
    message = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise exceptions.ValidationError([_('User with the given credentials already exists')])
        return value

    def validate(self, attrs):
        return attrs
    
    def validate_phone(self, value):
        return validate_phone(value)
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = RefreshToken().for_user(user)
        return {
            'message': _('Invite created'),
            'access': str(token.access_token),
            'refresh': str(token),
        }
