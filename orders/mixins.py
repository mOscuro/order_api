from rest_framework.exceptions import ValidationError

class validateCartItemMixin:
    """
    Factorize some logic for CartItem create and update serializers.
    """

    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError(
                f"Invalid value for quantity: {value}. Must be positive.")
        return value