#!/usr/bin/env python3
"""
eBay Listing Automation for Art Gallery
Automated creation of eBay listings from inventory
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from ebay_api_integration import eBayAPIIntegration

class eBayListingAutomation:
    """Automated eBay listing creation for art gallery"""
    
    def __init__(self):
        """Initialize eBay automation"""
        self.ebay_api = eBayAPIIntegration()
        self.listing_templates = self._load_listing_templates()
        
        print("🎨 eBay Listing Automation for Gauntlet Gallery initialized")
    
    def _load_listing_templates(self) -> Dict[str, Any]:
        """Load listing templates for different art types"""
        return {
            'contemporary': {
                'category_id': '550',  # Art
                'title_template': '{artist} - {title} {medium} {year}',
                'keywords': ['contemporary art', 'modern art', 'gallery', 'original'],
                'condition_note': 'Professional gallery piece in excellent condition'
            },
            'vintage': {
                'category_id': '550',  # Art
                'title_template': 'Vintage {artist} - {title} {year}',
                'keywords': ['vintage art', 'collectible', 'estate', 'authentic'],
                'condition_note': 'Vintage piece with age-appropriate wear'
            },
            'print': {
                'category_id': '550',  # Art
                'title_template': '{artist} {title} Print {edition}',
                'keywords': ['art print', 'limited edition', 'reproduction', 'poster'],
                'condition_note': 'High-quality art print'
            },
            'photography': {
                'category_id': '550',  # Art
                'title_template': '{artist} - {title} Photograph {year}',
                'keywords': ['fine art photography', 'photo', 'print', 'gallery'],
                'condition_note': 'Professional photography print'
            }
        }
    
    def create_listing_from_inventory(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create eBay listing from inventory product"""
        try:
            # Step 1: Determine art type and template
            template = self._select_template(product_data)
            
            # Step 2: Create inventory item
            inventory_result = self.ebay_api.create_inventory_item(product_data)
            if not inventory_result.get('success'):
                return inventory_result
            
            sku = inventory_result['sku']
            price = float(product_data.get('sale_price', 100))
            
            # Step 3: Create offer
            offer_result = self.ebay_api.create_offer(sku, price)
            if not offer_result.get('success'):
                return offer_result
            
            offer_id = offer_result['offer_id']
            
            # Step 4: Publish listing (optional - can be done manually)
            # publish_result = self.ebay_api.publish_offer(offer_id)
            
            result = {
                'success': True,
                'sku': sku,
                'offer_id': offer_id,
                'price': price,
                'template_used': template['title_template'],
                'status': 'draft',  # Change to 'published' if auto-publishing
                'ebay_url': f"https://www.sandbox.ebay.com/itm/{sku}" if self.ebay_api.credentials['environment'] == 'sandbox' else f"https://www.ebay.com/itm/{sku}",
                'message': 'eBay listing created successfully (draft mode)'
            }
            
            # Save listing info
            self._save_listing_info(product_data['sku'], result)
            
            print(f"✅ eBay listing created for {product_data.get('artist', 'Unknown')} - {product_data.get('title', 'Artwork')}")
            
            return result
            
        except Exception as e:
            print(f"❌ eBay listing creation failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def batch_create_listings(self, inventory_products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple eBay listings from inventory"""
        results = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'listings': [],
            'errors': []
        }
        
        for product in inventory_products:
            results['total_processed'] += 1
            
            try:
                listing_result = self.create_listing_from_inventory(product)
                
                if listing_result.get('success'):
                    results['successful'] += 1
                    results['listings'].append(listing_result)
                    
                    print(f"✅ {results['successful']}/{results['total_processed']}: {product.get('artist', 'Unknown')} - {product.get('title', 'Artwork')}")
                else:
                    results['failed'] += 1
                    error_info = {
                        'sku': product.get('sku'),
                        'title': f"{product.get('artist', 'Unknown')} - {product.get('title', 'Artwork')}",
                        'error': listing_result.get('error', 'Unknown error')
                    }
                    results['errors'].append(error_info)
                    
                    print(f"❌ {results['failed']} failed: {error_info['title']} - {error_info['error']}")
                    
            except Exception as e:
                results['failed'] += 1
                error_info = {
                    'sku': product.get('sku'),
                    'title': f"{product.get('artist', 'Unknown')} - {product.get('title', 'Artwork')}",
                    'error': str(e)
                }
                results['errors'].append(error_info)
        
        # Summary
        print(f"\n📊 Batch eBay Listing Results:")
        print(f"   ✅ Successful: {results['successful']}")
        print(f"   ❌ Failed: {results['failed']}")
        print(f"   📦 Total: {results['total_processed']}")
        
        return results
    
    def _select_template(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Select appropriate listing template based on product data"""
        medium = product_data.get('medium', '').lower()
        style = product_data.get('style', '').lower()
        year = product_data.get('year', '')
        
        # Determine template type
        if 'photograph' in medium or 'photo' in medium:
            return self.listing_templates['photography']
        elif 'print' in medium or 'edition' in product_data.get('edition_type', '').lower():
            return self.listing_templates['print']
        elif year and int(str(year)[:4]) < 1990:
            return self.listing_templates['vintage']
        else:
            return self.listing_templates['contemporary']
    
    def _save_listing_info(self, sku: str, listing_data: Dict[str, Any]):
        """Save eBay listing information"""
        listings_file = 'ebay_listings.json'
        
        # Load existing listings
        if os.path.exists(listings_file):
            with open(listings_file, 'r') as f:
                listings = json.load(f)
        else:
            listings = {'listings': {}, 'last_updated': None}
        
        # Add new listing
        listings['listings'][sku] = {
            **listing_data,
            'created_at': datetime.now().isoformat(),
            'gallery': 'Gauntlet Gallery'
        }
        listings['last_updated'] = datetime.now().isoformat()
        
        # Save
        with open(listings_file, 'w') as f:
            json.dump(listings, f, indent=2)
    
    def get_listing_status(self, sku: str) -> Dict[str, Any]:
        """Get status of eBay listing"""
        try:
            listings_file = 'ebay_listings.json'
            if os.path.exists(listings_file):
                with open(listings_file, 'r') as f:
                    listings = json.load(f)
                
                if sku in listings.get('listings', {}):
                    return {'success': True, 'listing': listings['listings'][sku]}
            
            return {'success': False, 'error': 'Listing not found'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_all_listings(self) -> Dict[str, Any]:
        """Get all eBay listings"""
        try:
            listings_file = 'ebay_listings.json'
            if os.path.exists(listings_file):
                with open(listings_file, 'r') as f:
                    listings = json.load(f)
                return {'success': True, 'listings': listings.get('listings', {})}
            else:
                return {'success': True, 'listings': {}}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_listing_preview(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate preview of how the eBay listing will look"""
        try:
            template = self._select_template(product_data)
            
            # Generate title
            title_vars = {
                'artist': product_data.get('artist', 'Unknown Artist'),
                'title': product_data.get('title', 'Artwork'),
                'medium': product_data.get('medium', 'Mixed Media'),
                'year': product_data.get('year', '2024'),
                'edition': product_data.get('edition', '')
            }
            
            ebay_title = template['title_template'].format(**title_vars)
            
            # Truncate title if too long (eBay 80 char limit)
            if len(ebay_title) > 80:
                ebay_title = ebay_title[:77] + "..."
            
            # Generate keywords
            keywords = template['keywords'] + [
                product_data.get('artist', '').lower(),
                product_data.get('style', '').lower(),
                'gauntlet gallery',
                'art'
            ]
            keywords = [k for k in keywords if k]  # Remove empty strings
            
            preview = {
                'title': ebay_title,
                'price': f"${product_data.get('sale_price', 100):.2f}",
                'condition': product_data.get('condition', 'Good'),
                'category': 'Art > Paintings',
                'keywords': ', '.join(keywords[:10]),  # Limit keywords
                'template_type': list(self.listing_templates.keys())[list(self.listing_templates.values()).index(template)],
                'estimated_fees': self._calculate_ebay_fees(float(product_data.get('sale_price', 100))),
                'profit_estimate': self._calculate_profit(product_data)
            }
            
            return {'success': True, 'preview': preview}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _calculate_ebay_fees(self, price: float) -> Dict[str, float]:
        """Calculate estimated eBay fees"""
        # eBay fee structure (approximate for art category)
        insertion_fee = 0.30  # First listing free, then $0.30
        final_value_fee_rate = 0.125  # 12.5% for most categories
        final_value_fee = price * final_value_fee_rate
        
        # PayPal/Payment processing (approximate)
        payment_fee_rate = 0.029  # 2.9% + $0.30
        payment_fee = (price * payment_fee_rate) + 0.30
        
        total_fees = insertion_fee + final_value_fee + payment_fee
        
        return {
            'insertion_fee': insertion_fee,
            'final_value_fee': final_value_fee,
            'payment_processing': payment_fee,
            'total_fees': total_fees,
            'net_amount': price - total_fees
        }
    
    def _calculate_profit(self, product_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate profit estimates"""
        cost = float(product_data.get('cost', 0))
        sale_price = float(product_data.get('sale_price', 100))
        
        fees = self._calculate_ebay_fees(sale_price)
        net_amount = fees['net_amount']
        
        gross_profit = sale_price - cost
        net_profit = net_amount - cost
        profit_margin = (net_profit / sale_price * 100) if sale_price > 0 else 0
        
        return {
            'cost': cost,
            'sale_price': sale_price,
            'gross_profit': gross_profit,
            'net_profit': net_profit,
            'profit_margin': profit_margin,
            'fees_total': fees['total_fees']
        }

if __name__ == "__main__":
    # Test eBay listing automation
    automation = eBayListingAutomation()
    
    # Sample product for testing
    sample_product = {
        'sku': 'TEST-ART-001',
        'artist': 'Test Artist',
        'title': 'Beautiful Landscape',
        'medium': 'Oil on canvas',
        'size': '24x18 inches',
        'year': '2023',
        'condition': 'Excellent',
        'sale_price': 500.0,
        'cost': 200.0,
        'style': 'Contemporary'
    }
    
    print("\\n🧪 Testing eBay Listing Preview")
    preview_result = automation.generate_listing_preview(sample_product)
    
    if preview_result['success']:
        preview = preview_result['preview']
        print(f"Title: {preview['title']}")
        print(f"Price: {preview['price']}")
        print(f"Template: {preview['template_type']}")
        print(f"Estimated Fees: ${preview['estimated_fees']['total_fees']:.2f}")
        print(f"Net Profit: ${preview['profit_estimate']['net_profit']:.2f}")
    else:
        print(f"Preview failed: {preview_result['error']}")
    
    print("\\n📝 Ready for eBay integration with dashboard!")