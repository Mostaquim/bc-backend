from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User, OTP_CODES

from .serializers import UserSerializer
from .helpers import get_token, generateOTP


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class InitPhoneNumberView(APIView):
    permission_classes = ()

    def post(self, request):
        if 'phone_number' in request.data:
            otp = generateOTP()
            phone_number = request.data['phone_number']

            o = OTP_CODES.objects.filter(phone_number=phone_number)
            
            if o.exists():
                o = o[0]
                o.code = otp
                o.is_used = False
            else:
                o = OTP_CODES(phone_number=phone_number, code=otp)
                o.save()

            return Response({
                'status': 'otp'
            })

        return Response({
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)


class OTPView(APIView):
    permission_classes = ()

    def post(self, request):
        if 'phone_number' in request.data:
            phone_number = request.data['phone_number']

            user = User.objects.filter(phone_number=phone_number)
            if user.exists():
                user = user[0]
                user_serialized = UserSerializer(user)
                token = get_token(user)
                if user.is_active:
                    return Response({
                        'status': 'registered',
                        'user': user_serialized.data,
                        'token': token
                    })
                else:
                    return Response({
                        'status': 'not_active',
                        'user': user_serialized.data,
                        'token': token
                    })
            else:
                user = User.objects.create_user_phone(phone_number)
            return Response({
                'status': 'new_user',
                'user': user.pk
            })
        return Response({
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
