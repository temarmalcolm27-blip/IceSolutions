"""
Distance calculation service using Google Maps Distance Matrix API
"""
import googlemaps
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class DistanceService:
    def __init__(self):
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY not found in environment variables")
        
        self.gmaps = googlemaps.Client(key=api_key)
        self.origin_address = "Washington Gardens, Kingston 20, Jamaica"
        self.base_delivery_fee = 300.0  # JMD
        self.per_mile_rate = 200.0  # JMD per mile
    
    def calculate_distance(self, destination_address: str) -> Dict[str, float]:
        """
        Calculate driving distance from Washington Gardens to destination address.
        Returns distance in miles and calculated delivery fee.
        
        Args:
            destination_address: Customer delivery address
            
        Returns:
            Dict containing:
                - distance_miles: Distance in miles
                - delivery_fee: Calculated delivery fee in JMD
                - distance_text: Human-readable distance string
                - duration_text: Estimated travel duration
        """
        try:
            # Check if address is in Washington Gardens
            if "washington gardens" in destination_address.lower():
                return {
                    'distance_miles': 0,
                    'delivery_fee': 0.0,
                    'distance_text': 'Washington Gardens (Free Delivery)',
                    'duration_text': 'Local delivery',
                    'is_washington_gardens': True
                }
            
            # Make API request for distance matrix
            result = self.gmaps.distance_matrix(
                origins=self.origin_address,
                destinations=destination_address,
                mode="driving",
                units="metric"
            )
            
            # Check API response status
            if result['status'] != 'OK':
                logger.error(f"API returned status: {result['status']}")
                raise ValueError(f"Unable to calculate distance: {result['status']}")
            
            # Extract distance data from response
            element = result['rows'][0]['elements'][0]
            
            if element['status'] != 'OK':
                if element['status'] == 'ZERO_RESULTS':
                    raise ValueError("No route found to the specified address. Please check the address and try again.")
                raise ValueError(f"Unable to calculate route: {element['status']}")
            
            # Convert distance from meters to miles
            distance_meters = element['distance']['value']
            distance_miles = distance_meters / 1609.344
            
            # Calculate delivery fee ($300 base + $200 per mile)
            delivery_fee = self.base_delivery_fee + (distance_miles * self.per_mile_rate)
            
            return {
                'distance_miles': round(distance_miles, 2),
                'delivery_fee': round(delivery_fee, 2),
                'distance_text': element['distance']['text'],
                'duration_text': element['duration']['text'],
                'is_washington_gardens': False
            }
            
        except googlemaps.exceptions.ApiError as e:
            logger.error(f"Google Maps API error: {str(e)}")
            raise ValueError(f"Distance calculation failed: Unable to reach mapping service")
        except Exception as e:
            logger.error(f"Distance calculation error: {str(e)}")
            raise ValueError(str(e))
    
    def calculate_delivery_fee_for_order(self, destination_address: str, bags: int) -> Dict[str, float]:
        """
        Calculate delivery fee for an order, applying free delivery for 20+ bags.
        
        Args:
            destination_address: Customer delivery address
            bags: Number of bags in order
            
        Returns:
            Dict containing distance and fee information, with fee set to 0 for 20+ bags
        """
        result = self.calculate_distance(destination_address)
        
        # Free delivery for 20+ bags anywhere in Kingston
        if bags >= 20:
            result['delivery_fee'] = 0.0
            result['free_delivery_reason'] = '20+ bags qualify for free delivery'
        
        return result
