from .models import AuthorizedKey
from .models import Repository
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render


def index(request):
    user = request.user
    context = {
        'user': user,
        'repositories': user.repository_set.all(),
        'authorized_keys': user.authorizedkey_set.all()
    }
    return render(request, 'main/index.html', context)


class RepositoryCreate(CreateView):
    model = Repository
    fields = ['name']
    exclude = ['user']

    success_url = reverse_lazy('index')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class RepositoryDelete(DeleteView):
    model = Repository
    success_url = reverse_lazy('index')


class AuthorizedKeyCreate(CreateView):
    model = AuthorizedKey
    fields = ['name', 'authorized_key']
    exclude = ['user']

    success_url = reverse_lazy('index')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class AuthorizedKeyUpdate(UpdateView):
    model = AuthorizedKey
    fields = ['name', 'authorized_key']
    success_url = reverse_lazy('index')


class AuthorizedKeyDelete(DeleteView):
    model = AuthorizedKey
    success_url = reverse_lazy('index')
