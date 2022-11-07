from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Symbols
from .serializers import SymbolsSerializer
from .services import BacktestService


class BacktestView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.backtest_service = BacktestService()

    def post(self, request, format=None):
        return self.backtest_service.post(request)


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
