"""
Sales Agent Script and FAQ for Ice Solutions
Contains the sales script and frequently asked questions for the AI sales agent.
"""

SALES_AGENT_SCRIPT = """
Hello! This is Marcus from Ice Solutions. We provide premium party ice delivery for businesses and events in Kingston, Jamaica.

Our 10-pound ice bags are crystal-clear, restaurant-quality ice delivered fresh to your door for just JMD $350 per bag.

We offer great bulk discounts:
- 5-9 bags: 5% discount
- 10-19 bags: 10% discount  
- 20+ bags: 15% discount

Delivery is FREE in Washington Gardens, and we charge JMD $300 base fee plus JMD $200 per mile for other areas. However, orders of 20+ bags get FREE delivery anywhere in Kingston!

Whether you're planning a party, running a bar, or need ice for an event, we can help with same-day delivery.

For orders or more information, please call us at (876) 490-7208 or visit our website.

Remember: More Ice = More Vibes!
"""

SALES_FAQ = [
    {
        "question": "What are your prices?",
        "answer": "Our 10lb ice bags are JMD $350 each. We offer bulk discounts: 5% off for 5-9 bags, 10% off for 10-19 bags, and 15% off for 20+ bags."
    },
    {
        "question": "Do you deliver?",
        "answer": "Yes! We offer same-day delivery. It's FREE in Washington Gardens. For other areas, we charge JMD $300 base fee plus JMD $200 per mile. Orders of 20+ bags get FREE delivery anywhere in Kingston."
    },
    {
        "question": "What areas do you serve?",
        "answer": "We serve Kingston and the corporate area. Washington Gardens gets free delivery, and we deliver to all other areas in Kingston with distance-based pricing."
    },
    {
        "question": "How fresh is your ice?",
        "answer": "Our ice is crystal-clear, restaurant-quality ice made fresh daily. We deliver the same day to ensure maximum freshness and quality."
    },
    {
        "question": "What sizes do you have?",
        "answer": "Currently we have 10lb party ice bags available. We're also launching 50lb commercial bags and 100lb industrial bags soon."
    },
    {
        "question": "How do I place an order?",
        "answer": "You can call us at (876) 490-7208 or visit our website to place an order online. We accept both phone orders and online orders."
    },
    {
        "question": "Do you have bulk discounts?",
        "answer": "Yes! We offer 5% off for 5-9 bags, 10% off for 10-19 bags, and 15% off for 20+ bags. Plus, 20+ bags get free delivery anywhere in Kingston."
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept cash on delivery and online payments through our website using credit/debit cards via Stripe."
    }
]

def calculate_ice_recommendation(guests, event_type="party", duration_hours=4):
    """Calculate ice recommendation based on guests and event type"""
    # Base calculation: 1 lb per guest per hour
    base_ice_lbs = guests * duration_hours
    
    # Event type multipliers
    multipliers = {
        "party": 1.2,
        "wedding": 1.5,
        "corporate": 1.0,
        "restaurant": 1.8,
        "bar": 2.0
    }
    
    multiplier = multipliers.get(event_type.lower(), 1.2)
    total_ice_lbs = base_ice_lbs * multiplier
    
    # Convert to 10lb bags (round up)
    bags_needed = max(1, int((total_ice_lbs + 9) // 10))
    
    return {
        "guests": guests,
        "event_type": event_type,
        "duration_hours": duration_hours,
        "total_ice_lbs": total_ice_lbs,
        "bags_needed": bags_needed,
        "recommendation": f"For {guests} guests at a {event_type} lasting {duration_hours} hours, I recommend {bags_needed} bags of ice ({total_ice_lbs:.1f} lbs total)."
    }

def calculate_price(bags, delivery_address=""):
    """Calculate total price including discounts and delivery"""
    base_price_per_bag = 350.0
    subtotal = bags * base_price_per_bag
    
    # Calculate bulk discount
    if bags >= 20:
        discount_percent = 15
    elif bags >= 10:
        discount_percent = 10
    elif bags >= 5:
        discount_percent = 5
    else:
        discount_percent = 0
    
    discount_amount = subtotal * (discount_percent / 100)
    discounted_total = subtotal - discount_amount
    
    # Calculate delivery fee
    is_washington_gardens = any(area in delivery_address.lower() for area in [
        'washington gardens', 'washington garden', 'wash gardens', 'wash garden'
    ])
    
    if is_washington_gardens or bags >= 20:
        delivery_fee = 0.0
        delivery_reason = "Washington Gardens" if is_washington_gardens else "20+ bags"
    else:
        delivery_fee = 300.0  # Base fee (distance calculation would be done by API)
        delivery_reason = "Standard delivery"
    
    total = discounted_total + delivery_fee
    
    return {
        "bags": bags,
        "base_price_per_bag": base_price_per_bag,
        "subtotal": subtotal,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "discounted_total": discounted_total,
        "delivery_fee": delivery_fee,
        "delivery_reason": delivery_reason,
        "total": total,
        "savings": discount_amount
    }