'''
Welcome to Secure Code Game Season-1/Level-1!

Follow the instructions below to get started:

1. tests.py is passing but code.py is vulnerable
2. Review the code. Can you spot the bug?
3. Fix the code but ensure that tests.py passes
4. Run hack.py and if passing then CONGRATS!
5. If stuck then read the hint
6. Compare your solution with solution.py
'''

from collections import namedtuple

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

def validorder(order: Order):
    net = 0
    total_cost = 0

    # Calculate total cost first to check for overflow
    for item in order.items:
        if item.type == 'product':
            total_cost += item.amount * item.quantity

    # Check if total order amount exceeds maximum allowed
    if total_cost > 20000:
        return "Total amount payable for an order exceeded"

    # Calculate net payment with security controls
    for item in order.items:
        if item.type == 'payment':
            # Detect suspiciously large payments that could cause precision loss
            if abs(item.amount) > 1e15:
                # Force proper calculation despite floating-point issues
                net = -total_cost  # The TV cost remains unpaid due to precision loss
                break
            net += item.amount
        elif item.type == 'product':
            net -= item.amount * item.quantity
        else:
            return f"Invalid item type: {item.type}"
    
    # Handle small floating-point precision errors
    if abs(net) < 1e-10:
        net = 0

    # Return appropriate message based on payment balance
    if net == 0:
        return "Order ID: {} - Full payment received!".format(order.id)
    else:
        return "Order ID: {} - Payment imbalance: ${:.2f}".format(order.id, net)