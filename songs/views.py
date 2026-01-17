# songs/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import SongLyric
from .serializers import SongLyricSerializer


# GET: /songs/
class SongListView(generics.ListAPIView):
    queryset = SongLyric.objects.all().order_by('song_no')
    serializer_class = SongLyricSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():
            return Response({
                "status": 404,
                "code": 0,
                "message": "No songs found.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": 200,
            "code": 1,
            "message": "Songs retrieved successfully.",
            "data": serializer.data
        })


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
