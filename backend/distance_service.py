"""
Distance calculation service using Google Routes API (new API replacing Distance Matrix)
"""
import requests
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class DistanceService:
    def __init__(self):
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY not found in environment variables")
        
        self.api_key = api_key
        self.origin_address = "Washington Gardens, Kingston 20, Jamaica"
        self.base_delivery_fee = 300.0  # JMD
        self.per_mile_rate = 35.0  # JMD per mile
    
    def calculate_distance(self, destination_address: str) -> Dict[str, float]:
        """
        Calculate driving distance from Washington Gardens to destination address using Routes API.
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
            
            # Use Google Routes API (new API)
            url = "https://routes.googleapis.com/directions/v2:computeRoutes"
            
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
                "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.legs"
            }
            
            body = {
                "origin": {
                    "address": self.origin_address
                },
                "destination": {
                    "address": destination_address
                },
                "travelMode": "DRIVE",
                "routingPreference": "TRAFFIC_UNAWARE"
            }
            
            response = requests.post(url, headers=headers, json=body)
            
            # Check response status
            if response.status_code != 200:
                logger.error(f"Routes API returned status {response.status_code}: {response.text}")
                raise ValueError(f"Unable to calculate distance. Please check the address and try again.")
            
            data = response.json()
            
            # Check if routes were found
            if not data.get('routes') or len(data['routes']) == 0:
                raise ValueError("No route found to the specified address. Please check the address and try again.")
            
            route = data['routes'][0]
            
            # Extract distance in meters
            distance_meters = route.get('distanceMeters', 0)
            if distance_meters == 0:
                raise ValueError("Unable to calculate distance for this address.")
            
            # Convert distance from meters to miles
            distance_miles = distance_meters / 1609.344
            
            # Extract duration
            duration_seconds = int(route.get('duration', '0s').replace('s', ''))
            duration_minutes = duration_seconds // 60
            duration_hours = duration_minutes // 60
            duration_remaining_minutes = duration_minutes % 60
            
            if duration_hours > 0:
                duration_text = f"{duration_hours} hour{'s' if duration_hours > 1 else ''} {duration_remaining_minutes} min{'s' if duration_remaining_minutes != 1 else ''}"
            else:
                duration_text = f"{duration_minutes} min{'s' if duration_minutes != 1 else ''}"
            
            # Format distance text
            distance_km = distance_meters / 1000
            distance_text = f"{distance_km:.1f} km"
            
            # Calculate delivery fee ($300 base + $200 per mile)
            delivery_fee = self.base_delivery_fee + (distance_miles * self.per_mile_rate)
            
            return {
                'distance_miles': round(distance_miles, 2),
                'delivery_fee': round(delivery_fee, 2),
                'distance_text': distance_text,
                'duration_text': duration_text,
                'is_washington_gardens': False
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Routes API request error: {str(e)}")
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
