from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
from packing.models import Box, Order, OrderItem, Product
from packing.services import BoxRecommendationService


class BoxRecommendationServiceTestCase(TestCase):
    def setUp(self):
        # Create standard boxes
        self.small_box = Box.objects.create(
            name="Small Box",
            inner_length=15.0,
            inner_width=10.0,
            inner_height=10.0,
            max_weight=2.0,
            cost=20.0,
            is_active=True,
        )
        self.medium_box = Box.objects.create(
            name="Medium Shoe Box",
            inner_length=35.0,
            inner_width=25.0,
            inner_height=15.0,
            max_weight=5.0,
            cost=45.0,
            is_active=True,
        )

        # Create sample products
        self.small_item = Product.objects.create(
            name="Phone Case",
            sku="PHONE-CASE-01",
            length=10.0,
            width=5.0,
            height=2.0,
            weight=0.2,
        )
        self.shoes = Product.objects.create(
            name="Running Shoes",
            sku="SHOE-RUN-01",
            length=30.0,
            width=20.0,
            height=12.0,
            weight=1.2,
        )
        self.oversized_item = Product.objects.create(
            name="Large Monitor",
            sku="MON-01",
            length=80.0,
            width=50.0,
            height=20.0,
            weight=10.0,
        )

    def test_recommend_box_success(self):
        """Test that shoes successfully recommend the medium box."""
        order = Order.objects.create(order_number="ORD-001")
        OrderItem.objects.create(order=order, product=self.shoes, quantity=1)

        recommended_box = BoxRecommendationService.recommend_box(order)
        self.assertEqual(recommended_box, self.medium_box)

    def test_recommend_box_prefers_cheaper_or_smaller_fit(self):
        """Test that smaller items fit into the smallest available box."""
        order = Order.objects.create(order_number="ORD-002")
        OrderItem.objects.create(order=order, product=self.small_item, quantity=1)

        recommended_box = BoxRecommendationService.recommend_box(order)
        self.assertEqual(recommended_box, self.small_box)

    def test_recommend_box_exceeds_weight(self):
        """Test that an order exceeding max weight returns None."""
        order = Order.objects.create(order_number="ORD-003")
        # Add multiple small items to exceed small box weight (2.0kg) but keep volume small
        OrderItem.objects.create(order=order, product=self.small_item, quantity=15)

        # Should fail small box due to weight (15 * 0.2 = 3.0kg > 2.0kg),
        # but fit in medium box (3.0kg <= 5.0kg and fits volume/3D)
        recommended_box = BoxRecommendationService.recommend_box(order)
        self.assertEqual(recommended_box, self.medium_box)

    def test_recommend_box_no_fit_required(self):
        """Test that items exceeding all available box dimensions return None."""
        order = Order.objects.create(order_number="ORD-004")
        OrderItem.objects.create(order=order, product=self.oversized_item, quantity=1)

        recommended_box = BoxRecommendationService.recommend_box(order)
        self.assertIsNone(recommended_box)


class OrderRecommendationAPITestCase(APITestCase):
    def setUp(self):
        self.box = Box.objects.create(
            name="Medium Box",
            inner_length=35.0,
            inner_width=25.0,
            inner_height=15.0,
            max_weight=5.0,
            cost=45.0,
            is_active=True,
        )
        self.product = Product.objects.create(
            name="T-Shirt",
            sku="TSHIRT-01",
            length=25.0,
            width=15.0,
            height=5.0,
            weight=0.4,
        )
        self.orders_url = "/orders/"  # Adjust if your URL name differs

    def test_create_order_triggers_recommendation(self):
        """Test that posting a new order instantly calculates and assigns recommended_box."""
        payload = {
            "order_number": "ORD-API-01",
            "is_packed": False,
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 1
                }
            ]
        }
        response = self.client.post(self.orders_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["recommended_box"], self.box.id)
        self.assertIsNotNone(response.data["recommended_box_details"])

    def test_retrieve_order_triggers_recommendation(self):
        """Test that retrieving an order detail endpoint evaluates and returns the box recommendation."""
        order = Order.objects.create(order_number="ORD-API-02")
        OrderItem.objects.create(order=order, product=self.product, quantity=1)

        detail_url = f"/orders/{order.id}/"
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["recommended_box"], self.box.id)