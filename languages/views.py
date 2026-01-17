from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import languageList
from .serializers import LanguageListSerializer  

class LanguageListView(generics.ListAPIView):
    queryset = languageList.objects.all()
    serializer_class = LanguageListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response({
                'status': 404,
                'code': 0,
                'message': 'No languages found.',
                'data': []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 200,
            'code': 1,
            'message': 'Languages retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)