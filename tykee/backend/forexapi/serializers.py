from rest_framework import serializers

from .models import Symbols, Strategies


class BacktestRawSerializer(serializers.Serializer):
    start_balance = serializers.FloatField()
    account_currency = serializers.CharField()
    symbol_name = serializers.CharField()
    period_minutes = serializers.IntegerField()
    date_from = serializers.IntegerField()
    date_to = serializers.IntegerField()
    session_limits = serializers.CharField()
    inputs = serializers.CharField()
    entry_list = serializers.CharField()
    exit_list = serializers.CharField()
    confirmation_list = serializers.CharField()


class PositionRawSerializer(serializers.Serializer):
    order_number = serializers.IntegerField()
    open_time = serializers.IntegerField()
    close_time = serializers.IntegerField()
    gross_profit = serializers.FloatField()
    net_profit = serializers.FloatField()
    balance = serializers.FloatField()
    lot_size = serializers.FloatField()
    open_price = serializers.FloatField()
    close_price = serializers.FloatField()
    sl_price = serializers.FloatField()
    tp_price = serializers.FloatField()
    commission = serializers.FloatField()
    swap = serializers.FloatField()
    close_type_value = serializers.IntegerField()
    position_type_value = serializers.IntegerField()
    breakeven_flag_value = serializers.IntegerField()


class StrategiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategies
        fields = ['strategy_id', 'name']


class SymbolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbols
        fields = ['name', 'base_currency', 'quote_currency', 'digits']
