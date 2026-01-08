#!/usr/bin/env python3
"""
eBay Art Listing Creator
Analyzes art images and generates complete eBay listings
"""

import os
import json
import base64
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class ArtworkAnalysis:
    title: str
    artist: Optional[str]
    medium: str
    style: str
    colors: List[str]
    subject_matter: str
    condition: str
    estimated_year: Optional[str]
    size_category: str
    frame_info: str
    signature_present: bool
    authenticity_markers: List[str]

@dataclass
class EbayListing:
    title: str
    subtitle: Optional[str]
    description: str
    category_id: int
    category_name: str
    condition: str
    condition_description: str
    item_specifics: Dict[str, str]
    suggested_price_min: float
    suggested_price_max: float
    suggested_starting_bid: float
    buy_it_now_price: float
    tags: List[str]
    shipping_weight: str
    dimensions: str
    return_policy: str
    payment_methods: List[str]

class EbayArtAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY', '')
        self.ebay_categories = self._load_ebay_categories()
        self.pricing_database = self._load_pricing_database()
        
    def _load_ebay_categories(self) -> Dict:
        """Load eBay art categories mapping"""
        return {
            'paintings': {
                'oil': 20125,
                'acrylic': 20126,
                'watercolor': 20127,
                'mixed_media': 20128,
                'pastel': 360010001,
                'gouache': 360010002
            },
            'prints': {
                'lithograph': 360010003,
                'screenprint': 360010004,
                'etching': 360010005,
                'giclee': 360010006,
                'woodblock': 360010007,
                'offset_lithograph': 360010008
            },
            'drawings': {
                'pencil': 20130,
                'charcoal': 20131,
                'ink': 20132,
                'colored_pencil': 360010009,
                'marker': 360010010
            },
            'photographs': {
                'vintage': 360010011,
                'contemporary': 360010012,
                'digital': 360010013,
                'film': 360010014
            },
            'sculptures': {
                'bronze': 553,
                'marble': 554,
                'wood': 555,
                'ceramic': 556,
                'metal': 557,
                'glass': 558
            },
            'digital_art': {
                'nft': 360010015,
                'digital_print': 360010016,
                'ai_generated': 360010017
            }
        }
    
    def _load_pricing_database(self) -> Dict:
        """Load pricing guidelines based on artwork characteristics"""
        return {
            'size_multipliers': {
                'miniature': 0.5,
                'small': 0.8,
                'medium': 1.0,
                'large': 1.5,
                'oversized': 2.0
            },
            'condition_multipliers': {
                'mint': 1.2,
                'excellent': 1.0,
                'very_good': 0.8,
                'good': 0.6,
                'fair': 0.4,
                'poor': 0.2
            },
            'medium_base_prices': {
                'oil_painting': 500,
                'acrylic_painting': 350,
                'watercolor': 250,
                'print': 150,
                'photograph': 200,
                'drawing': 180,
                'sculpture': 600,
                'mixed_media': 400,
                'digital': 100
            },
            'authenticity_multipliers': {
                'signed': 1.5,
                'numbered': 1.3,
                'certificate': 2.0,
                'provenance': 2.5
            }
        }
    
    def analyze_image(self, image_path: str) -> ArtworkAnalysis:
        """Analyze artwork image using AI vision API"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Encode image
        with open(image_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        # Prepare vision API request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        prompt = """Analyze this artwork image and provide:
        1. Suggested title (descriptive, marketable)
        2. Artist name (if visible/identifiable)
        3. Medium (oil, acrylic, watercolor, print, etc.)
        4. Style (abstract, impressionist, realist, etc.)
        5. Dominant colors (up to 5)
        6. Subject matter
        7. Condition assessment
        8. Estimated creation period
        9. Size category (miniature/small/medium/large/oversized)
        10. Frame information
        11. Is signature visible?
        12. Any authenticity markers (signature, stamps, certificates, etc.)
        
        Respond in JSON format."""
        
        payload = {
            'model': 'gpt-4-vision-preview',
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': prompt},
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:image/jpeg;base64,{img_base64}'
                            }
                        }
                    ]
                }
            ],
            'max_tokens': 1000
        }
        
        # For demo, return mock analysis
        return self._mock_analysis(image_path)
    
    def _mock_analysis(self, image_path: str) -> ArtworkAnalysis:
        """Generate mock analysis for demonstration"""
        filename = Path(image_path).stem
        
        return ArtworkAnalysis(
            title=f"Contemporary Abstract Composition - {filename}",
            artist="Unknown Artist",
            medium="Acrylic on Canvas",
            style="Abstract Expressionist",
            colors=["Blue", "Red", "Yellow", "White", "Black"],
            subject_matter="Abstract composition with dynamic brushwork",
            condition="Excellent",
            estimated_year="2020-2024",
            size_category="medium",
            frame_info="Unframed, gallery wrapped canvas",
            signature_present=True,
            authenticity_markers=["Artist signature", "Gallery stamp on reverse"]
        )
    
    def determine_category(self, analysis: ArtworkAnalysis) -> Tuple[int, str]:
        """Determine appropriate eBay category based on analysis"""
        medium_lower = analysis.medium.lower()
        
        # Map medium to category
        if 'oil' in medium_lower:
            return 20125, "Art > Paintings > Oil Paintings"
        elif 'acrylic' in medium_lower:
            return 20126, "Art > Paintings > Acrylic Paintings"
        elif 'watercolor' in medium_lower:
            return 20127, "Art > Paintings > Watercolor Paintings"
        elif 'print' in medium_lower or 'lithograph' in medium_lower:
            return 360010003, "Art > Prints > Lithographs"
        elif 'photograph' in medium_lower:
            return 360010011, "Art > Photographs > Contemporary"
        elif 'drawing' in medium_lower or 'pencil' in medium_lower:
            return 20130, "Art > Drawings > Pencil Drawings"
        elif 'sculpture' in medium_lower:
            return 553, "Art > Sculptures > Contemporary"
        elif 'digital' in medium_lower:
            return 360010016, "Art > Digital Art > Digital Prints"
        else:
            return 20128, "Art > Paintings > Mixed Media"
    
    def calculate_pricing(self, analysis: ArtworkAnalysis) -> Tuple[float, float, float, float]:
        """Calculate suggested pricing based on artwork characteristics"""
        # Get base price for medium
        medium_key = analysis.medium.lower().replace(' ', '_')
        base_price = 250  # Default
        
        for key, price in self.pricing_database['medium_base_prices'].items():
            if key in medium_key:
                base_price = price
                break
        
        # Apply size multiplier
        size_mult = self.pricing_database['size_multipliers'].get(
            analysis.size_category, 1.0
        )
        
        # Apply condition multiplier
        condition_mult = self.pricing_database['condition_multipliers'].get(
            analysis.condition.lower(), 0.8
        )
        
        # Apply authenticity multipliers
        auth_mult = 1.0
        if analysis.signature_present:
            auth_mult *= self.pricing_database['authenticity_multipliers']['signed']
        if any('certificate' in marker.lower() for marker in analysis.authenticity_markers):
            auth_mult *= 1.3
        
        # Calculate final price
        estimated_value = base_price * size_mult * condition_mult * auth_mult
        
        # Generate price range
        min_price = estimated_value * 0.7
        max_price = estimated_value * 1.3
        starting_bid = estimated_value * 0.3
        buy_now = estimated_value * 1.1
        
        return (
            round(min_price, 2),
            round(max_price, 2),
            round(starting_bid, 2),
            round(buy_now, 2)
        )
    
    def generate_description(self, analysis: ArtworkAnalysis) -> str:
        """Generate compelling eBay listing description"""
        description = f"""
