from django.urls import path, include
from rest_framework import routers
from api.views import *

routerA = routers.SimpleRouter()
routerA.register(r'author', AuthorListAndDetailAPI)

routerB = routers.SimpleRouter()
routerB.register(r'books', BookListAndDetailAPI)

urlpatterns = [
    path('api/v/', include(routerA.urls)),
    path('api/v/', include(routerB.urls)),
    path('api/v/add_book', AddBookAPI.as_view()),
]
