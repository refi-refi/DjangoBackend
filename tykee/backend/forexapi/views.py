import ast

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .dto_models import calculate_backtest_stats
from .models import Symbols, Strategies, Periods, Backtests
from .serializers import SymbolsSerializer, BacktestRawSerializer, PositionRawSerializer


class BacktestView(APIView):
    def post(self, request, format=None):
        request_body = request.data

        strategy = Strategies.objects.filter(name=request_body['strategy_name'])
        if not strategy:
            strategy_id = Strategies.objects.last()
            strategy_id = strategy_id.strategy_id + 1 if strategy_id else 1
            strategy = Strategies.objects.create(strategy_id=strategy_id, name=request_body['strategy_name'])
            strategy.save()
        else:
            strategy = strategy[0]

        backtest_raw = BacktestRawSerializer(request_body['backtest_info'])
        backtest_raw_data = ast.literal_eval(JSONRenderer().render(backtest_raw.data).decode('utf-8'))

        symbol = Symbols.objects.filter(name=backtest_raw.data['symbol_name'])[0]
        period = Periods.objects.filter(period_minutes=backtest_raw.data['period_minutes'])[0]

        position_data = PositionRawSerializer(request_body['positions'], many=True)

        backtest_stats = calculate_backtest_stats(position_data.data)

        backtest = Backtests(
            backtest_id=Backtests.objects.last().backtest_id + 1 if Backtests.objects.last() else 1,
            strategy=strategy,
            symbol=symbol,
            period=period,
            start_balance=backtest_raw_data['start_balance'],
            account_currency=backtest_raw_data['account_currency'],
            date_from=backtest_raw_data['date_from'],
            date_to=backtest_raw_data['date_to'],
            session_limits=backtest_raw_data['session_limits'],
            inputs=backtest_raw_data['inputs'],
            entry_list=backtest_raw_data['entry_list'],
            exit_list=backtest_raw_data['exit_list'],
            confirmation_list=backtest_raw_data['confirmation_list'],
            profit=backtest_stats['profit'],
            profit_factor=backtest_stats['profit_factor'],
            drawdown=backtest_stats['drawdown'],
            total_trades=backtest_stats['total_trades'],
            win_rate=backtest_stats['win_rate']
        )
        backtest.save()
        print(backtest)
        print(type(backtest))

        return Response(status=status.HTTP_201_CREATED)

        # return Response(status=status.HTTP_400_BAD_REQUEST)


class SymbolsView(APIView):
    def get(self, request, format=None):
        symbols = Symbols.objects.all()
        serializer = SymbolsSerializer(symbols, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SymbolsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
