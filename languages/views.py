from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from songs.models import SongLyric
from songs.serializers import SongLyricSerializer
from .models import languageList
from .serializers import LanguageListSerializer  

# GET: /languages/songslist/
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
        
# GET: /songs/<id>/
class SongDetailView(generics.RetrieveAPIView):
    queryset = SongLyric.objects.all()
    serializer_class = SongLyricSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            "status": 200,
            "code": 1,
            "message": "Song details retrieved successfully.",
            "data": serializer.data
        })



# GET: /songs/search/?q=...
class SongSearchView(generics.ListAPIView):
    serializer_class = SongLyricSerializer

    def get_queryset(self):
        q = self.request.query_params.get('q', '').strip()
        if not q:
            return SongLyric.objects.none()

        return SongLyric.objects.filter(
            Q(song_no__icontains=q) |
            Q(song_name__icontains=q) |
            Q(song_title__icontains=q) |
            Q(song_lyric__icontains=q) |
            Q(priseWord__icontains=q)
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()

        if count == 0:
            return Response({
                "status": 404,
                "code": 0,
                "message": "No songs found matching your search.",
                "count": 0,
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "status": 200,
            "code": 1,
            "message": f"{count} song(s) found.",
            "count": count,
            "data": serializer.data
        })