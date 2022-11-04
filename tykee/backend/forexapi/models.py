# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


class Backtests(models.Model):
    id = models.BigAutoField(primary_key=True)
    backtest_id = models.BigIntegerField(unique=True)
    strategy = models.ForeignKey('Strategies', models.DO_NOTHING, to_field='strategy_id')
    symbol = models.ForeignKey('Symbols', models.DO_NOTHING, to_field='symbol_id')
    period = models.ForeignKey('Periods', models.DO_NOTHING, to_field='period_id')
    start_balance = models.FloatField()
    account_currency = models.TextField()
    date_from = models.BigIntegerField()
    date_to = models.BigIntegerField()
    session_limits = models.TextField()
    inputs = models.TextField()
    entry_list = models.TextField()
    exit_list = models.TextField()
    confirmation_list = models.TextField()
    profit = models.FloatField()
    profit_factor = models.FloatField()
    drawdown = models.FloatField()
    total_trades = models.IntegerField()
    win_rate = models.FloatField()

    class Meta:
        managed = False
        db_table = 'backtests'


class Bars(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.ForeignKey('Symbols', models.DO_NOTHING, to_field='symbol_id')
    period = models.ForeignKey('Periods', models.DO_NOTHING, to_field='period_id')
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()
    open = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    close = models.IntegerField()
    spread = models.IntegerField()
    volume = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bars'
        unique_together = (('symbol', 'start_dt', 'end_dt'),)


class BreakevenFlags(models.Model):
    id = models.BigAutoField(primary_key=True)
    breakeven_flag_value = models.BigIntegerField(unique=True)
    name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'breakeven_flags'


class CloseTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    close_type_value = models.BigIntegerField(unique=True)
    name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'close_types'


class Periods(models.Model):
    id = models.BigAutoField(primary_key=True)
    period_id = models.BigIntegerField(unique=True)
    name = models.TextField(unique=True)
    period_minutes = models.BigIntegerField()
    trunc_period = models.TextField()
    part_period = models.TextField(blank=True, null=True)
    part_value = models.IntegerField(blank=True, null=True)
    period_interval = models.TextField()

    class Meta:
        managed = False
        db_table = 'periods'


class PositionTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    position_type_value = models.BigIntegerField(unique=True)
    name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'position_types'


class Positions(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_number = models.IntegerField()
    open_time = models.BigIntegerField()
    close_time = models.BigIntegerField()
    lot_size = models.FloatField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    sl_price = models.FloatField()
    tp_price = models.FloatField()
    gross_profit = models.FloatField()
    net_profit = models.FloatField()
    commission = models.FloatField()
    swap = models.FloatField()
    balance = models.FloatField()
    backtest = models.ForeignKey(Backtests, models.DO_NOTHING, to_field='backtest_id')
    position_type = models.ForeignKey(PositionTypes, models.DO_NOTHING)
    breakeven_flag = models.ForeignKey(BreakevenFlags, models.DO_NOTHING)
    close_type = models.ForeignKey(CloseTypes, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'positions'


class Strategies(models.Model):
    id = models.BigAutoField(primary_key=True)
    strategy_id = models.BigIntegerField(unique=True)
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'strategies'

    def find_by_name(self, name):
        return self.objects.get(name=name)

    # def get_or_create(self, name):
    #     return self.objects.get_or_create(name=name)


#     def get_or_create(self, name):
#         strategy, created = Strategies.objects.get_or_create(name=name)
#         return strategy
#
# print(Strategies.objects.get_or_create(name='test'))


class Symbols(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol_id = models.BigIntegerField(unique=True)
    name = models.TextField(unique=True)
    base_currency = models.TextField()
    quote_currency = models.TextField()
    digits = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'symbols'


class Ticks(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.ForeignKey(Symbols, models.DO_NOTHING, to_field='symbol_id')
    ts_utc = models.BigIntegerField()
    bid = models.BigIntegerField()
    ask = models.BigIntegerField()
    flags = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ticks'
