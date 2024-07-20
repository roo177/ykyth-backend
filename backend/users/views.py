from rest_framework import viewsets, generics
from .serializers import UserSerializer, GroupSerializer, MyTokenObtainPairSerializer,ChangePasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.models import Group
from helper.pagination import StandardResultsSetPagination, LargeResultsSetPagination
from helper.responseProcess.ResponseHelper import *
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from helper.responseProcess.ResponseHelper import *
from helper.responseProcess.ResponseInfo import *
from users.models import User
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return get_not_found_response()
        serializer = self.serializer_class(user)
        data = serializer.data
        user.delete()
        
        return get_deleted_successfully_response(data)
    

class UserViewSet(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = StandardResultsSetPagination
    
    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def get_queryset(self):

        fields = {
            'email': self.request.query_params.get('email'),
            'username': self.request.query_params.get('username'),
            'fullname': self.request.query_params.get('fullname')
        }
        queryset = User.objects.filter(is_deleted=False)
        

        if fields['email']:
            queryset = queryset.filter(email__icontains=fields['email'])

        if fields['username']:
            queryset = queryset.filter(username__icontains=fields['username'])

        if fields['fullname']:
            queryset = queryset.filter(fullname__icontains=fields['fullname'])

        return queryset
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.request.query_params.get('page')
            
            if page is not None:
                queryset = self.paginate_queryset(queryset)
                serializer = self.get_serializer(queryset, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = {
                    'data': serializer.data,
                    'count': queryset.count(),
                }
                return get_list_successfully_response(request.GET, data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)

        
    def create(self, request, *args, **kwargs):
        try:
            email = User.objects.filter(is_deleted=False, email__exact=self.request.data['email'])
            if email.exists():
                return get_already_email_error_response()

            if self.request.data['password'] != self.request.data['password_repeat']:
                return get_new_password_error_response()

            data = {
                "username": request.data['username'],
                "email": request.data['email'],
                "fullname": request.data['fullname'],
                "group": request.data['group'],
                "created_by_id": request.user.id,
                "is_active": request.data.get('is_active', True),
                "is_superuser": request.data.get('is_superuser', False),
                "is_staff": request.data.get('is_staff', False),
                "password": request.data['password'],
                "password_repeat": request.data['password_repeat']
            }

            user_data = {
                'username': data['username'],
                'email': data['email'],
                'fullname': data['fullname'],
                'created_by_id': data['created_by_id']
            }

            user, created = User.objects.get_or_create(email=user_data['email'], defaults=user_data)

            if created:
                if data['group']:
                    user.groups.add(data['group'])
            else:
                # print("reactivating user_data:", user_data)
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.is_deleted = False
                
            user.is_active = data['is_active']
            user.is_superuser = data['is_superuser']
            user.is_staff = data['is_staff']
            user.set_password(data['password'])
            user.save()

            return get_created_successfully_response(data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)


    def perform_update(self, serializer):
        user = User.objects.filter(pk=self.request.user.id).first()
        serializer.save(updated_by=user)

    def update(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(pk=self.request.user.id).first()
            group = self.request.data['group']
            if user and group:
                user.groups.clear()
                user.groups.add(int(group))

            return get_updated_successfully_response(super().update(request, *args, **kwargs).data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)

    def destroy(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(pk=self.request.user.id).first()
            user_obj = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
            user_obj.deleted_at = timezone.now()
            user_obj.is_deleted = True
            user_obj.deleted_by = user
            user_obj.save()

            return get_deleted_successfully_response(self.serializer_class(user_obj).data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)

    def retrieve(self, request, *args, **kwargs):
        try:
            return get_detail_successfully_response(super().retrieve(request, *args, **kwargs).data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)



class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = LargeResultsSetPagination
    

    def get_queryset(self):

        queryset = Group.objects.all()

        return queryset



    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.request.query_params.get('page')
            
            if page is not None:
                queryset = self.paginate_queryset(queryset)
                serializer = self.get_serializer(queryset, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = {
                    'data': serializer.data,
                    'count': queryset.count(),
                }
                return get_list_successfully_response(request.GET, data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)

    def create(self, request, *args, **kwargs):
        try:
            return get_created_successfully_response(super().create(request, *args, **kwargs).data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)

    def update(self, request, *args, **kwargs):
        try:
            return get_updated_successfully_response(super().update(request, *args, **kwargs).data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)

    def destroy(self, request, *args, **kwargs):
        try:
            return get_deleted_successfully_response(super().destroy(request, *args, **kwargs).data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)

    def retrieve(self, request, *args, **kwargs):
        try:
            return get_detail_successfully_response(super().retrieve(request, *args, **kwargs).data)
        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)


# Create your views here.
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']
        
        # Set tokens in cookies
        response.set_cookie(
            'access', 
            access, 
            httponly=True, 
            secure=True, 
            samesite='Lax'
        )
        response.set_cookie(
            'refresh', 
            refresh, 
            httponly=True, 
            secure=True, 
            samesite='Lax'
        )
        return response



class ChangePasswordView(generics.UpdateAPIView):
    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        # self.object = self.get_object()
        try:
            new_password = self.request.data.get('new_password')
            new_password_repeat = self.request.data.get('new_password_repeat')
        
        except (Exception) as exp:
            return get_bad_request_message_response(exp)
        
        if new_password is None or new_password_repeat is None:
            return get_provide_password_error_response()

        if new_password != new_password_repeat:
            return get_new_password_error_response()
     
        self.object = User.objects.filter(pk=kwargs['pk']).first()
        serializer = self.get_serializer(data=self.request.data)
        

        try:
            if serializer.initial_data['new_password'] != serializer.initial_data['new_password_repeat']:
                return get_new_password_error_response()

            # if not self.object.check_password(serializer.initial_data['old_password']):
            #     return get_old_error_response()
            self.object.set_password(serializer.initial_data['new_password'])
            self.object.save()

            return get_change_password_successfully_response()

        except (ValidationError, IntegrityError) as exp:
            return get_bad_request_message_response(exp)

