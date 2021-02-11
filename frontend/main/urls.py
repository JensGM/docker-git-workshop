from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path('repositories/create', login_required(views.RepositoryCreate.as_view())),
    path('repositories/<int:pk>/delete', login_required(views.RepositoryDelete.as_view())),
    path('authorized_keys/create/', login_required(views.AuthorizedKeyCreate.as_view())),
    path('authorized_keys/<int:pk>/update/', login_required(views.AuthorizedKeyUpdate.as_view())),
    path('authorized_keys/<int:pk>/delete/', login_required(views.AuthorizedKeyDelete.as_view())),
    path('', login_required(views.index), name='index'),
]
