from django.contrib.auth.models import User
from rest_framework import status, viewsets, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenBlacklistView
from api.constants import LOGIN_SUCCESS, LOGOUT_SUCCESS, REGISTER_SUCCESS, INVALID_CREDENTIALS, POSTED_SUCCESS
from api.models import Post
from api.serializers import LoginSerializer, RegisterSerializer, PostSerializer


class RegisterView(CreateAPIView):
    """
    API endpoint for registering new users.

    This view inherits from DRF's CreateAPIView which provides the default
    implementation for a 'POST' method handler to create an instance of the model.

    Attributes:
        queryset (QuerySet): The set of all User objects. While this is not directly
                             used for creating a new user, it's required for the base
                             view's get_object() method to function correctly.

        permission_classes (tuple): Specifies the permissions required to access the view.
                                    Here, any user (authenticated or not) is allowed to
                                    register a new account.

        serializer_class (class): Points to the serializer that's used to validate and
                                  transform the incoming request data.

    Methods:
        post(request, *args, **kwargs): Overrides the default post method to add a custom
                                        success message to the response after successful
                                        user registration.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data['message'] = REGISTER_SUCCESS
        return response


class LoginView(APIView):
    """
    API endpoint for user authentication.

    This view inherits from DRF's APIView and provides a custom implementation for the
    'POST' method handler, specifically tailored for user login functionality.

    Attributes:
        permission_classes (tuple): Specifies the permissions required to access the view.
                                    Here, any user (authenticated or not) is allowed to
                                    attempt logging in.

        serializer_class (class): Points to the serializer that's used to validate and
                                  transform the incoming login data.

    Methods:
        post(request, *args, **kwargs): Validates incoming login data and either responds
                                        with a success message and validated data upon
                                        successful authentication or with errors upon
                                        validation failure.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user login.

        Args:
            request (Request): DRF's Request object that contains the login data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: Upon successful validation and authentication, returns a success
                      message and the validated data. If validation fails, returns
                      relevant errors.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(data={'message': LOGIN_SUCCESS, 'token': serializer.validated_data},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(TokenBlacklistView):
    """
    API endpoint for user logout.

    This view inherits from DRF Simple JWT's TokenBlacklistView, which provides
    functionality to blacklist a given JWT token, effectively rendering it invalid
    for future requests. It is specifically tailored for user logout functionality,
    ensuring the token can't be used once the user logs out.

    Methods:
        post(request, *args, **kwargs): Blacklists the provided token and responds
                                        with a custom success message upon successful
                                        token invalidation.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user logout.

        The method blacklists the provided JWT token, rendering it unusable for future
        requests. This ensures the user is effectively logged out.

        Args:
            request (Request): DRF's Request object that contains the JWT token.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A Response object containing a success message indicating
                      that the user has been successfully logged out and their token
                      invalidated.
        """
        response = super().post(request, *args, **kwargs)
        response.data['message'] = LOGOUT_SUCCESS
        return response


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on the Post model.

    This viewset provides default implementations for 'list', 'create', 'retrieve',
    'update', and 'destroy' actions on the Post model. It inherits from DRF's
    ModelViewSet, and certain methods are overridden for custom functionality.

    Attributes:
        queryset (QuerySet): The set of all Post objects, to be used as the base of any
                             database query for the Post model.

        serializer_class (class): The serializer that's used to validate and transform
                                  data for the Post model.

        permission_classes (list): A list of permission classes that determine who can
                                   access this viewset. Here, only authenticated users
                                   are allowed.

    Methods:
        perform_create(serializer): Overrides the default method to set the 'author'
                                    field to the currently authenticated user during post
                                    creation.

        create(request, *args, **kwargs): Overrides the default 'create' method to add a
                                          custom success message in the response data after
                                          a successful post creation.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Override the default queryset to return only posts created by the currently logged-in user.
        """
        return Post.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        """
        Save the post instance with the currently authenticated user as the author.

        Args:
            serializer (Serializer): The serializer containing validated data for the
                                     Post instance.
        """
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new Post instance.

        After successful creation, it adds a custom success message to the response data.

        Args:
            request (Request): DRF's Request object that contains data for the new Post.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A Response object containing the created Post's data, and a success
                      message if the creation was successful.
        """
        response = super(PostViewSet, self).create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            response.data['message'] = POSTED_SUCCESS
        return response
