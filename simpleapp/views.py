# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import News
from datetime import datetime
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.mixins import PermissionRequiredMixin



class NewsList(ListView):
    model = News
    template_name = 'simpleapp/news.html'
    context_object_name = 'news'
    queryset = News.objects.order_by('-dateCreation')
    paginate_by = 2  # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_upgrade'] = "Обновление каждый четверг"
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    model = News
    template_name = 'simpleapp/news_detail.html'
    context_object_name = 'news_detail'

#def create_news(request):
    #form = NewsForm()
    #if request.method == 'POST':
        #form = NewsForm(request.POST)
        #if form.is_valid():
            #form.save()
            #return HttpResponseRedirect('/news/')
    #return render(request, 'simpleapp/news_add.html', {'form': form})

class NewsCreate(PermissionRequiredMixin, CreateView):
    template_name = 'simpleapp/news_add.html'
    form_class = NewsForm
    context_object_name = 'news_create'
    model = News
    permission_required = ('news.news_add', )

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'simpleapp/news_add.html'
    permission_required = ('news.news_update',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return News.objects.get(pk=id)

class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'simpleapp/news_delete.html'
    success_url = '/news/'
    queryset = News.objects.all()
    permission_required = ('news.news_delete',)

class NewsSearch(ListView):
    model = News
    template_name = 'simpleapp/news_search.html'
    context_object_name = 'search'
    queryset = News.objects.order_by('-dateCreation')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET,
                                          queryset=self.get_queryset())
        return context