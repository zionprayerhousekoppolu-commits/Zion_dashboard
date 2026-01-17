import secrets
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import AppUser, UserToken
from .serializers import AppUserSerializer, UserTokenSerializer
from languages.models import languageList


class SaveUser(APIView):
    """
    Create or update an AppUser. Returns the generated tokens on create/update.
    Expects multipart/form-data if profile image is included.
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        gmail = request.data.get("gmail")
        if not gmail:
            return Response({"success": False, "message": "Gmail is required"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = AppUser.objects.get_or_create(gmail=gmail)

        # Update fields from request (safe / partial)
        name = request.data.get("name")
        role = request.data.get("role")
        mobile = request.data.get("mobileNumber")
        age = request.data.get("age")

        if name is not None:
            user.name = name
        if role is not None:
            user.role = role
        if mobile is not None:
            user.mobileNumber = mobile
        if age is not None:
            try:
                user.age = int(age)
            except (ValueError, TypeError):
                pass

        # --- Default Telugu language: get or create ---
        telugu, _ = languageList.objects.get_or_create(
            languageCode="te",
            defaults={"languages": "Telugu", "is_active": True}
        )

        if created:
            user.prefered_language_for_dailyWord = telugu
        else:
            if not user.prefered_language_for_dailyWord:
                user.prefered_language_for_dailyWord = telugu

        # Update status
        user.is_login = True
        user.is_active = True
        user.is_logout = False

        # Accept profile file if provided
        profile_file = request.FILES.get("profile")
        if profile_file:
            user.profile = profile_file

        user.save()

        # Ensure a token object exists for this user (handle multiple tokens safely)
        token_qs = UserToken.objects.filter(user=user)
        token_obj = token_qs.first()
        if not token_obj:
            token_obj = UserToken.objects.create(user=user, access_token=secrets.token_hex(32))
        else:
            # If token is empty generate a new one
            if not token_obj.access_token:
                token_obj.access_token = secrets.token_hex(32)
                token_obj.save()

        serializer = AppUserSerializer(user, context={'request': request})
        return Response({
            "success": True,
            "created": created,
            "message": "User saved successfully",
            "token":token_obj.access_token,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# Saveing UserToken ==>
@method_decorator(csrf_exempt, name='dispatch')
class SaveUserToken(APIView):
    """
    Update tokens for a user. This is a separate endpoint used by clients to push tokens
    (e.g. after SaveUser returns tokens client saves locally and then calls this endpoint)
    """
    def post(self, request):
        gmail = request.data.get("gmail")
        access_token = request.data.get("access_token")

        if not gmail:
            return Response({"success": False, "message": "gmail required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = AppUser.objects.get(gmail=gmail)
        except AppUser.DoesNotExist:
            return Response({"success": False, "message": "user not found"}, status=status.HTTP_404_NOT_FOUND)

        # Find an existing token for the user or create one. Use filter().first() to avoid
        # MultipleObjectsReturned when multiple tokens exist for same user.
        token_qs = UserToken.objects.filter(user=user)
        token_obj = token_qs.first()
        if not token_obj:
            token_obj = UserToken.objects.create(user=user, access_token=access_token)
        else:
            token_obj.access_token = access_token or token_obj.access_token
            token_obj.save()

        serializer = UserTokenSerializer(token_obj)
        return Response({
            'status': status.HTTP_200_OK,
            'code': 1,
            "message": "Token saved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class GetUsers(APIView):
    def get(self, request):
        users = AppUser.objects.all().order_by("-created_at")
        serializer = AppUserSerializer(users, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'code': 1,
            'message': 'Users retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class GetUser(APIView):
    def get(self, request):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return Response({"status": 401, "message": "Invalid Authorization"}, status=status.HTTP_401_UNAUTHORIZED)

        token_value = auth.split("Bearer ")[1].strip()
        try:
            token = UserToken.objects.get(access_token=token_value)
        except UserToken.DoesNotExist:
            return Response({"status": 401, "message": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = AppUserSerializer(token.user, context={'request': request})
        return Response({
            "status": 200,
            "code": 1,
            "message": "User fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class UserUpdate(APIView):
    def put(self, request, id):
        try:
            user = AppUser.objects.get(id=id)
        except AppUser.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'code': 0,
                "message": "User not found",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AppUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'code': 1,
                "message": "User updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteAccount(APIView):
    def delete(self, request, id):
        try:
            user = AppUser.objects.get(id=id)
        except AppUser.DoesNotExist:
            return Response({"success": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({
            'status': status.HTTP_200_OK,
            'code': 1,
            "message": "User deleted successfully"
        }, status=status.HTTP_200_OK)


class UserLogout(APIView):
    def post(self, request, id):
        try:
            user = AppUser.objects.get(id=id)
        except AppUser.DoesNotExist:
            return Response({"success": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Invalidate all tokens for this user instead of assuming exactly one
        UserToken.objects.filter(user=user).update(access_token="")

        user.is_login = False
        user.is_logout = True
        user.save()

        return Response({
            'status': status.HTTP_200_OK,
            'code': 1,
            "message": "Logout successful. Tokens invalidated."
        }, status=status.HTTP_200_OK)