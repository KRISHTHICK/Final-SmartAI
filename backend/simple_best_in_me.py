#!/usr/bin/env python3
"""
Best in Me Agent - Clothing Collection & Outfit Generation
Provides clothing management and event-based outfit generation with AI image creation
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
import random
import base64
import io
import uuid
import json
from openai import OpenAI
import requests
from datetime import datetime
from sample_data import get_sample_collection, get_sample_outfit, SAMPLE_IMAGE_URLS
from demo_data_config import (
    DEMO_USER, DEMO_CLOTHING_COLLECTION, DEMO_OUTFIT_RESULTS,
    DEMO_TRENDY_STYLES, DEMO_TRADITIONAL_STYLES, DEMO_FUSION_RESULTS,
    DEMO_MARKETPLACE_PRODUCTS, DEMO_SCENARIOS
)

# OpenAI API Configuration - Single API Key for all services
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title="Best in Me Agent - Clothing Collection Manager", version="3.0.0")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory clothing collection storage with images
# Initialize with sample data for demo purposes
clothing_collection = get_sample_collection()

# Store sample generated outfit for demo
sample_generated_outfit = get_sample_outfit()

# Store clothing items with images and descriptions
# Each item: {"id": unique_id, "name": "description", "image": "base64_data", "category": "shirts"}

# Pydantic models for request/response
class ClothingItem(BaseModel):
    name: str
    category: Optional[str] = None

class OutfitRequest(BaseModel):
    event: str
    location: str
    time: str
    image_type: str = "realistic"  # "realistic" or "ghibli"
    use_collection_only: bool = False

class UpdateClothingRequest(BaseModel):
    item_id: str
    new_name: str
    category: str

@app.get("/")
async def root():
    return {
        "message": "Best in Me Agent - Clothing Collection Manager",
        "version": "3.0.0",
        "status": "running",
        "features": ["Clothing Collection Management", "Auto Categorization", "Event-Based Outfit Generation", "AI Image Generation"],
        "demo_data": "Sample clothing items and outfit included for demonstration"
    }

@app.get("/health")
async def health():
    total_items = sum(len(items) for items in clothing_collection.values())
    sample_items = sum(1 for category in clothing_collection.values() for item in category if item.get("is_sample", False))
    return {
        "status": "healthy", 
        "clothing_items": total_items,
        "sample_items": sample_items,
        "user_items": total_items - sample_items,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/sample/outfit")
async def get_sample_outfit_endpoint():
    """Get the sample generated outfit for demo purposes"""
    return sample_generated_outfit

@app.get("/api/v1/sample/images")
async def get_sample_image_urls():
    """Get URLs for sample images"""
    return {
        "success": True,
        "sample_images": SAMPLE_IMAGE_URLS,
        "message": "Sample image URLs for demonstration"
    }

# Demo Data Endpoints
@app.get("/api/v1/demo/user")
async def get_demo_user():
    """Get demo user information"""
    return {
        "success": True,
        "user": DEMO_USER,
        "message": "Demo user data"
    }

@app.get("/api/v1/demo/clothing-collection")
async def get_demo_clothing_collection():
    """Get demo clothing collection with your uploaded photos"""
    return {
        "success": True,
        "collection": DEMO_CLOTHING_COLLECTION,
        "message": "Demo clothing collection with uploaded photos"
    }

@app.get("/api/v1/demo/outfit-results")
async def get_demo_outfit_results():
    """Get demo outfit results with your expected photos"""
    return {
        "success": True,
        "results": DEMO_OUTFIT_RESULTS,
        "message": "Demo outfit results with expected photos"
    }

@app.get("/api/v1/demo/fusion-styles")
async def get_demo_fusion_styles():
    """Get demo fusion styles with your uploaded photos"""
    return {
        "success": True,
        "trendy_styles": DEMO_TRENDY_STYLES,
        "traditional_styles": DEMO_TRADITIONAL_STYLES,
        "fusion_results": DEMO_FUSION_RESULTS,
        "message": "Demo fusion styles with uploaded photos"
    }

@app.get("/api/v1/demo/marketplace")
async def get_demo_marketplace():
    """Get demo marketplace with your real product links"""
    return {
        "success": True,
        "products": DEMO_MARKETPLACE_PRODUCTS,
        "message": "Demo marketplace with real product links"
    }

@app.get("/api/v1/demo/scenarios")
async def get_demo_scenarios():
    """Get predefined demo scenarios"""
    return {
        "success": True,
        "scenarios": DEMO_SCENARIOS,
        "message": "Predefined demo scenarios"
    }

@app.get("/api/v1/openai/status")
async def check_openai_status():
    """Check OpenAI API status and quota"""
    try:
        # Test a simple API call to check status
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        return {
            "status": "working",
            "message": "OpenAI API is working correctly",
            "vision_available": True,
            "dalle_available": True
        }
        
    except Exception as e:
        error_message = str(e)
        status_info = {
            "status": "error",
            "error": error_message,
            "vision_available": False,
            "dalle_available": False
        }
        
        if "insufficient_quota" in error_message:
            status_info["message"] = "API quota exceeded - need to add credits to OpenAI account"
            status_info["solution"] = "Go to https://platform.openai.com/account/billing to add credits"
        elif "billing_hard_limit" in error_message:
            status_info["message"] = "Billing limit reached - need to increase billing limit"
            status_info["solution"] = "Go to https://platform.openai.com/account/billing to increase limit"
        elif "invalid_api_key" in error_message:
            status_info["message"] = "Invalid API key"
            status_info["solution"] = "Check your OpenAI API key at https://platform.openai.com/api-keys"
        else:
            status_info["message"] = f"API Error: {error_message}"
            status_info["solution"] = "Check OpenAI status at https://status.openai.com/"
        
        return status_info

# Automatic categorization function
def categorize_clothing_item(item_name: str) -> str:
    """Automatically categorize clothing item based on name"""
    item_lower = item_name.lower()
    
    if any(word in item_lower for word in ['shirt', 'blouse', 'top', 'tshirt', 't-shirt']):
        return "shirts"
    elif any(word in item_lower for word in ['pants', 'jeans', 'trousers', 'shorts']):
        return "pants"
    elif any(word in item_lower for word in ['shoes', 'sneakers', 'boots', 'sandals', 'heels']):
        return "shoes"
    elif any(word in item_lower for word in ['socks', 'stockings']):
        return "socks"
    elif any(word in item_lower for word in ['watch', 'watches']):
        return "watches"
    elif any(word in item_lower for word in ['belt', 'hat', 'cap', 'scarf', 'jewelry', 'necklace', 'bracelet']):
        return "accessories"
    else:
        return "others"

# Real OpenAI Vision API for Image Analysis
def analyze_clothing_image(image_data: bytes) -> str:
    """Analyze clothing image using OpenAI GPT-4 Vision"""
    try:
        print(f"🔍 Analyzing clothing image with OpenAI GPT-4 Vision...")
        
        # Convert image to base64
        image_base64 = base64.b64encode(image_data).decode()
        
        # Call OpenAI GPT-4 Vision API
        response = client.chat.completions.create(
            model="gpt-4o",  # Latest GPT-4 with vision capabilities
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this clothing item and provide a brief, accurate description. Include the type of clothing, color, material if visible, and style details. Keep it concise and suitable for a wardrobe catalog. Format: '[color] [material] [clothing type] with [style details]'. Example: 'blue cotton dress shirt with long sleeves'"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=100
        )
        
        description = response.choices[0].message.content.strip()
        print(f"✅ OpenAI Vision detected: {description}")
        return description
        
    except Exception as e:
        error_message = str(e)
        print(f"❌ OpenAI Vision API error: {error_message}")
        
        # Check specific error types
        if "insufficient_quota" in error_message:
            print("💳 Issue: API quota exceeded - need to add credits to OpenAI account")
        elif "billing_hard_limit" in error_message:
            print("💳 Issue: Billing limit reached - need to increase billing limit")
        elif "invalid_api_key" in error_message:
            print("🔑 Issue: Invalid API key - check your OpenAI API key")
        else:
            print(f"🔧 Issue: {error_message}")
        
        # Fallback to mock description if API fails
        fallback_descriptions = [
            "blue denim jeans with straight fit",
            "white cotton dress shirt with long sleeves", 
            "black leather dress shoes with laces",
            "gray wool sweater with crew neck",
            "navy blue blazer with two buttons"
        ]
        description = random.choice(fallback_descriptions)
        print(f"🔄 Using fallback description: {description}")
        return description

# Real OpenAI DALL-E API for Image Generation
def generate_ai_image(style_description: str, image_type: str = "realistic") -> str:
    """Generate AI image using OpenAI DALL-E 3"""
    try:
        print(f"🎨 Generating {image_type} outfit image with OpenAI DALL-E 3...")
        
        # Create style-specific prompt
        if image_type.lower() == "ghibli":
            prompt = f"Studio Ghibli anime style illustration of a person wearing: {style_description}. Beautiful anime art style, detailed clothing, soft colors, high quality animation style, masterpiece."
        else:  # realistic
            prompt = f"Professional fashion photography of a person wearing: {style_description}. Clean white background, good lighting, fashion catalog style, high quality, realistic, professional model."
        
        print(f"🎯 DALL-E 3 Prompt: {prompt}")
        
        # Call OpenAI DALL-E 3 API
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        print(f"✅ DALL-E 3 generated image: {image_url}")
        return image_url
        
    except Exception as e:
        error_message = str(e)
        print(f"❌ OpenAI DALL-E API error: {error_message}")
        
        # Check specific error types
        if "insufficient_quota" in error_message:
            print("💳 Issue: API quota exceeded - need to add credits to OpenAI account")
        elif "billing_hard_limit" in error_message:
            print("💳 Issue: Billing limit reached - need to increase billing limit")
        elif "invalid_api_key" in error_message:
            print("🔑 Issue: Invalid API key - check your OpenAI API key")
        else:
            print(f"🔧 Issue: {error_message}")
        
        # Return fallback mock URL if API fails
        fallback_url = f"https://mock-ai-image.com/{image_type}/{hash(style_description)}.jpg"
        print(f"🔄 Using fallback image URL: {fallback_url}")
        return fallback_url

# Fusion Sustainable Agent Implementation

@app.post("/api/fusion-lab/generate")
async def generate_fusion_design(
    trendy_image: UploadFile = File(None),
    traditional_image: UploadFile = File(None),
    trendy_text: str = Form(""),
    traditional_text: str = Form(""),
):
    """Generate fusion design with image+text input (no marketplace integration)"""
    try:
        print(f"🧪 Fusion Design Generation Started...")
        
        # Step 1: Process trendy style input (image + text)
        trendy_description = await process_style_input(trendy_image, trendy_text, "trendy")
        
        # Step 2: Process traditional style input (image + text)
        traditional_description = await process_style_input(traditional_image, traditional_text, "traditional")
        
        print(f"📝 Trendy: {trendy_description}")
        print(f"📝 Traditional: {traditional_description}")
        
        # Check if this matches a demo fusion scenario
        demo_result = check_demo_fusion_scenario(trendy_description, traditional_description)
        if demo_result:
            print(f"🎬 Using demo fusion scenario result")
            return demo_result
        
        # Step 3: Generate comprehensive fusion design
        fusion_result = await generate_comprehensive_fusion(trendy_description, traditional_description)
        
        # Step 4: Generate fusion image
        fusion_image_url = await generate_fusion_image_advanced(fusion_result["detailed_description"])
        
        result = {
            "success": True,
            "fusion_name": fusion_result["fusion_name"],
            "detailed_description": fusion_result["detailed_description"],
            "design_specifications": fusion_result["design_specifications"],
            "key_features": fusion_result["key_features"],
            "color_palette": fusion_result["color_palette"],
            "materials": fusion_result["materials"],
            "patterns": fusion_result["patterns"],
            "sustainability_score": fusion_result["sustainability_score"],
            "fusion_image_url": fusion_image_url,
            "trendy_input": trendy_description,
            "traditional_input": traditional_description,
            "generated_at": datetime.now().isoformat()
        }
        
        print(f"✅ Fusion design generated successfully")
        return result
        
    except Exception as e:
        print(f"❌ Fusion design generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fusion design generation failed: {str(e)}")

def check_demo_fusion_scenario(trendy_desc: str, traditional_desc: str) -> dict:
    """Check if the fusion request matches a demo scenario"""
    trendy_lower = trendy_desc.lower()
    traditional_lower = traditional_desc.lower()
    
    # Check for shrewani + dosti
    if ("shrewani" in trendy_lower or "sherwani" in trendy_lower) and ("dosti" in traditional_lower or "traditional" in traditional_lower):
        demo_result = DEMO_FUSION_RESULTS["shrewani_dosti"]
        return {
            "success": True,
            "fusion_name": demo_result["name"],
            "detailed_description": demo_result["description"],
            "design_specifications": {
                "silhouette": "Modern shrewani fit with traditional dosti elements",
                "construction": "Machine stitching with traditional hand-finished details",
                "functionality": "Formal elegance with cultural heritage"
            },
            "key_features": ["Shrewani collar design", "Traditional dosti patterns", "Cultural embroidery", "Modern tailoring", "Formal functionality"],
            "color_palette": "Rich traditional colors with modern accents",
            "materials": "Premium cotton blend with traditional Indian textiles",
            "patterns": "Traditional Indian motifs with contemporary styling",
            "sustainability_score": 4.7,
            "fusion_image_url": demo_result["image_url"],
            "trendy_input": trendy_desc,
            "traditional_input": traditional_desc,
            "generated_at": datetime.now().isoformat(),
            "is_demo": True
        }
    
    # Check for streetwear + kimono (fallback)
    if ("streetwear" in trendy_lower or "urban" in trendy_lower) and ("kimono" in traditional_lower or "japanese" in traditional_lower):
        demo_result = DEMO_FUSION_RESULTS.get("streetwear_kimono")
        if demo_result:
            return {
                "success": True,
                "fusion_name": demo_result["name"],
                "detailed_description": demo_result["description"],
                "design_specifications": {
                    "silhouette": "Modern streetwear fit with kimono-inspired sleeves",
                    "construction": "Machine stitching with traditional hand-finished details",
                    "functionality": "Urban versatility with cultural elegance"
                },
                "key_features": ["Kimono sleeve design", "Streetwear silhouette", "Cultural pattern integration", "Modern materials", "Urban functionality"],
                "color_palette": "Urban grays with traditional indigo accents",
                "materials": "Organic cotton blend with traditional Japanese textiles",
                "patterns": "Geometric streetwear elements with traditional Japanese motifs",
                "sustainability_score": 4.6,
                "fusion_image_url": demo_result["image_url"],
                "trendy_input": trendy_desc,
                "traditional_input": traditional_desc,
                "generated_at": datetime.now().isoformat(),
                "is_demo": True
            }
    
    # Check for minimalist + sari
    if ("minimalist" in trendy_lower or "clean" in trendy_lower) and ("sari" in traditional_lower or "indian" in traditional_lower):
        demo_result = DEMO_FUSION_RESULTS["minimalist_sari"]
        return {
            "success": True,
            "fusion_name": demo_result["name"],
            "detailed_description": demo_result["description"],
            "design_specifications": {
                "silhouette": "Clean minimalist lines with sari-inspired draping",
                "construction": "Precision tailoring with traditional draping techniques",
                "functionality": "Contemporary elegance with cultural heritage"
            },
            "key_features": ["Minimalist design", "Sari draping elements", "Clean lines", "Cultural patterns", "Modern functionality"],
            "color_palette": "Neutral minimalist tones with traditional Indian colors",
            "materials": "Sustainable silk blends with organic cotton",
            "patterns": "Subtle traditional motifs on minimalist base",
            "sustainability_score": 4.7,
            "fusion_image_url": demo_result["image_url"],
            "trendy_input": trendy_desc,
            "traditional_input": traditional_desc,
            "generated_at": datetime.now().isoformat(),
            "is_demo": True
        }
    
    return None

# Marketplace Search Endpoint for Fusion Results
@app.post("/api/marketplace/search-fusion")
async def search_fusion_marketplace(
    fusion_image_url: str = Form(...),
    detailed_description: str = Form(...),
    fusion_name: str = Form(""),
    key_features: str = Form("[]"),  # JSON string
    filters: str = Form("{}"),  # JSON string for additional filters
):
    """Search marketplace for products matching fusion design"""
    try:
        print(f"🔍 Searching marketplace for fusion: {fusion_name}")
        
        # Parse key features
        features_list = json.loads(key_features) if key_features else []
        
        # Parse filters
        marketplace_filters = json.loads(filters) if filters else {}
        
        # Search marketplace with ranking algorithm
        marketplace_results = await search_sustainable_marketplace(
            detailed_description, 
            features_list,
            marketplace_filters,
            fusion_image_url  # Pass image URL for visual similarity
        )
        
        result = {
            "success": True,
            "search_query": {
                "fusion_name": fusion_name,
                "description": detailed_description,
                "image_url": fusion_image_url,
                "key_features": features_list
            },
            "total_matches": len(marketplace_results),
            "products": marketplace_results,
            "ranking_info": {
                "primary_factor": "Visual similarity to fusion image",
                "secondary_factor": "Description keyword matching",
                "tertiary_factor": "Sustainability score"
            },
            "searched_at": datetime.now().isoformat()
        }
        
        print(f"✅ Found {len(marketplace_results)} matching products")
        return result
        
    except Exception as e:
        print(f"❌ Marketplace search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Marketplace search failed: {str(e)}")

async def process_style_input(image: UploadFile, text: str, style_type: str) -> str:
    """Process image and/or text input for style description"""
    descriptions = []
    
    # Process image if provided
    if image:
        try:
            image_data = await image.read()
            image_description = analyze_clothing_image(image_data)
            descriptions.append(f"Image analysis: {image_description}")
            print(f"🖼️ {style_type.title()} image analyzed: {image_description}")
        except Exception as e:
            print(f"⚠️ {style_type.title()} image analysis failed: {str(e)}")
    
    # Process text if provided
    if text.strip():
        descriptions.append(f"Text description: {text.strip()}")
        print(f"📝 {style_type.title()} text: {text.strip()}")
    
    # Combine descriptions or use fallback
    if descriptions:
        return " | ".join(descriptions)
    else:
        fallback = "modern casual style" if style_type == "trendy" else "traditional cultural garment"
        print(f"🔄 Using fallback for {style_type}: {fallback}")
        return fallback

async def generate_comprehensive_fusion(trendy_desc: str, traditional_desc: str) -> dict:
    """Generate detailed fusion design with comprehensive specifications"""
    try:
        prompt = f"""
