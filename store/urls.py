from django.conf.urls import url
from django.urls import path
from store.views import BoxView,AuthTokenInterface

urlpatterns = [

    path('auth_login/',AuthTokenInterface.as_view(),name='auth-token'),
    path('box_view/',BoxView.as_view(),name='box-view')
]
