from django.db import models


class StrategyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(strategy_type='S')
