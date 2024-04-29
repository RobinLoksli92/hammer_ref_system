from django.http import Http404
from rest_framework import generics, status
from rest_framework import authentication
from rest_framework.response import Response
from time import sleep

from .models import User
from .serializers import UserSerializer, UserProfileSerializer


class PhoneNumberLoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [authentication.BasicAuthentication]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        user, _ = User.objects.get_or_create(phone_number=phone_number)
        if user:
            sleep(3)
            return Response({'message': 'User authenticated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': ''}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self, phone_number):
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise Http404
        return user

    def get(self, request):
        user = self.get_object(phone_number=request.data['phone_number'])
        invited_users = [user for user in User.objects.filter(activated_invite_code=user.invite_code)]
        user.invited_users = invited_users
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = self.get_object(request.data['phone_number'])
        inputed_invite_code = request.data['invite_code']
        serializer = UserProfileSerializer(user, data=request.data)

        if user.activated_invite_code:
            return Response({'message': 'У вас уже есть активированный invite-код', 'invite_code': user.activated_invite_code})
        if inputed_invite_code == user.invite_code:
            return Response({'message': 'Вы не можете применить свой инвайт код.'})
        if inputed_invite_code not in User.objects.values_list('invite_code', flat=True):
            return Response({'message': 'Такого инвайт кода не существует.'})
        if serializer.is_valid():
            user.activated_invite_code = inputed_invite_code
            user.save()
            return Response({'message': 'Инвайт код применен.'})