🎨 {analysis.title}

ARTWORK DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━
• Medium: {analysis.medium}
• Style: {analysis.style}
• Period: {analysis.estimated_year or 'Contemporary'}
• Condition: {analysis.condition}
• Size Category: {analysis.size_category.title()}
• Frame: {analysis.frame_info}

DESCRIPTION:
This captivating {analysis.style.lower()} piece showcases {analysis.subject_matter.lower()}. 
The artwork features a rich palette of {', '.join(analysis.colors[:3])} tones, 
creating a dynamic visual experience that commands attention.

KEY FEATURES:
✓ {analysis.medium} artwork in {analysis.condition.lower()} condition
✓ {'Signed by artist' if analysis.signature_present else 'Unsigned piece'}
✓ {analysis.frame_info}
✓ Perfect for collectors and art enthusiasts

AUTHENTICITY:
"""
        
        if analysis.authenticity_markers:
            for marker in analysis.authenticity_markers:
                description += f"• {marker}\n"
        else:
            description += "• Sold as-is without authentication\n"
        
        description += """
SHIPPING & HANDLING:
• Carefully packaged with protective materials
• Ships within 1-2 business days
• Tracking number provided
• International shipping available

RETURNS:
• 30-day return policy
• Buyer pays return shipping
• Item must be returned in original condition

PAYMENT:
• PayPal accepted
• Immediate payment required for Buy It Now

