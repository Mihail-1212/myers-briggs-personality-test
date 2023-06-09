"""myers_briggs_personality_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.templatetags.static import static
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('', include('personality_test.urls')),
    path('admin/', admin.site.urls),
]

# Add favicon to url path
favicon_view = RedirectView.as_view(url=static('icons/favicon.ico'), permanent=True)
urlpatterns.append(path('favicon.ico/', favicon_view))
