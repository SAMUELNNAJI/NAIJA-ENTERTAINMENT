from decimal import Decimal

from django.test import SimpleTestCase

from .models import Post, estimate_view_earnings


class ViewEarningsTests(SimpleTestCase):
    def test_one_hundred_views_earn_fifty_naira(self):
        self.assertEqual(estimate_view_earnings(100), Decimal("50.00"))
        self.assertEqual(Post(views=100).estimated_earnings, Decimal("50.00"))

    def test_partial_and_thousand_view_earnings(self):
        self.assertEqual(estimate_view_earnings(1), Decimal("0.50"))
        self.assertEqual(estimate_view_earnings(1000), Decimal("500.00"))