Please review all photos carefully and ask any questions before bidding.
Thank you for viewing this exceptional artwork!
"""
        return description.strip()
    
    def generate_tags(self, analysis: ArtworkAnalysis) -> List[str]:
        """Generate relevant search tags"""
        tags = []
        
        # Add medium tags
        medium_words = analysis.medium.lower().split()
        tags.extend(medium_words)
        
        # Add style tags
        style_words = analysis.style.lower().split()
        tags.extend(style_words)
        
        # Add color tags
        tags.extend([color.lower() for color in analysis.colors[:3]])
        
        # Add subject tags
        subject_words = analysis.subject_matter.lower().split()
        tags.extend([w for w in subject_words if len(w) > 3][:5])
        
        # Add general tags
        tags.extend([
            'art', 'artwork', 'original', 'handmade', 'wall art',
            'home decor', 'collectible', 'fine art'
        ])
        
        # Add condition tags
        if analysis.condition.lower() in ['mint', 'excellent']:
            tags.append('pristine')
        
        # Add authenticity tags
        if analysis.signature_present:
            tags.extend(['signed', 'authentic'])
        
        # Remove duplicates and limit
        unique_tags = list(dict.fromkeys(tags))
        return unique_tags[:30]  # eBay limit
    
    def create_listing(self, image_path: str) -> EbayListing:
        """Create complete eBay listing from image"""
        # Analyze the image
        analysis = self.analyze_image(image_path)
        
        # Determine category
        category_id, category_name = self.determine_category(analysis)
        
        # Calculate pricing
        min_price, max_price, starting_bid, buy_now = self.calculate_pricing(analysis)
        
        # Generate description
        description = self.generate_description(analysis)
        
        # Generate tags
        tags = self.generate_tags(analysis)
        
        # Create item specifics
        item_specifics = {
            'Type': analysis.medium,
            'Style': analysis.style,
            'Subject': analysis.subject_matter,
            'Size Type/Largest Dimension': analysis.size_category.title(),
            'Features': ', '.join(analysis.authenticity_markers[:3]) if analysis.authenticity_markers else 'Original Artwork',
            'Year of Production': analysis.estimated_year or 'Unknown',
            'Material': 'Canvas' if 'canvas' in analysis.medium.lower() else 'Paper',
            'Framing': 'Framed' if 'framed' in analysis.frame_info.lower() else 'Unframed',
            'Signed': 'Yes' if analysis.signature_present else 'No',
            'Originality': 'Original' if 'print' not in analysis.medium.lower() else 'Print',
            'Color': ', '.join(analysis.colors[:3])
        }
        
        # Create listing object
        listing = EbayListing(
            title=self._format_title(analysis.title),
            subtitle=f"{analysis.style} {analysis.medium}",
            description=description,
            category_id=category_id,
            category_name=category_name,
            condition="Used" if analysis.condition.lower() not in ['mint', 'new'] else "New",
            condition_description=f"Artwork in {analysis.condition.lower()} condition. See photos for details.",
            item_specifics=item_specifics,
            suggested_price_min=min_price,
            suggested_price_max=max_price,
            suggested_starting_bid=starting_bid,
            buy_it_now_price=buy_now,
            tags=tags,
            shipping_weight="2 lbs",
            dimensions="Varies by artwork",
            return_policy="30-day returns accepted",
            payment_methods=["PayPal", "Credit Card", "Debit Card"]
        )
        
        return listing
    
    def _format_title(self, title: str) -> str:
        """Format title to meet eBay requirements (80 char limit)"""
        if len(title) <= 80:
            return title
        return title[:77] + "..."
    
    def batch_process(self, image_folder: str, output_file: str = "ebay_listings.json") -> List[EbayListing]:
        """Process multiple images and generate listings"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        listings = []
        
        folder_path = Path(image_folder)
        if not folder_path.exists():
            raise ValueError(f"Folder not found: {image_folder}")
        
        # Process each image
        for image_file in folder_path.iterdir():
            if image_file.suffix.lower() in image_extensions:
                print(f"Processing: {image_file.name}")
                try:
                    listing = self.create_listing(str(image_file))
                    listings.append(listing)
                    print(f"✓ Created listing: {listing.title}")
                except Exception as e:
                    print(f"✗ Error processing {image_file.name}: {e}")
        
        # Save to JSON
        if listings:
            with open(output_file, 'w') as f:
                listings_data = [asdict(listing) for listing in listings]
                json.dump(listings_data, f, indent=2)
            print(f"\n✓ Saved {len(listings)} listings to {output_file}")
        
        return listings
    
    def export_to_csv(self, listings: List[EbayListing], output_file: str = "ebay_listings.csv"):
        """Export listings to CSV format for bulk upload"""
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'Title', 'Subtitle', 'Category ID', 'Condition', 'Start Price',
                'Buy It Now Price', 'Description', 'PicURL', 'Quantity',
                'Duration', 'Location', 'Payment Methods', 'Shipping Service'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for listing in listings:
                writer.writerow({
                    'Title': listing.title,
                    'Subtitle': listing.subtitle,
                    'Category ID': listing.category_id,
                    'Condition': listing.condition,
                    'Start Price': listing.suggested_starting_bid,
                    'Buy It Now Price': listing.buy_it_now_price,
                    'Description': listing.description[:4000],  # eBay limit
                    'PicURL': '',  # To be filled with actual image URLs
                    'Quantity': 1,
                    'Duration': 7,  # 7-day auction
                    'Location': 'United States',
                    'Payment Methods': '|'.join(listing.payment_methods),
                    'Shipping Service': 'USPS Priority Mail'
                })
        
        print(f"✓ Exported {len(listings)} listings to {output_file}")
    
    def generate_html_preview(self, listing: EbayListing, output_file: str = "listing_preview.html"):
        """Generate HTML preview of the listing"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{listing.title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .listing-container {{
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #0064d2;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #0064d2;
            margin-top: 30px;
        }}
        .price-info {{
            background: #e8f4fd;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .price {{
            font-size: 32px;
            color: #d32f2f;
            font-weight: bold;
        }}
        .specs {{
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 10px;
            margin: 20px 0;
        }}
        .spec-label {{
            font-weight: bold;
            color: #666;
        }}
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 20px 0;
        }}
        .tag {{
            background: #e0e0e0;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
        }}
        .description {{
            white-space: pre-wrap;
            line-height: 1.6;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="listing-container">
        <h1>{listing.title}</h1>
        {f'<h3>{listing.subtitle}</h3>' if listing.subtitle else ''}
        
        <div class="price-info">
            <div>Starting Bid: <span class="price">${listing.suggested_starting_bid:.2f}</span></div>
            <div>Buy It Now: <span class="price">${listing.buy_it_now_price:.2f}</span></div>
            <div style="color: #666; margin-top: 10px;">
                Estimated Value: ${listing.suggested_price_min:.2f} - ${listing.suggested_price_max:.2f}
            </div>
        </div>
        
        <h2>Item Specifics</h2>
        <div class="specs">
            {''.join(f'<div class="spec-label">{k}:</div><div>{v}</div>' for k, v in listing.item_specifics.items())}
        </div>
        
        <h2>Category</h2>
        <p>{listing.category_name}</p>
        
        <h2>Condition</h2>
        <p><strong>{listing.condition}</strong> - {listing.condition_description}</p>
        
        <h2>Description</h2>
        <div class="description">{listing.description}</div>
        
        <h2>Search Tags</h2>
        <div class="tags">
            {''.join(f'<span class="tag">{tag}</span>' for tag in listing.tags)}
        </div>
        
        <h2>Shipping & Payment</h2>
        <ul>
            <li>Weight: {listing.shipping_weight}</li>
            <li>Dimensions: {listing.dimensions}</li>
            <li>Returns: {listing.return_policy}</li>
            <li>Payment Methods: {', '.join(listing.payment_methods)}</li>
        </ul>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"✓ Generated HTML preview: {output_file}")
        return output_file


def main():
    """Example usage"""
    analyzer = EbayArtAnalyzer()
    
    # Example: Single image processing
    image_path = "artwork_sample.jpg"
    
    # Create a sample image for testing
    print("Creating sample artwork for demonstration...")
    
    # For demo purposes, we'll just process with mock data
    if not os.path.exists(image_path):
        # Create a placeholder file for demo
        with open(image_path, 'w') as f:
            f.write("placeholder")
    
    print(f"\nProcessing image: {image_path}")
    listing = analyzer.create_listing(image_path)
    
    print("\n" + "="*60)
    print("EBAY LISTING GENERATED")
    print("="*60)
    print(f"Title: {listing.title}")
    print(f"Category: {listing.category_name}")
    print(f"Starting Bid: ${listing.suggested_starting_bid:.2f}")
    print(f"Buy It Now: ${listing.buy_it_now_price:.2f}")
    print(f"Tags: {', '.join(listing.tags[:10])}...")
    
    # Generate HTML preview
    analyzer.generate_html_preview(listing)
    
    # Save to JSON
    with open('sample_listing.json', 'w') as f:
        json.dump(asdict(listing), f, indent=2)
    
    print("\n✓ Listing saved to sample_listing.json")
    print("✓ HTML preview saved to listing_preview.html")
    
    # Clean up test file
    if os.path.exists(image_path) and os.path.getsize(image_path) < 100:
        os.remove(image_path)

if __name__ == "__main__":
    main()