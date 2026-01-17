# views.py
from datetime import date
import hashlib
from rest_framework import generics, status
from rest_framework.response import Response


from appusers.models import UserToken
from .models import languageList, BibleBook, Verse
from .serializers import BibleBookSerializer, BibleVerseSerializer
from django.db.models import Q
from rest_framework.views import APIView


# GET: /<language_code>/biblelist/
class BibleListByLanguageView(generics.ListAPIView):
    serializer_class = BibleBookSerializer

    def get_queryset(self):
        language_code = self.kwargs['language_code']
        return BibleBook.objects.filter(bibleLanguage__languageCode=language_code)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        language_code = self.kwargs['language_code']

        # 1. First: check if language exists (one query)
        language = languageList.objects.filter(languageCode=language_code).first()

        if not language:
            return Response({
                'status': 404,
                'code': 0,
                'message': 'Language not found.',
                'data': {
                    'category': language_code.upper(),
                    'bibleList': []
                }
            }, status=status.HTTP_404_NOT_FOUND)
            
        # 2. Now get the books
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)

        data = {
            'id': language.id,
            'category': language.languages,
            'bibleList': serializer.data  # even if empty, it's fine
        }

        # Only if language exists but has no books → still return success (or optional 404)
        if not serializer.data:
            return Response({
                'status': 404,
                'code': 0,
                'message': f'Bible books not available in {language.languages} yet.',
                'data': data
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'status': 200,
            'code': 1,
            'message': 'Bible list retrieved successfully.',
            'data': data
        })

        return Response({
            'status': 200,
            'code': 1,
            'message': 'Bible list retrieved successfully.',
            'data': data
        })


# GET: /<book_id>/verses/
class BibleVersesByBookView(generics.ListAPIView):
    serializer_class = BibleVerseSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']          # ← changed here
        return Verse.objects.filter(book_id=book_id).select_related('book')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({
                'status': 404,
                'code': 0,
                'message': 'Bible verses not found for this book.',
                'data': []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 200,
            'code': 1,
            'message': 'Bible verses retrieved successfully.',
            'data': serializer.data
        })
        
        
# GET: /search/?q=...&lang=...&book=...&chapter=...
class VerseSearchView(generics.ListAPIView):
    serializer_class = BibleVerseSerializer
    # Optional: order results logically
    ordering = ['book__booknumber', 'no_of_chapter', 'no_of_verses']

    def get_queryset(self):
        queryset = Verse.objects.select_related('book__bibleLanguage').all()

        # 1. Search term (required)
        q = self.request.query_params.get('q', '').strip()
        if not q:
            return Verse.objects.none()

        # Works on ALL databases: SQLite, MySQL, PostgreSQL
        queryset = queryset.filter(
            Q(verses__icontains=q)
        )

        # Optional filters
        lang = self.request.query_params.get('lang')
        if lang:
            queryset = queryset.filter(book__bibleLanguage__languageCode__iexact=lang.strip())

        book_id = self.request.query_params.get('book')
        if book_id:
            try:
                queryset = queryset.filter(book_id=int(book_id))
            except ValueError:
                pass

        chapter = self.request.query_params.get('chapter')
        if chapter:
            try:
                queryset = queryset.filter(no_of_chapter=int(chapter))
            except ValueError:
                pass

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()

        if count == 0:
            return Response({
                "status": 404,
                "code": 0,
                "message": "No verses found matching your search.",
                "count": 0,
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})

        return Response({
            "status": 200,
            "code": 1,
            "message": f"{count} verse(s) found.",
            "count": count,
            "data": serializer.data
        })
        
# GET: /bible/verse-of-the-day/
class VerseOfTheDayView(APIView):
    """
    GET /bible/verse-of-the-day/
    Optional: Authorization: Bearer <token>
    """

    def get(self, request, language_code=None):
        selected_language_code = None

        # 1️⃣ Token-based language
        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token_value = auth.replace("Bearer ", "").strip()
            token = UserToken.objects.select_related(
                "user__prefered_language_for_dailyWord"
            ).filter(access_token=token_value).first()

            if token and token.user.prefered_language_for_dailyWord:
                selected_language_code = token.user.prefered_language_for_dailyWord.languageCode.lower()

        # 2️⃣ URL-based language
        if not selected_language_code and language_code:
            selected_language_code = language_code.lower()

        # 3️⃣ Default language
        selected_language_code = selected_language_code or "en"

        # Fetch language safely
        language = languageList.objects.filter(
            languageCode__iexact=selected_language_code
        ).first()

        if not language:
            language = languageList.objects.get(languageCode__iexact="en")
            selected_language_code = "en"

        verses = Verse.objects.filter(
            book__bibleLanguage=language
        ).select_related("book").order_by("id")

        if not verses.exists():
            return Response({
                "status": 404,
                "code": 0,
                "message": f"No verses available in {language.languages}.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        today = date.today().isoformat()
        seed = f"{today}:{selected_language_code}".encode()
        index = int(hashlib.sha256(seed).hexdigest(), 16) % verses.count()
        verse = verses[index]

        return Response({
            "status": 200,
            "code": 1,
            "message": "Verse of the Day",
            "data": {
                "reference": f"{verse.book.bookName} {verse.no_of_chapter}:{verse.no_of_verses}",
                "date": today,
                "language": {
                    "code": language.languageCode,
                    "name": language.languages
                },
                "verses": verse.verses
            }
        })
