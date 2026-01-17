import re
from rest_framework import serializers
from .models import BibleBook, Verse
from languages.models import languageList

class LanguageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = languageList
        fields = ['id', 'languageCode', 'languages', 'is_active']

class BibleBookSerializer(serializers.ModelSerializer):
    bibleLanguage = LanguageListSerializer(read_only=True)
    bibleLanguage_id = serializers.PrimaryKeyRelatedField(
        queryset=languageList.objects.all(), source='bibleLanguage', write_only=True
    )

    class Meta:
        model = BibleBook
        fields = [
            'id',
            'bibleLanguage',
            'bibleLanguage_id',
            'testament',
            'booknumber',
            'bookName',
            'chapters',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class BibleVerseSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.bookName', read_only=True)
    book = BibleBookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=BibleBook.objects.all(), source='book', write_only=True
    )

    class Meta:
        model = Verse
        fields = [
            'id',
            'book',
            'book_id',
            'book_name',           # extra helpful field
            'no_of_chapter',
            'no_of_verses',
            'verses',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'book_name']
        
    def get_highlighted_verse(self, obj):
        query = self.context['request'].query_params.get('q', '')
        if not query:
            return obj.verses
        
        # Simple highlight (safe for JSON)
        highlighted = re.sub(
            re.escape(query),
            lambda m: f'<b>{m.group()}</b>',
            obj.verses,
            flags=re.IGNORECASE
        )
        return highlighted