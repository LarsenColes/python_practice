import requests
from typing import Dict, Any, Tuple, Optional
from geopy.geocoders import Nominatim

class LocationResolver:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="nature_journal_app")
        
    def get_user_location(self) -> Dict[str, Any]:
        """
        Get the user's location using IP geolocation.
        This is a simple implementation - in a real app, you might 
        want to use browser geolocation API or a mobile device's GPS.
        """
        try:
            response = requests.get('https://ipapi.co/json/')
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data.get('city', ''),
                    'state': data.get('region_code', ''),  # Use region_code for state abbreviation
                    'state_name': data.get('region', ''),  # Full state name
                    'country': data.get('country_code', ''),
                    'latitude': data.get('latitude', 0),
                    'longitude': data.get('longitude', 0)
                }
        except Exception:
            pass
            
        # Return empty data if request fails
        return {
            'city': '',
            'state': '',
            'state_name': '',
            'country': '',
            'latitude': 0,
            'longitude': 0
        }
    
    def get_state_from_coordinates(self, latitude: float, longitude: float) -> str:
        """
        Convert coordinates to a US state.
        Returns the state code (e.g., NY, CA) if in the US, or 'Unknown' otherwise.
        """
        if not latitude or not longitude:
            return "Unknown"
            
        try:
            location = self.geolocator.reverse((latitude, longitude), language='en')
            address = location.raw.get('address', {})
            
            country_code = address.get('country_code', '').upper()
            
            # If in the US, return the state code
            if country_code == 'US':
                state_code = address.get('state_code')
                if state_code:
                    return state_code
                # Alternative: try to get the state name and return first 2 chars
                state = address.get('state')
                if state:
                    return state[:2].upper()
            
            return "Unknown"
        except Exception:
            return "Unknown" 