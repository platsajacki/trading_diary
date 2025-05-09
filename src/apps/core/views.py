from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Главная страница сайта."""

    template_name = 'home.html'
