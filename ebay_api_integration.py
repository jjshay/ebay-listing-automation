#!/usr/bin/env python3
"""
eBay API Integration for Gauntlet Gallery
Handles authentication, listing creation, and inventory management
"""

import os
import json
import base64
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class eBayAPIIntegration:
    """eBay API integration for automated art listings"""

    def __init__(self):
        """Initialize eBay API with credentials from environment"""

        # Load credentials from environment variables
        self.credentials = {
            'app_id': os.getenv('EBAY_APP_ID', ''),
            'cert_id': os.getenv('EBAY_CERT_ID', ''),
            'dev_id': os.getenv('EBAY_DEV_ID', ''),
            'redirect_uri': os.getenv('EBAY_REDIRECT_URI', ''),
            'environment': os.getenv('EBAY_ENVIRONMENT', 'sandbox')
        }
        
        # API endpoints
        self.sandbox_endpoints = {
            'oauth': 'https://api.sandbox.ebay.com/identity/v1/oauth2/token',
            'sell_inventory': 'https://api.sandbox.ebay.com/sell/inventory/v1',
            'sell_account': 'https://api.sandbox.ebay.com/sell/account/v1',
            'sell_marketing': 'https://api.sandbox.ebay.com/sell/marketing/v1',
            'browse': 'https://api.sandbox.ebay.com/buy/browse/v1'
        }
        
        self.production_endpoints = {
            'oauth': 'https://api.ebay.com/identity/v1/oauth2/token',
            'sell_inventory': 'https://api.ebay.com/sell/inventory/v1',
            'sell_account': 'https://api.ebay.com/sell/account/v1',
            'sell_marketing': 'https://api.ebay.com/sell/marketing/v1',
            'browse': 'https://api.ebay.com/buy/browse/v1'
        }
        
        self.endpoints = self.sandbox_endpoints if self.credentials['environment'] == 'sandbox' else self.production_endpoints
        
        # Authentication
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        
        print(f"🛒 eBay API Integration initialized for {self.credentials['environment']} environment")
    
    def get_auth_url(self) -> str:
        """Generate eBay OAuth authorization URL"""
        base_url = "https://auth.sandbox.ebay.com/oauth2/authorize" if self.credentials['environment'] == 'sandbox' else "https://auth.ebay.com/oauth2/authorize"
        
        scopes = [
            'https://api.ebay.com/oauth/api_scope',
            'https://api.ebay.com/oauth/api_scope/sell.inventory',
            'https://api.ebay.com/oauth/api_scope/sell.marketing',
            'https://api.ebay.com/oauth/api_scope/sell.account'
        ]
        
        auth_url = (
            f"{base_url}?"
            f"client_id={self.credentials['app_id']}&"
            f"redirect_uri={self.credentials['redirect_uri']}&"
            f"response_type=code&"
            f"scope={' '.join(scopes)}"
        )
        
        return auth_url
    
    def exchange_code_for_token(self, auth_code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        try:
            # Create authorization header
            credentials = f"{self.credentials['app_id']}:{self.credentials['cert_id']}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': self.credentials['redirect_uri']
            }
            
            response = requests.post(self.endpoints['oauth'], headers=headers, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                
                self.access_token = token_data['access_token']
                self.refresh_token = token_data.get('refresh_token')
                expires_in = token_data.get('expires_in', 7200)  # Default 2 hours
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                # Save tokens
                self._save_tokens()
                
                print("✅ eBay OAuth tokens obtained successfully")
                return token_data
            else:
                print(f"❌ eBay OAuth failed: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            print(f"❌ eBay OAuth error: {str(e)}")
            return {}
    
    def refresh_access_token(self) -> bool:
        """Refresh the access token using refresh token"""
        if not self.refresh_token:
            return False
            
        try:
            credentials = f"{self.credentials['app_id']}:{self.credentials['cert_id']}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token
            }
            
            response = requests.post(self.endpoints['oauth'], headers=headers, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                expires_in = token_data.get('expires_in', 7200)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                self._save_tokens()
                print("✅ eBay access token refreshed")
                return True
            else:
                print(f"❌ eBay token refresh failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ eBay token refresh error: {str(e)}")
            return False
    
    def _save_tokens(self):
        """Save tokens to file"""
        token_data = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.token_expires_at.isoformat() if self.token_expires_at else None,
            'environment': self.credentials['environment']
        }
        
        with open('.ebay_tokens.json', 'w') as f:
            json.dump(token_data, f, indent=2)
    
    def _load_tokens(self):
        """Load saved tokens"""
        try:
            if os.path.exists('.ebay_tokens.json'):
                with open('.ebay_tokens.json', 'r') as f:
                    token_data = json.load(f)
                
                self.access_token = token_data.get('access_token')
                self.refresh_token = token_data.get('refresh_token')
                
                if token_data.get('expires_at'):
                    self.token_expires_at = datetime.fromisoformat(token_data['expires_at'])
                
                return True
        except Exception as e:
            print(f"⚠️ Could not load eBay tokens: {str(e)}")
        
        return False
    
    def ensure_valid_token(self) -> bool:
        """Ensure we have a valid access token"""
        # Load existing tokens
        if not self.access_token:
            self._load_tokens()
        
        # Check if token is expired
        if self.token_expires_at and datetime.now() >= self.token_expires_at:
            if self.refresh_token:
                return self.refresh_access_token()
            else:
                return False
        
        return bool(self.access_token)
    
    def create_inventory_item(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create inventory item on eBay"""
        if not self.ensure_valid_token():
            return {'success': False, 'error': 'No valid eBay token'}
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'
            }
            
            # Convert product data to eBay format
            ebay_item = self._convert_to_ebay_format(product_data)
            
            # Create inventory item
            sku = product_data.get('sku', f"ART-{int(time.time())}")
            url = f"{self.endpoints['sell_inventory']}/inventory_item/{sku}"
            
            response = requests.put(url, headers=headers, json=ebay_item)
            
            if response.status_code in [200, 201, 204]:
                print(f"✅ eBay inventory item created: {sku}")
                return {'success': True, 'sku': sku, 'item_data': ebay_item}
            else:
                error_msg = self._parse_ebay_error(response)
                print(f"❌ eBay inventory creation failed: {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            print(f"❌ eBay inventory creation error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_offer(self, sku: str, price: float, quantity: int = 1) -> Dict[str, Any]:
        """Create offer for inventory item"""
        if not self.ensure_valid_token():
            return {'success': False, 'error': 'No valid eBay token'}
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'
            }
            
            offer_data = {
                'sku': sku,
                'marketplaceId': 'EBAY_US',
                'format': 'FIXED_PRICE',
                'availableQuantity': quantity,
                'categoryId': '550',  # Art category
                'listingDescription': f'Beautiful artwork - see inventory item {sku} for details',
                'listingPolicies': {
                    'fulfillmentPolicyId': None,  # Will need to be set
                    'paymentPolicyId': None,      # Will need to be set
                    'returnPolicyId': None        # Will need to be set
                },
                'pricingSummary': {
                    'price': {
                        'value': str(price),
                        'currency': 'USD'
                    }
                }
            }
            
            url = f"{self.endpoints['sell_inventory']}/offer"
            response = requests.post(url, headers=headers, json=offer_data)
            
            if response.status_code in [200, 201]:
                offer_response = response.json()
                offer_id = offer_response.get('offerId')
                print(f"✅ eBay offer created: {offer_id}")
                return {'success': True, 'offer_id': offer_id, 'sku': sku}
            else:
                error_msg = self._parse_ebay_error(response)
                print(f"❌ eBay offer creation failed: {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            print(f"❌ eBay offer creation error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def publish_offer(self, offer_id: str) -> Dict[str, Any]:
        """Publish offer to create active listing"""
        if not self.ensure_valid_token():
            return {'success': False, 'error': 'No valid eBay token'}
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'
            }
            
            url = f"{self.endpoints['sell_inventory']}/offer/{offer_id}/publish"
            response = requests.post(url, headers=headers)
            
            if response.status_code in [200, 204]:
                publish_response = response.json() if response.text else {}
                listing_id = publish_response.get('listingId')
                print(f"✅ eBay listing published: {listing_id}")
                return {'success': True, 'listing_id': listing_id, 'offer_id': offer_id}
            else:
                error_msg = self._parse_ebay_error(response)
                print(f"❌ eBay publishing failed: {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            print(f"❌ eBay publishing error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _convert_to_ebay_format(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert product data to eBay inventory item format"""
        
        # Extract data with fallbacks
        title = product_data.get('title', 'Artwork')
        artist = product_data.get('artist', 'Unknown Artist')
        medium = product_data.get('medium', 'Mixed Media')
        size = product_data.get('size', 'Various')
        condition = product_data.get('condition', 'Good')
        year = product_data.get('year', '2024')
        
        # Create eBay-compatible title (80 char limit)
        ebay_title = f"{artist} - {title}"[:77] + "..." if len(f"{artist} - {title}") > 80 else f"{artist} - {title}"
        
        # Create detailed description
        description = f"""
<div style="font-family: Arial, sans-serif; max-width: 800px;">
    <h2>{artist} - {title}</h2>
    
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
        <h3>🎨 Artwork Details</h3>
        <ul>
            <li><strong>Artist:</strong> {artist}</li>
            <li><strong>Title:</strong> {title}</li>
            <li><strong>Medium:</strong> {medium}</li>
            <li><strong>Size:</strong> {size}</li>
            <li><strong>Year:</strong> {year}</li>
            <li><strong>Condition:</strong> {condition}</li>
        </ul>
    </div>
    
    <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 15px 0;">
        <h3>🏆 About Gauntlet Gallery</h3>
        <p>Professional art dealers specializing in contemporary and modern artwork. 
        All pieces are carefully curated and authenticated. We provide detailed 
        condition reports and provenance information.</p>
        
        <p><strong>Why Choose Gauntlet Gallery?</strong></p>
        <ul>
            <li>✅ Professional authentication</li>
            <li>✅ Detailed condition reports</li>
            <li>✅ Secure packaging & shipping</li>
            <li>✅ 30-day return policy</li>
            <li>✅ Certificate of authenticity available</li>
        </ul>
    </div>
    
    <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 15px 0;">
        <h3>📦 Shipping & Handling</h3>
        <p>This artwork will be carefully packaged with museum-quality materials 
        to ensure it arrives in perfect condition. We ship worldwide with tracking 
        and insurance included.</p>
    </div>
    
    <p style="text-align: center; margin-top: 20px;">
        <em>Thank you for considering this beautiful piece for your collection!</em>
    </p>
</div>
        """.strip()
        
        # Product aspects (item specifics)
        aspects = {
            'Artist': [artist],
            'Type': ['Art Print' if 'print' in medium.lower() else 'Original Artwork'],
            'Medium': [medium],
            'Size': [size],
            'Year Created': [str(year)],
            'Condition': [condition],
            'Style': [product_data.get('style', 'Contemporary')],
            'Theme': ['Art'],
            'Country/Region of Manufacture': ['United States']
        }
        
        # Add edition info if available
        if product_data.get('edition'):
            aspects['Edition'] = [product_data['edition']]
        
        ebay_item = {
            'availability': {
                'shipToLocationAvailability': {
                    'quantity': 1
                }
            },
            'condition': self._map_condition_to_ebay(condition),
            'conditionDescription': f"{condition} condition artwork from Gauntlet Gallery",
            'product': {
                'title': ebay_title,
                'description': description,
                'aspects': aspects,
                'imageUrls': self._get_image_urls(product_data),
                'isbn': []  # Not applicable for artwork
            }
        }
        
        return ebay_item
    
    def _map_condition_to_ebay(self, condition: str) -> str:
        """Map internal condition to eBay condition values"""
        condition_map = {
            'mint': 'NEW',
            'excellent': 'LIKE_NEW',
            'very good': 'VERY_GOOD',
            'good': 'GOOD',
            'fair': 'ACCEPTABLE'
        }
        
        return condition_map.get(condition.lower(), 'GOOD')
    
    def _get_image_urls(self, product_data: Dict[str, Any]) -> List[str]:
        """Extract and format image URLs for eBay"""
        images = []
        
        # Get photos from product data
        photos = product_data.get('photos', [])
        for photo in photos[:12]:  # eBay allows max 12 images
            if photo.startswith('http'):
                images.append(photo)
            else:
                # Convert local path to URL (you'll need to host these)
                # For now, return placeholder
                images.append(f"https://your-domain.com{photo}")
        
        # If no images, add placeholder
        if not images:
            images.append("https://via.placeholder.com/800x600/f0f0f0/333333?text=Artwork+Image")
        
        return images
    
    def _parse_ebay_error(self, response) -> str:
        """Parse eBay API error response"""
        try:
            error_data = response.json()
            if 'errors' in error_data:
                errors = []
                for error in error_data['errors']:
                    message = error.get('message', 'Unknown error')
                    error_id = error.get('errorId', '')
                    errors.append(f"{message} ({error_id})" if error_id else message)
                return '; '.join(errors)
            else:
                return f"HTTP {response.status_code}: {response.text[:200]}"
        except:
            return f"HTTP {response.status_code}: {response.text[:200]}"
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get eBay account information"""
        if not self.ensure_valid_token():
            return {'success': False, 'error': 'No valid eBay token'}
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.endpoints['sell_account']}/fulfillment_policy"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return {'success': True, 'account_data': response.json()}
            else:
                return {'success': False, 'error': self._parse_ebay_error(response)}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    # Test eBay API integration
    ebay = eBayAPIIntegration()
    
    print("\\n🧪 eBay API Integration Test")
    print("=" * 40)
    print(f"Environment: {ebay.credentials['environment']}")
    print(f"App ID: {ebay.credentials['app_id']}")
    print("\\n📝 Next steps:")
    print("1. Complete OAuth authorization")
    print("2. Test inventory item creation")
    print("3. Test offer creation and publishing")
    
    # Generate auth URL for testing
    auth_url = ebay.get_auth_url()
    print(f"\\n🔗 Authorization URL:")
    print(auth_url)