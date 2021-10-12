import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from orders.models import Order, Product, CartItem


class Command(BaseCommand):

    def extract_node(self, node, skip_node=False):
        """
        Simple recusive method to convert an XML node and its children into a python dictionary.
        Keep in mind that this method only works for this specific test file.
        This would not work if there was multiple products in the cart for example.
        """

        return {
            child.tag: (
                child.text
                if len(child) == 0
                else self.extract_node(child)
            )
            for child in node
        }


    def handle(self, *args, **options):
        # Stream the XML file
        req = requests.get("http://test.lengow.io/orders-test.xml", stream=True)
        req.raw.decode_content = True  # ensure transfer encoding is honoured

        tree = ET.parse(req.raw)
        root = tree.getroot()

        # Convert data into a dictionary for convinience
        order_node = root.find("orders")
        order_list = [self.extract_node(node) for node in order_node]

        for order_data in order_list:
            # Read date and time of purchase if possible
            date_of_purchase = None
            if order_data['order_purchase_date'] and order_data['order_purchase_date']:
                date_time_str = f"{order_data['order_purchase_date']} {order_data['order_purchase_heure']}"
                date_of_purchase = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

            # Create Order in database
            new_order = Order.objects.create(
                identifier=order_data["order_id"],
                mrid=order_data["order_mrid"],
                refid=order_data["order_refid"],
                marketplace=order_data["marketplace"],
                purchased_at=date_of_purchase,
                amount=order_data["order_amount"],
                shipping_amount=order_data["order_shipping"],
                currency=order_data["order_currency"]
            )

            # Create Products to be used on Orders
            product_data = order_data["cart"]["products"]["product"]

            product, created = Product.objects.get_or_create(
                id_lengow=product_data["idLengow"],
                defaults={
                    "title": product_data["title"],
                    "price_unit": product_data["price_unit"],
                    "category": product_data["category"],
                }
            )

            CartItem.objects.create(
                order=new_order,
                product=product,
                quantity=product_data["quantity"]
            )

            
