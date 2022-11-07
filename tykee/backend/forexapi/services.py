import ast

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .dto_models import calculate_backtest_stats
from .models import Strategies, Symbols, Periods, Backtests
from .serializers import BacktestRawSerializer, PositionRawSerializer


class BacktestService:
    """BacktestService class

    This is a wrapper class for handling backtest requests.
    Solve purpose - place for business logic.

    Methods
    -------
    post(request)
        Handles POST requests. It creates a new backtest in the database.

    """

    def post(self, request):
        """
        Handles POST requests. It creates a new backtest in the database,
        and related objects (strategies, positions).

        Parameters
        ----------
        request
            Request object.

        Returns
        -------
        Response
            Response object with status code 201 if the backtest was created successfully.
        """
        request_body = request.data

        strategy = Strategies.objects.filter(name=request_body["strategy_name"])
        if not strategy:
            strategy = Strategies.objects.create(
                strategy_id=Strategies.new_strategy_id(), name=request_body["strategy_name"]
            )
            strategy.save()
        else:
            strategy = strategy[0]

        backtest_info = BacktestRawSerializer(request_body["backtest_info"])
        backtest_data = ast.literal_eval(JSONRenderer().render(backtest_info.data).decode("utf-8"))

        symbol = Symbols.objects.filter(name=backtest_data["symbol_name"])[0]
        period = Periods.objects.filter(period_minutes=backtest_data["period_minutes"])[0]

        if not symbol or not period:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for key in ("symbol_name", "period_minutes"):
            del backtest_data[key]

        position_data = PositionRawSerializer(request_body["positions"], many=True)
        backtest_stats = calculate_backtest_stats(position_data.data)

        backtest = Backtests(
            backtest_id=Backtests.new_backtest_id(),
            strategy=strategy,
            symbol=symbol,
            period=period,
            **backtest_data,
            **backtest_stats,
        )
        backtest.save()

        return Response(status=status.HTTP_201_CREATED)
