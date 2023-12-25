from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Book, Author
from api.serializers import BookSerializer, AuthorSerializer, AddBookSerializer


class AddBookAPI(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        serializer = AddBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data['title']
        category = serializer.validated_data['category']
        publisher = serializer.validated_data['publisher']
        year_of_release = serializer.validated_data['yearOfRel']

        existing_books = Book.objects.filter(title=title)

        for book in existing_books:
            if (category == 0 and book.publisher != publisher) or (category == 1 and book.yearOfRel != year_of_release):
                raise ValidationError(f'Есть книга с названием "{title}" и другими характеристиками.')

        serializer.save()
        return Response({"запись успешно добавлена"})


class BookListAndDetailAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'genre']


class AuthorListAndDetailAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
