from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group, update_last_login


class UserSerializer(serializers.ModelSerializer):
    groups_name = serializers.SerializerMethodField(read_only=True)
    groups = serializers.CharField(source='groups.all.first.pk', required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    new_password_repeat = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'id', 'fullname', 'username', 'email', 'groups', 'new_password',
            'new_password_repeat', 'is_superuser', 'is_staff', 'groups_name', 'is_active',
            'created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_by', 'deleted_at', 'is_deleted')
        extra_kwargs = {
            'id': {'read_only': True},
            'groups_name': {'read_only': True}
        }

    def get_groups_name(self, obj):
        group = obj.groups.all().first()
        if group:
            return group.name
        return None


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'validators': []},
            'id': {'read_only': True}
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs["password"]

        if not email:
            raise ValidationError("Username or email is required to login.")
        user = User.objects.filter(is_deleted=False, email=email).distinct()

        user = user.exclude(email__isnull=True).exclude(email__iexact=' ').exclude(email__iexact='')

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username or email is not valid.")

        if user_obj:
            if not check_password(password, user_obj.password):
                raise ValidationError("Incorrect password or email.")

            else:
                data = {}
                attrs = super().validate(attrs)
                data['userid'] = self.user.id
                data['username'] = self.user.username
                data['fullname'] = self.user.fullname
                data['email'] = self.user.email
                data['permissions'] = self.user.user_permissions.values_list("codename", flat=True)
                data['is_staff'] = self.user.is_staff
                data['is_superuser'] = self.user.is_superuser
                data['refresh'] = attrs['refresh']
                data['access'] = attrs['access']
                data['groups'] = self.user.groups.values_list("name", flat=True)
                update_last_login(None, user_obj)

            return data

class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('new_password', 'new_password_repeat')