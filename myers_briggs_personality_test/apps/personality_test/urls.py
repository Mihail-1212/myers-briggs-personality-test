from django.urls import path


from .views import PersonalityTestView


urlpatterns = [
    path('', PersonalityTestView.as_view(), name="index_page"),
]