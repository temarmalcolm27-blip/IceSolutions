# Sales Agent Script and FAQ for Ice Solutions
# Agent sells 10lb bags of ice to leads

SALES_AGENT_SCRIPT = """
You are a friendly and professional sales representative for Ice Solutions, Jamaica's premier ice delivery service.

YOUR MISSION: Sell 10lb bags of premium restaurant-quality ice to potential customers.

PRICING:
- Regular Price: JMD $350 per 10lb bag
- Bulk Discounts:
  * 5-9 bags: 5% off (JMD $332.50 per bag)
  * 10-19 bags: 10% off (JMD $315.00 per bag)
  * 20+ bags: 15% off (JMD $297.50 per bag)
- Delivery: FREE in Washington Gardens, JMD $300 elsewhere
- Same-day delivery available (order at least 2 hours before needed)

YOUR APPROACH:
1. Greet the customer warmly using their name if available
2. Introduce yourself and Ice Solutions
3. Ask about their ice needs (events, restaurant, bar, party, etc.)
4. Listen to their requirements
5. Suggest appropriate quantities based on their needs
6. Highlight bulk discounts if applicable
7. Confirm delivery details
8. Close the sale and provide order confirmation

CONVERSATION STYLE:
- Friendly Jamaican tone
- Professional and helpful
- Build rapport naturally
- Use the tagline: "More Ice = More Vibes"
- Be enthusiastic about the product quality
"""

SALES_FAQ = {
    "product_quality": {
        "question": "What's the quality of your ice?",
        "answer": "Our ice is crystal-clear, restaurant-quality ice made from purified water. It's the same premium ice used by top restaurants and bars across Jamaica. We guarantee freshness and quality with every delivery."
    },
    "delivery_time": {
        "question": "How fast can you deliver?",
        "answer": "We offer same-day delivery! Just order at least 2 hours before you need your ice. For Washington Gardens, delivery is completely FREE. For other areas, there's a small JMD $300 delivery fee."
    },
    "minimum_order": {
        "question": "Is there a minimum order?",
        "answer": "No minimum order required! Whether you need 1 bag or 100 bags, we'll deliver. However, ordering 5 or more bags gets you our bulk discount starting at 5% off."
    },
    "bulk_pricing": {
        "question": "Do you offer bulk discounts?",
        "answer": "Absolutely! We have great bulk pricing: 5-9 bags get 5% off, 10-19 bags get 10% off, and 20 or more bags get 15% off. The more you order, the more you save!"
    },
    "payment_methods": {
        "question": "How do I pay?",
        "answer": "We accept secure online payment through our website using credit or debit cards. You can place your order at icesolutions.com, or I can help you order right now over the phone, and we'll send you a payment link."
    },
    "delivery_areas": {
        "question": "Where do you deliver?",
        "answer": "We deliver throughout Kingston and surrounding areas. Washington Gardens gets FREE delivery, and all other areas have a small JMD $300 delivery fee. We cover most of the Kingston metropolitan area."
    },
    "ice_amount_events": {
        "question": "How much ice do I need for my event?",
        "answer": "Great question! As a general rule, plan for about 1-2 pounds of ice per guest for a 4-hour event. So for 50 guests, you'd need about 10 bags (100 lbs). For bars or longer events, I'd recommend more. I can help calculate the exact amount for your specific event."
    },
    "storage": {
        "question": "How should I store the ice?",
        "answer": "Keep the bags in a freezer until needed. Our bags are designed to stack easily and stay fresh. If you're using it for an event, we recommend transferring to coolers with some insulation about 1-2 hours before the event."
    },
    "recurring_orders": {
        "question": "Can I set up recurring deliveries?",
        "answer": "Yes! We offer recurring delivery services for restaurants, bars, and businesses. You'll get priority scheduling and can discuss custom pricing for regular large orders. Just let me know your needs, and I'll set that up for you."
    },
    "cancellation": {
        "question": "Can I cancel or change my order?",
        "answer": "You can cancel or modify your order up to 1 hour before the scheduled delivery time. Just give us a call at (876) 490-7208, and we'll take care of it."
    },
    "quality_guarantee": {
        "question": "What if I'm not satisfied?",
        "answer": "We have a 100% satisfaction guarantee! If there's any issue with your ice quality or delivery, let us know immediately and we'll make it right. We stand behind our product and service."
    },
    "business_accounts": {
        "question": "Do you offer business accounts?",
        "answer": "Yes! For restaurants, bars, and businesses that need regular ice deliveries, we offer business accounts with flexible payment terms, priority scheduling, and a dedicated account manager for orders of 20+ bags. It's perfect for businesses that need consistent, reliable ice supply."
    },
    "ice_types": {
        "question": "What type of ice do you sell?",
        "answer": "We specialize in premium cube ice, which is perfect for drinks, coolers, and keeping things cold. Each bag contains 10 pounds of crystal-clear ice cubes. This is the same quality ice you'd find in high-end restaurants."
    },
    "emergency_orders": {
        "question": "Can you handle emergency orders?",
        "answer": "Absolutely! We understand events and businesses sometimes need ice quickly. As long as you order at least 2 hours before you need it, we'll get it to you the same day. For urgent needs, call us directly at (876) 490-7208, and we'll do our best to accommodate you."
    }
}

# Ice calculation helper for the agent
def calculate_ice_recommendation(guests=None, event_type=None, duration_hours=4):
    """
    Calculate recommended ice bags based on event details
    """
    if not guests:
        return None
    
    # Base calculation: 1.5 lbs per guest per 4 hours
    base_lbs_per_guest = 1.5
    
    # Adjust for event type
    multipliers = {
        'party': 1.2,
        'wedding': 1.5,
        'restaurant': 1.8,
        'bar': 2.0,
        'corporate': 1.0,
        'other': 1.2
    }
    
    multiplier = multipliers.get(event_type, 1.2)
    
    # Adjust for duration
    duration_factor = duration_hours / 4.0
    
    total_lbs = guests * base_lbs_per_guest * multiplier * duration_factor
    bags_needed = max(1, round(total_lbs / 10))
    
    return {
        'guests': guests,
        'bags_recommended': bags_needed,
        'total_lbs': round(total_lbs, 1),
        'event_type': event_type,
        'duration_hours': duration_hours
    }

# Pricing calculator for the agent
def calculate_price(bags, delivery_area='other'):
    """
    Calculate total price with discounts
    """
    price_per_bag = 350.00
    subtotal = bags * price_per_bag
    
    # Apply bulk discount
    discount_percent = 0
    if bags >= 20:
        discount_percent = 15
    elif bags >= 10:
        discount_percent = 10
    elif bags >= 5:
        discount_percent = 5
    
    discount_amount = subtotal * (discount_percent / 100)
    total_after_discount = subtotal - discount_amount
    
    # Add delivery fee
    delivery_fee = 0 if delivery_area.lower() == 'washington gardens' else 300.00
    final_total = total_after_discount + delivery_fee
    
    return {
        'bags': bags,
        'price_per_bag': price_per_bag,
        'subtotal': subtotal,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'total_after_discount': total_after_discount,
        'delivery_fee': delivery_fee,
        'final_total': final_total
    }
