from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User, OTP_CODES

from .serializers import UserSerializer
from .helpers import get_token, generateOTP



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
                o.save()
            else:
                o = OTP_CODES(phone_number=phone_number, code=otp)
                o.save()

            return Response({
                'status': 'otp created'
            })

        return Response({
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)


class OTPView(APIView):
    permission_classes = ()

    def post(self, request):
        if 'phone_number' and 'otp' in request.data:
            phone_number = request.data['phone_number']
            otp_code = request.data['otp']

            otp = OTP_CODES.objects.filter(phone_number=phone_number, code=otp_code)
            
            if otp.exists():
                otp = otp[0]
                if otp.is_used:
                    return Response({
                        'status': 'error',
                        'message': 'OTP USED'
                    })
                otp.is_used = True
                otp.save()

                user = User.objects.filter(phone_number=phone_number)

                if user.exists():
                    
                    user = user[0]
                    token = get_token(user)
                    return Response({
                        'status': 'OK',
                        'user_registered': True,
                        'user': UserSerializer(user).data,
                        'token': token
                    })
                else:
                    user = User.objects.create_user_phone(phone_number)
                    token = get_token(user)
                    user.is_active = True
                    user.save()

                    return Response({
                        'status': 'OK',
                        'user_registered': False,
                        'user': UserSerializer(user).data,
                        'token': token
                    })

            else:
                return Response({
                    'status': 'error',
                    'message': 'Invalid OTP'
                })


            
        return Response({
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)



class UserUpdateView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request,  format=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['token'] = get_token(user)
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
