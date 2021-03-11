from django.urls import path
from stackoverflow.views import SearchView

urlpatterns = [
    path('stackoverflow', SearchView.as_view(), name="search"),
]
