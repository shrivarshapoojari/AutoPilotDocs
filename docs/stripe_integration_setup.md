# Stripe Integration Setup

## Overview

This document provides a comprehensive guide to integrate Stripe into our payment system, as part of the migration process outlined in Jira ticket MIG-101. The integration will replace our legacy payment system with Stripe's robust payment processing capabilities.

## Pre-requirements

1. **Stripe Account**: Ensure you have a Stripe account. You can sign up at [Stripe](https://stripe.com/).
2. **Stripe API Keys**: Obtain your Secret Key and Publishable Key from the Stripe Dashboard.

## Setup Steps

### 1. Install Stripe API Library

First, install the Stripe Python library using pip:

```bash
pip install stripe
```

### 2. Update Payment Service

Update the `payment_service.py` file to integrate with the Stripe API. Here is a basic template of what the file might look like:

```python
import stripe

# Set your secret key: remember to change this to your live secret key in production
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

def create_payment(amount, currency, customer_email):
    try:
        # Create a new charge
        charge = stripe.Charge.create(
            amount=amount,  # amount in cents
            currency=currency,
            description='Payment for order',
            metadata={'order_id': '123', 'customer_email': customer_email},
        )
        return charge
    except stripe.error.StripeError as e:
        print('Error during charge creation: ', e)
        return None

# Example usage:
# charge = create_payment(500, 'usd', 'customer@example.com')
```

### 3. Remove Old Payment Flow Documentation

As part of this integration, remove the old payment flow documentation. This includes references to PayPal integration and any associated workflows. Git commits have been made to remove PayPal integration, ensuring a clean transition.

## Testing the Integration

### 1. Run a Test Payment

Use Stripe’s Test Cards to simulate successful and failed payments. For example, you can use the Visa card number `4242 4242 4242 4242` with any future expiration date and any valid CVC number.

### 2. Verify Charges in Stripe Dashboard

Log in to the Stripe Dashboard and verify that the test charges appear correctly. Check both successful and failed payments to ensure proper handling.

## Deploying Changes

When you are ready to go live, ensure that you update the `stripe.api_key` to use your live secret key. Deploy the changes and closely monitor the payment system for any issues.

## Additional Resources

- [Stripe API Documentation](https://stripe.com/docs/api)
- [Stripe Integration Examples](https://stripe.com/docs/examples)

By following these steps, we can successfully migrate our payment system to Stripe, providing a more seamless and reliable payment experience.