from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product, Box, Order
from .serializers import ProductSerializer, BoxSerializer, OrderSerializer
from .services import BoxRecommendationService


# ========================
# PRODUCT CRUD VIEWS
# ========================
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# ========================
# BOX CRUD VIEWS
# ========================
class BoxListCreateView(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class BoxDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


# ==========================================
# ORDER CRUD + INSTANT BOX RECOMMENDATION
# ==========================================
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.prefetch_related('items__product', 'recommended_box').all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        recommended_box = BoxRecommendationService.recommend_box(order)
        order.recommended_box = recommended_box
        order.save(update_fields=['recommended_box'])


class OrderBoxRecommendationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.prefetch_related('items__product', 'recommended_box').all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'order_id'

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        recommended_box = BoxRecommendationService.recommend_box(order)
        order.recommended_box = recommended_box
        order.save(update_fields=['recommended_box'])

        data = self.get_serializer(order).data
        if not recommended_box:
            data["message"] = "No standard box fits this order. Custom packaging required."
        return Response(data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        updated_order = serializer.save()
        recommended_box = BoxRecommendationService.recommend_box(updated_order)
        updated_order.recommended_box = recommended_box
        updated_order.save(update_fields=['recommended_box'])