from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from pure_pagination.mixins import PaginationMixin

from apps.airport.models import Airport
from apps.review.models import Review


class Index(PaginationMixin, ListView):
    template_name = 'airport/index.html'
    context_object_name = 'airports'
    paginate_by = 6

    def get_queryset(self):
        country = self.request.GET.get('country')

        if country:
            object_list = Airport.objects \
                .filter(Q(country__icontains=country.strip().lower())) \
                .order_by('-created_at')
        else:
            object_list = Airport.objects \
                .filter(created_at__lte=timezone.now()) \
                .order_by('-created_at')
        return object_list


class Search(PaginationMixin, ListView):
    template_name = 'airport/index.html'
    context_object_name = 'airports'
    paginate_by = 6

    def get_context_data(self):
        context = super().get_context_data()
        context['is_search'] = True
        return context

    def get_queryset(self):
        q_word = self.request.GET.get('q')

        if q_word:
            object_list = Airport.objects \
                .filter(Q(title__icontains=q_word.strip()) | Q(body__icontains=q_word.strip())) \
                .order_by('-created_at')
        else:
            object_list = []
        return object_list


def show(request, pk):
    airport = Airport.objects.get(id=pk)
    reviews = Review.objects \
        .filter(airport=airport.id) \
        .order_by('-created_at') \
        .all()

    return render(request, 'airport/show.html', {'airport': airport, 'reviews': reviews})


def top(request):
    return render(request, 'index.html')


def notfound(request):
    return render(request, '404.html')
