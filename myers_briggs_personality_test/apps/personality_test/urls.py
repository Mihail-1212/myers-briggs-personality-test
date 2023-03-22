from django.urls import path


from . import views


urlpatterns = [
    path('', views.index_page, name="index_page"),
    path('test/', views.PersonalityTestView.as_view(), name="test_page"),
    path('descriptor/', views.DescriptorListView.as_view(), name="descriptor_list"),
    path('descriptor/<int:descriptor_id>/', views.DescriptorDetailView.as_view(), name="descriptor_detail"),
]