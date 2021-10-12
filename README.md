# Order API for Lengow technical test

## Installation

The use of a virtual environment is advised.
&nbsp;

The requirements file was generated using pipenv.
&nbsp;

&nbsp;

First, install requirements:
- From within a virtual environment using pip
```
pip install requirements.txt
```
- Using pipenv if installed
```
pipenv install
pipenv shell
```
&nbsp;

Then, create the sqlite database using the migrate command:
```
python manage.py migrate --settings=order_api.settings
```
&nbsp;

Parse XML test file and create Orders, Carts and Products using the custom Django command `read_orders`
```
python manage.py read_orders --settings=order_api.settings
```
&nbsp;

Finally, run django webserver to be able to access apis.
```
python manage.py runserver 0.0.0.0:8443  --settings=order_api.settings
```
&nbsp;

## Usage

**Note that a basic UI for documentation and tests is available at `/docs/`.**
<br/><br/>
List all existing orders with `GET /orders/`<br/>
List can be filtered using query parameters **marketplace**, **currency** or **category**<br/>
Retrieve a specific order and show its items using `GET /orders/{order_pk}/`<br/>
Create a basic order with `POST /orders/` and a body composed of **markeplace** and **currency**
<br/><br/>
List all availaible products with `GET /products/`
<br/><br/>
Access the detail of an order's cart with `GET /orders/{order_pk}/cart-items/`<br/>
Add a new item to the cart of an order with `POST /orders/{order_pk}/cart-items/` and a body composed of **product** and **quantity**<br/>
Update a cart item quantity with `PATCH /orders/{order_pk}/cart-items/{item_pk}/`<br/>
Remove an item from the cart of an order using `DELETE /orders/{order_pk}/cart-items/{item_pk}/`<br/>