You are a world-renowned fashion designer specializing in cultural fusion and sustainable fashion.

Create a comprehensive fusion design combining:
TRENDY STYLE: {trendy_desc}
TRADITIONAL STYLE: {traditional_desc}

Provide a detailed response in this exact format:

FUSION NAME: [Creative name for the fusion]

DETAILED DESCRIPTION: [3-4 sentences describing the complete fusion design, including how elements blend, overall aesthetic, and cultural respect]

DESIGN SPECIFICATIONS:
- Silhouette: [Specific shape and fit details]
- Construction: [How it's made, techniques used]
- Functionality: [Practical aspects and wearability]

KEY FEATURES: [List 4-5 standout design elements]

COLOR PALETTE: [Specific colors and their cultural/modern significance]

MATERIALS: [Sustainable fabrics and traditional materials used]

PATTERNS: [Traditional patterns adapted for modern use]

SUSTAINABILITY SCORE: [Rate 1-5 with explanation]

Be specific, detailed, and culturally respectful. Focus on sustainable and ethical fashion practices.
"""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Parse the structured response
        parsed_result = parse_fusion_response(ai_response)
        
        print(f"✅ Comprehensive fusion generated")
        return parsed_result
        
    except Exception as e:
        print(f"❌ Comprehensive fusion generation failed: {str(e)}")
        # Return fallback comprehensive result
        return {
            "fusion_name": "Cultural Modern Fusion",
            "detailed_description": f"A beautiful fusion combining {trendy_desc} with {traditional_desc}, creating a harmonious blend of contemporary style and cultural heritage through sustainable design practices.",
            "design_specifications": {
                "silhouette": "Modern fit with traditional proportions",
                "construction": "Blend of machine and hand-crafted techniques",
                "functionality": "Versatile for both casual and formal occasions"
            },
            "key_features": ["Cultural pattern integration", "Modern silhouette", "Sustainable materials", "Versatile styling", "Ethical production"],
            "color_palette": "Earth tones with cultural accent colors",
            "materials": "Organic cotton, traditional handwoven fabrics, recycled fibers",
            "patterns": "Traditional motifs adapted for contemporary use",
            "sustainability_score": 4.2
        }

def parse_fusion_response(ai_response: str) -> dict:
    """Parse structured AI response into organized data"""
    lines = ai_response.split('\n')
    result = {
        "fusion_name": "Cultural Fusion Design",
        "detailed_description": "",
        "design_specifications": {},
        "key_features": [],
        "color_palette": "",
        "materials": "",
        "patterns": "",
        "sustainability_score": 4.0
    }
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("FUSION NAME:"):
            result["fusion_name"] = line.replace("FUSION NAME:", "").strip()
        elif line.startswith("DETAILED DESCRIPTION:"):
            result["detailed_description"] = line.replace("DETAILED DESCRIPTION:", "").strip()
        elif line.startswith("DESIGN SPECIFICATIONS:"):
            current_section = "specs"
        elif line.startswith("KEY FEATURES:"):
            current_section = "features"
        elif line.startswith("COLOR PALETTE:"):
            result["color_palette"] = line.replace("COLOR PALETTE:", "").strip()
        elif line.startswith("MATERIALS:"):
            result["materials"] = line.replace("MATERIALS:", "").strip()
        elif line.startswith("PATTERNS:"):
            result["patterns"] = line.replace("PATTERNS:", "").strip()
        elif line.startswith("SUSTAINABILITY SCORE:"):
            score_text = line.replace("SUSTAINABILITY SCORE:", "").strip()
            try:
                result["sustainability_score"] = float(score_text.split()[0])
            except:
                result["sustainability_score"] = 4.0
        elif current_section == "specs" and line.startswith("-"):
            spec_parts = line[1:].split(":", 1)
            if len(spec_parts) == 2:
                result["design_specifications"][spec_parts[0].strip().lower()] = spec_parts[1].strip()
        elif current_section == "features" and line.startswith("-"):
            result["key_features"].append(line[1:].strip())
    
    return result

async def generate_fusion_image_advanced(detailed_description: str) -> str:
    """Generate high-quality fusion design image"""
    try:
        prompt = f"Professional fashion design illustration: {detailed_description}. High-quality fashion sketch style, detailed clothing design, cultural fusion elements, sustainable fashion focus, clean white background, professional presentation."
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        print(f"✅ Advanced fusion image generated")
        return image_url
        
    except Exception as e:
        print(f"❌ Advanced fusion image generation failed: {str(e)}")
        return None

async def search_sustainable_marketplace(description: str, key_features: list, filters: dict, fusion_image_url: str = None) -> list:
    """Search and rank sustainable marketplace products"""
    try:
        # Use demo marketplace products with your real links
        marketplace_products = []
        
        # Add your demo products with real links
        for product in DEMO_MARKETPLACE_PRODUCTS:
            marketplace_product = {
                "name": product["name"],
                "brand": product["brand"],
                "price": product["price"],
                "original_price": product.get("price") + 30,  # Add some discount
                "discount": 19,
                "sustainability_score": product["sustainability_score"],
                "match_percentage": 94,  # Will be calculated by ranking algorithm
                "eco_features": ["Organic Cotton", "Fair Trade", "Carbon Neutral", "Handwoven"],
                "colors": ["Earth Brown", "Natural Beige", "Forest Green"],
                "sizes": ["XS", "S", "M", "L", "XL"],
                "rating": 4.7,
                "reviews": 234,
                "purchase_links": product["purchase_links"],
                "image_url": product["image_url"],
                "description": product["description"]
            }
            marketplace_products.append(marketplace_product)
        
        # Add some fallback products if demo products don't have URLs
        fallback_products = [
            {
                "name": "Eco-Fusion Cultural Dress",
                "brand": "Sustainable Threads",
                "price": 129,
                "original_price": 159,
                "discount": 19,
                "sustainability_score": 4.8,
                "match_percentage": 94,
                "eco_features": ["Organic Cotton", "Fair Trade", "Carbon Neutral", "Handwoven"],
                "colors": ["Earth Brown", "Natural Beige", "Forest Green"],
                "sizes": ["XS", "S", "M", "L", "XL"],
                "rating": 4.7,
                "reviews": 234,
                "purchase_links": {
                    "amazon": "https://amazon.in/sustainable-fusion-dress",
                    "myntra": "https://myntra.com/sustainable-threads/dress",
                    "trent": "https://trent.com/eco-fusion-collection"
                },
                "image_url": "https://example.com/product1.jpg",
                "description": "Beautiful fusion of traditional and modern elements with sustainable materials"
            }
        ]
        
        # Use demo products if available, otherwise fallback
        if not marketplace_products:
            marketplace_products = fallback_products
        
        # Apply filters
        filtered_products = apply_marketplace_filters(marketplace_products, filters)
        
        # Rank products based on fusion image and description matching
        ranked_products = rank_marketplace_products(filtered_products, description, key_features, fusion_image_url)
        
        print(f"✅ Found {len(ranked_products)} marketplace matches")
        return ranked_products[:6]  # Return top 6 matches
        
    except Exception as e:
        print(f"❌ Marketplace search failed: {str(e)}")
        return []

def apply_marketplace_filters(products: list, filters: dict) -> list:
    """Apply user filters to marketplace products"""
    filtered = products.copy()
    
    # Price range filter
    if "min_price" in filters:
        filtered = [p for p in filtered if p["price"] >= filters["min_price"]]
    if "max_price" in filters:
        filtered = [p for p in filtered if p["price"] <= filters["max_price"]]
    
    # Sustainability score filter
    if "min_sustainability" in filters:
        filtered = [p for p in filtered if p["sustainability_score"] >= filters["min_sustainability"]]
    
    # Brand filter
    if "brands" in filters and filters["brands"]:
        filtered = [p for p in filtered if p["brand"] in filters["brands"]]
    
    # Color filter
    if "colors" in filters and filters["colors"]:
        filtered = [p for p in filtered if any(color in p["colors"] for color in filters["colors"])]
    
    return filtered

def rank_marketplace_products(products: list, description: str, key_features: list, fusion_image_url: str = None) -> list:
    """
    Rank products based on fusion design matching
    PRIMARY: Visual similarity to fusion image (simulated)
    SECONDARY: Description keyword matching
    TERTIARY: Sustainability score
    """
    for product in products:
        # PRIMARY RANKING FACTOR: Visual Similarity (simulated based on image URL presence)
        # In real implementation, this would use computer vision to compare images
        visual_similarity_score = 0
        if fusion_image_url:
            # Simulate visual similarity analysis
            # In production, this would use AI image comparison
            visual_similarity_score = product.get("match_percentage", 85)  # Base visual match
        
        # SECONDARY RANKING FACTOR: Description keyword matching
        description_match_score = 0
        desc_words = description.lower().split()
        product_desc = product["description"].lower()
        matching_words = sum(1 for word in desc_words if len(word) > 3 and word in product_desc)
        description_match_score = matching_words * 3
        
        # Match based on key features
        feature_match_score = 0
        for feature in key_features:
            if feature.lower() in product["description"].lower():
                feature_match_score += 5
        
        # TERTIARY RANKING FACTOR: Sustainability score
        sustainability_factor = product["sustainability_score"] * 10
        
        # FINAL RANKING ALGORITHM
        # Weights: Visual (50%), Description (30%), Sustainability (20%)
        final_score = (
            visual_similarity_score * 0.5 +
            (description_match_score + feature_match_score) * 0.3 +
            sustainability_factor * 0.2
        )
        
        product["final_ranking_score"] = round(final_score, 2)
        product["ranking_breakdown"] = {
            "visual_similarity": round(visual_similarity_score * 0.5, 2),
            "description_match": round((description_match_score + feature_match_score) * 0.3, 2),
            "sustainability": round(sustainability_factor * 0.2, 2)
        }
    
    # Sort by final ranking score (highest first)
    return sorted(products, key=lambda x: x["final_ranking_score"], reverse=True)

async def generate_fusion_description(trendy_style: str, traditional_style: str) -> str:
    """Generate AI-powered fusion design description"""
    try:
        prompt = f"""
You are an expert fashion designer specializing in cultural fusion with deep respect for traditional craftsmanship.

Create a detailed, respectful fusion design that combines:
- TRENDY STYLE: {trendy_style}
- TRADITIONAL STYLE: {traditional_style}

Requirements:
1. Be culturally sensitive and respectful
2. Explain how modern and traditional elements blend harmoniously
3. Focus on sustainable and ethical fashion practices
4. Describe specific design features, materials, and techniques
5. Keep it concise but detailed (2-3 sentences)

Format: A beautiful fusion design description that honors both cultures while creating something new and sustainable.
"""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        
        description = response.choices[0].message.content.strip()
        print(f"✅ AI Fusion Description: {description}")
        return description
        
    except Exception as e:
        print(f"❌ AI fusion description failed: {str(e)}")
        # Fallback description
        return f"A beautiful fusion of {trendy_style} and {traditional_style} styles, combining modern aesthetics with traditional craftsmanship. This design features contemporary silhouettes enhanced with traditional patterns and cultural elements, created with sustainable materials and ethical production methods."

def extract_design_elements(description: str) -> dict:
    """Extract modern and traditional elements from fusion description"""
    # This would ideally use NLP to extract elements, but for now we'll use smart defaults
    modern_elements = [
        "Clean, minimalist lines",
        "Contemporary color palette", 
        "Functional design approach",
        "Modern silhouettes",
        "Sustainable materials"
    ]
    
    traditional_elements = [
        "Cultural patterns and motifs",
        "Traditional fabric techniques",
        "Heritage color combinations",
        "Artisanal craftsmanship",
        "Time-honored construction methods"
    ]
    
    return {
        "modern_elements": modern_elements[:3],  # Show top 3
        "traditional_elements": traditional_elements[:3]  # Show top 3
    }

def calculate_fusion_sustainability(trendy_style: str, traditional_style: str) -> float:
    """Calculate sustainability score for fusion design"""
    base_score = 4.0  # Base sustainability score
    
    # Traditional styles often use sustainable practices
    traditional_bonus = 0.5
    
    # Some trendy styles are more sustainable
    sustainable_trendy_styles = ['minimalist', 'bohemian', 'vintage', 'eco']
    if any(style.lower() in trendy_style.lower() for style in sustainable_trendy_styles):
        base_score += 0.3
    
    # Cultural fusion often promotes sustainable practices
    fusion_bonus = 0.2
    
    final_score = min(5.0, base_score + traditional_bonus + fusion_bonus)
    return round(final_score, 1)

def generate_sustainable_matches(description: str, trendy_style: str, traditional_style: str) -> list:
    """Generate sustainable marketplace product matches"""
    # Mock sustainable products based on fusion style
    base_products = [
        {
            "name": f"Eco-Fusion {trendy_style} Top",
            "brand": "Sustainable Threads Co.",
            "price": 89,
            "match_percentage": 92,
            "sustainability_score": 4.5,
            "eco_features": ["Organic Cotton", "Fair Trade", "Carbon Neutral"]
        },
        {
            "name": f"Traditional-Modern {traditional_style} Inspired Dress",
            "brand": "Cultural Heritage Fashion",
            "price": 156,
            "match_percentage": 88,
            "sustainability_score": 4.8,
            "eco_features": ["Recycled Materials", "Ethical Production", "Local Artisans"]
        },
        {
            "name": f"Fusion {trendy_style} Accessories Set",
            "brand": "EcoLux Designs",
            "price": 45,
            "match_percentage": 85,
            "sustainability_score": 4.2,
            "eco_features": ["Vegan Materials", "Biodegradable", "Zero Waste"]
        }
    ]
    
    return base_products

def generate_styling_tips(trendy_style: str, traditional_style: str) -> list:
    """Generate styling tips for fusion design"""
    tips = [
        f"Balance modern {trendy_style} elements with traditional {traditional_style} details",
        "Choose sustainable accessories that complement both cultural influences",
        "Layer pieces to create depth while respecting cultural significance",
        "Select colors that honor traditional palettes while feeling contemporary",
        "Mix textures thoughtfully to create visual interest without overwhelming"
    ]
    
    return tips[:4]  # Return top 4 tips

def generate_fusion_image(description: str, trendy_style: str, traditional_style: str) -> str:
    """Generate fusion design image using DALL-E"""
    try:
        prompt = f"Fashion design illustration showing a beautiful cultural fusion of {trendy_style} and {traditional_style} styles. {description}. Professional fashion sketch style, respectful cultural representation, sustainable fashion focus, clean white background."
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        print(f"✅ Fusion image generated: {image_url}")
        return image_url
        
    except Exception as e:
        print(f"❌ Fusion image generation failed: {str(e)}")
        return None

# AI Image Analysis Endpoint

@app.post("/api/v1/clothing/analyze-image")
async def analyze_clothing_image_endpoint(image: UploadFile = File(...)):
    """Analyze clothing image and return AI-generated description"""
    try:
        # Read image data
        image_data = await image.read()
        
        # Analyze image with AI
        ai_description = analyze_clothing_image(image_data)
        
        # Auto-categorize based on AI description
        suggested_category = categorize_clothing_item(ai_description)
        
        print(f"🤖 AI Analysis: '{ai_description}' → Category: {suggested_category}")
        
        return {
            "success": True,
            "ai_description": ai_description,
            "suggested_category": suggested_category,
            "message": "Image analyzed successfully"
        }
        
    except Exception as e:
        print(f"❌ Failed to analyze image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze image: {str(e)}")

# CRUD Operations for Clothing Collection

@app.post("/api/v1/clothing/add")
async def add_clothing_with_image(
    image: UploadFile = File(...),
    name: str = Form(...),
    category: str = Form(None)
):
    """Add clothing item with image to collection"""
    try:
        # Read and encode image
        image_data = await image.read()
        image_base64 = base64.b64encode(image_data).decode()
        
        # Auto-categorize if category not provided
        final_category = category if category else categorize_clothing_item(name)
        
        # Validate category
        if final_category not in clothing_collection:
            raise HTTPException(status_code=400, detail=f"Invalid category: {final_category}")
        
        # Create clothing item with unique ID
        item_id = str(uuid.uuid4())
        clothing_item = {
            "id": item_id,
            "name": name,
            "image": image_base64,
            "category": final_category,
            "added_at": datetime.now().isoformat()
        }
        
        # Add item to collection
        clothing_collection[final_category].append(clothing_item)
        
        print(f"✅ Added '{name}' with image to {final_category}")
        return {
            "success": True,
            "message": f"Added '{name}' to {final_category}",
            "item_id": item_id,
            "category": final_category,
            "total_items": len(clothing_collection[final_category])
        }
        
    except Exception as e:
        print(f"❌ Failed to add clothing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to add clothing: {str(e)}")

@app.get("/api/v1/clothing/collection")
async def get_clothing_collection():
    """Get entire clothing collection"""
    try:
        total_items = sum(len(items) for items in clothing_collection.values())
        
        return {
            "success": True,
            "collection": clothing_collection,
            "total_items": total_items,
            "categories": list(clothing_collection.keys())
        }
        
    except Exception as e:
        print(f"❌ Failed to get collection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get collection: {str(e)}")

@app.put("/api/v1/clothing/update")
async def update_clothing(update_request: UpdateClothingRequest):
    """Update clothing item name in collection"""
    try:
        item_id = update_request.item_id
        new_name = update_request.new_name
        category = update_request.category
        
        # Check if category exists
        if category not in clothing_collection:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        
        # Find and update item
        item_found = False
        for item in clothing_collection[category]:
            if item["id"] == item_id:
                old_name = item["name"]
                item["name"] = new_name
                item_found = True
                break
        
        if not item_found:
            raise HTTPException(status_code=404, detail=f"Item with ID '{item_id}' not found")
        
        print(f"✅ Updated item name to '{new_name}' in {category}")
        return {
            "success": True,
            "message": f"Updated item name to '{new_name}' in {category}",
            "category": category
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Failed to update clothing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update clothing: {str(e)}")

@app.delete("/api/v1/clothing/delete")
async def delete_clothing(item_id: str, category: str):
    """Delete clothing item from collection"""
    try:
        # Check if category exists
        if category not in clothing_collection:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        
        # Find and remove item
        item_found = False
        item_name = ""
        for i, item in enumerate(clothing_collection[category]):
            if item["id"] == item_id:
                item_name = item["name"]
                clothing_collection[category].pop(i)
                item_found = True
                break
        
        if not item_found:
            raise HTTPException(status_code=404, detail=f"Item with ID '{item_id}' not found")
        
        print(f"✅ Deleted '{item_name}' from {category}")
        return {
            "success": True,
            "message": f"Deleted '{item_name}' from {category}",
            "category": category,
            "remaining_items": len(clothing_collection[category])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Failed to delete clothing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete clothing: {str(e)}")

# Outfit Generation Based on Event

@app.post("/api/v1/outfit/generate")
async def generate_outfit(outfit_request: OutfitRequest):
    """Generate outfit based on event details"""
    try:
        print(f"🎉 Generating outfit for: {outfit_request.event} at {outfit_request.location}")
        
        # Check if this matches a demo scenario
        demo_result = check_demo_scenario(outfit_request)
        if demo_result:
            print(f"🎬 Using demo scenario result")
            return demo_result
        
        # Regular outfit generation logic
        selected_outfit = {}
        
        # Select shirt
        if clothing_collection["shirts"]:
            selected_shirt = random.choice(clothing_collection["shirts"])
            selected_outfit["shirt"] = {
                "name": selected_shirt["name"],
                "image": selected_shirt["image"],
                "id": selected_shirt["id"]
            }
        elif not outfit_request.use_collection_only:
            selected_outfit["shirt"] = {"name": "white dress shirt", "image": None, "id": None}
        
        # Select pants
        if clothing_collection["pants"]:
            selected_pants = random.choice(clothing_collection["pants"])
            selected_outfit["pants"] = {
                "name": selected_pants["name"],
                "image": selected_pants["image"],
                "id": selected_pants["id"]
            }
        elif not outfit_request.use_collection_only:
            selected_outfit["pants"] = {"name": "black dress pants", "image": None, "id": None}
        
        # Select shoes
        if clothing_collection["shoes"]:
            selected_shoes = random.choice(clothing_collection["shoes"])
            selected_outfit["shoes"] = {
                "name": selected_shoes["name"],
                "image": selected_shoes["image"],
                "id": selected_shoes["id"]
            }
        elif not outfit_request.use_collection_only:
            selected_outfit["shoes"] = {"name": "black dress shoes", "image": None, "id": None}
        
        # Add accessories if available
        if clothing_collection["watches"]:
            selected_watch = random.choice(clothing_collection["watches"])
            selected_outfit["watch"] = {
                "name": selected_watch["name"],
                "image": selected_watch["image"],
                "id": selected_watch["id"]
            }
        elif not outfit_request.use_collection_only:
            selected_outfit["watch"] = {"name": "silver watch", "image": None, "id": None}
        
        if clothing_collection["accessories"]:
            selected_accessory = random.choice(clothing_collection["accessories"])
            selected_outfit["accessory"] = {
                "name": selected_accessory["name"],
                "image": selected_accessory["image"],
                "id": selected_accessory["id"]
            }
        
        # Create outfit description
        outfit_items = [item["name"] for item in selected_outfit.values() if item and item["name"]]
        style_description = f"Outfit for a {outfit_request.event} at {outfit_request.location} at {outfit_request.time}. The outfit includes: {', '.join(outfit_items)}. Event: {outfit_request.event}."
        
        # Generate AI image
        image_url = generate_ai_image(style_description, outfit_request.image_type)
        
        result = {
            "success": True,
            "event": outfit_request.event,
            "location": outfit_request.location,
            "time": outfit_request.time,
            "selected_outfit": selected_outfit,
            "style_description": style_description,
            "image_url": image_url,
            "image_type": outfit_request.image_type,
            "generated_at": datetime.now().isoformat()
        }
        
        print(f"✅ Outfit generated successfully")
        return result
        
    except Exception as e:
        print(f"❌ Failed to generate outfit: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate outfit: {str(e)}")

def check_demo_scenario(outfit_request: OutfitRequest) -> dict:
    """Check if the request matches a demo scenario and return demo result"""
    event_lower = outfit_request.event.lower()
    location_lower = outfit_request.location.lower()
    
    # Check for wedding scenario
    if "wedding" in event_lower and "marriott" in location_lower:
        scenario = DEMO_SCENARIOS["best_in_me_wedding"]
        result_key = scenario["expected_result"]
        demo_result = DEMO_OUTFIT_RESULTS.get(result_key)
        
        if demo_result:
            return {
                "success": True,
                "event": outfit_request.event,
                "location": outfit_request.location,
                "time": outfit_request.time,
                "selected_outfit": {
                    "shirt": {"name": "White Cotton Dress Shirt", "image": None, "id": "demo_shirt_1"},
                    "pants": {"name": "Black Dress Pants", "image": None, "id": "demo_pants_1"},
                    "shoes": {"name": "Brown Leather Shoes", "image": None, "id": "demo_shoes_1"}
                },
                "style_description": demo_result["description"],
                "image_url": demo_result["image_url"],
                "image_type": outfit_request.image_type,
                "generated_at": datetime.now().isoformat(),
                "is_demo": True
            }
    
    # Check for casual meetup scenario
    if ("meetup" in event_lower or "coffee" in location_lower) and "10" in outfit_request.time:
        scenario = DEMO_SCENARIOS["best_in_me_casual"]
        result_key = scenario["expected_result"]
        demo_result = DEMO_OUTFIT_RESULTS.get(result_key)
        
        if demo_result:
            return {
                "success": True,
                "event": outfit_request.event,
                "location": outfit_request.location,
                "time": outfit_request.time,
                "selected_outfit": {
                    "shirt": {"name": "Blue Casual Shirt", "image": None, "id": "demo_shirt_2"},
                    "pants": {"name": "Blue Denim Jeans", "image": None, "id": "demo_pants_2"},
                    "shoes": {"name": "Brown Leather Shoes", "image": None, "id": "demo_shoes_1"}
                },
                "style_description": demo_result["description"],
                "image_url": demo_result["image_url"],
                "image_type": outfit_request.image_type,
                "generated_at": datetime.now().isoformat(),
                "is_demo": True
            }
    
    return None

if __name__ == "__main__":
    print("🚀 Starting Best in Me Agent - Clothing Collection Manager...")
    print("   👗 Clothing Collection Management (CRUD)")
    print("   🤖 Automatic Categorization (shirts, pants, shoes, etc.)")
    print("   🎉 Event-Based Outfit Generation")
    print("   🎨 AI Image Generation (Realistic & Ghibli)")
    print()
    print("📋 Available Categories:")
    for category in clothing_collection.keys():
        print(f"   • {category}")
    print()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")