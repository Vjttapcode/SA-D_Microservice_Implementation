from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Shipment
from .serializers import ShipmentSerializer
import uuid


class ShipmentCreate(APIView):
    def get(self, request):
        shipments = Shipment.objects.all()
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShipmentSerializer(data=request.data)
        if serializer.is_valid():
            shipment = serializer.save()
            # Auto-generate tracking number
            shipment.tracking_number = f"TRACK-{uuid.uuid4().hex[:8].upper()}"
            shipment.status = 'processing'
            shipment.save()
            return Response(ShipmentSerializer(shipment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShipmentDetail(APIView):
    def get(self, request, pk):
        try:
            shipment = Shipment.objects.get(pk=pk)
        except Shipment.DoesNotExist:
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            shipment = Shipment.objects.get(pk=pk)
        except Shipment.DoesNotExist:
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
        shipment.status = request.data.get("status", shipment.status)
        shipment.save()
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)
