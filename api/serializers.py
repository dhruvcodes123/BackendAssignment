from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from api.constants import EMAIL_REQUIRED_ERROR, EMAIL_NOT_UNIQUE, LOGIN_SUCCESS
from api.models import Post
from api.utils import get_tokens_for_user


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message=EMAIL_NOT_UNIQUE)],
        error_messages={'required': EMAIL_REQUIRED_ERROR, 'blank': EMAIL_REQUIRED_ERROR}
    )
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'username')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            raise serializers.ValidationError('Invalid email or password.') from e

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password.')

        token = get_tokens_for_user(user)
        data = {
            'refresh': token['refresh'],
            'access': token['access']        }

        return data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content_description', 'author', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.method == 'POST':
            self.fields.pop('author', None)
