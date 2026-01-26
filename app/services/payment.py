"""
Payment service
"""

from decimal import Decimal
from typing import Optional


class PaymentService:
    """Payment processing service"""

    @staticmethod
    def process_payment(amount: Decimal, payment_method: str) -> dict:
        """
        Process a payment

        Args:
            amount: Payment amount
            payment_method: Payment method (e.g., 'credit_card', 'paypal')

        Returns:
            dict: Payment result with status and transaction_id
        """
        # TODO: Implement payment processing logic
        # This would integrate with payment gateways like Stripe, PayPal, etc.
        return {
            "status": "success",
            "transaction_id": "mock_transaction_id",
            "amount": float(amount),
            "payment_method": payment_method,
        }

    @staticmethod
    def refund_payment(transaction_id: str, amount: Optional[Decimal] = None) -> dict:
        """
        Process a refund

        Args:
            transaction_id: Original transaction ID
            amount: Refund amount (if None, full refund)

        Returns:
            dict: Refund result with status
        """
        # TODO: Implement refund processing logic
        return {
            "status": "success",
            "refund_id": "mock_refund_id",
            "transaction_id": transaction_id,
            "amount": float(amount) if amount else None,
        }

    @staticmethod
    def validate_payment_method(payment_method: str) -> bool:
        """
        Validate if a payment method is supported

        Args:
            payment_method: Payment method to validate

        Returns:
            bool: True if payment method is valid
        """
        valid_methods = ["credit_card", "debit_card", "paypal", "bank_transfer"]
        return payment_method.lower() in valid_methods
