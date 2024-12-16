"""
URL configuration for cmt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path , include
from cmt_app import views 
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register('guests' , views.viewset_guest)
router.register('movie' , views.viewset_movie)
router.register('reservation' , views.viewset_reservations)

urlpatterns = [
    path('admin/', admin.site.urls),
    #1
    path('django/jsonresponsenomodel/' , views.no_rest_no_model) ,
    #2
    path('django/jsonresponsefrommodel/' , views.no_rest_from_model),
    #3 GET POST from rest
   path('rest/fbvlist/' , views.fbv_list),
    #4 GET PUT DELETE from rest
   path('rest/fbvlist/<int:pk>' , views.fbv_pk),
    #5 GET POST from rest as CLASS
   path('rest/cbvlist/' , views.cbv_list.as_view()),
    #6 GET PUT DELETE from rest as CLASS
   path('rest/cbvlist/<int:pk>' , views.cbv_pk.as_view()),
    #7 GET POST from rest as CLASS MIXINS
   path('rest/mixins/' , views.mixins_list.as_view()),
    #8 GET PUT DELETE from rest as CLASS MIXINS
   path('rest/mixins/<int:pk>' , views.mixins_pk.as_view()),
    #9 GET POST from rest as CLASS GENERICS
   path('rest/generics/' , views.generics_list.as_view()),
    #10 GET PUT DELETE from rest as CLASS GENERICS
   path('rest/generics/<int:pk>' , views.generics_pk.as_view()),
    #11 GET POST PUT DELETE  from rest as CLASS VIEWSET
   path('rest/viewset/' , include(router.urls)),
    #12 GET find movie
    path('fbv/find_movie' , views.find_movie),
    #12 Post creat reservations
    path('fbv/newresr' , views.newr),
    #rest auth
    path('api-auth', include('rest_framework.urls')),
    # TOKEN
    path('api-token-auth' , obtain_auth_token)


]
