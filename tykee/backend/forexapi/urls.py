from django.urls import path

from . import views

urlpatterns = [
    path("symbols/", views.SymbolsView.as_view(), name="symbols"),
    path("backtests/", views.BacktestView.as_view(), name="backtests"),
]
