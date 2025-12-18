#!/usr/bin/env python3
"""
Demo Data Configuration for SmartAI Fashion Platform
Upload your demo photos and links here
"""

# Demo User Account
DEMO_USER = {
    "name": "Test User",
    "email": "srikrishkodi@gmail.com",
    "avatar": "https://via.placeholder.com/100x100?text=TU"  # Replace with your photo URL
}

# ===== BEST IN ME AGENT DEMO DATA =====

# Your clothing collection photos (replace with your actual image URLs)
DEMO_CLOTHING_COLLECTION = {
    "shirts": [
        {
            "name": "White Cotton Dress Shirt",
            "image_url": "https://raw.githubusercontent.com/KRISHTHICK/SAI-demo-photos/main/whiteshirt.png",  # ✅ Fixed GitHub raw URL
            "description": "Classic white cotton dress shirt with long sleeves"
        },
        {
            "name": "Blue Casual Shirt", 
            "image_url": "YOUR_SHIRT_2_URL_HERE",  # 👈 Upload your shirt photo URL here
            "description": "Light blue casual cotton shirt"
        }
    ],
    "pants": [
        {
            "name": "Black Dress Pants",
            "image_url": "YOUR_PANTS_1_URL_HERE",  # 👈 Upload your pants photo URL here
            "description": "Formal black dress pants with slim fit"
        },
        {
            "name": "Blue Denim Jeans",
            "image_url": "https://raw.githubusercontent.com/KRISHTHICK/SAI-demo-photos/main/pant.png",  # ✅ Fixed GitHub raw URL
            "description": "Classic blue denim jeans with regular fit"
        }
    ],
    "shoes": [
        {
            "name": "Brown Leather Shoes",
            "image_url": "YOUR_SHOES_1_URL_HERE",  # 👈 Upload your shoes photo URL here
            "description": "Brown leather formal shoes with laces"
        }
    ]
}

# Expected outfit result photos (replace with your actual result image URLs)
DEMO_OUTFIT_RESULTS = {
    "wedding_formal": {
        "image_url": "YOUR_WEDDING_OUTFIT_RESULT_URL_HERE",  # 👈 Upload your expected wedding outfit photo
        "description": "Formal wedding outfit with white shirt, black pants, brown shoes"
    },
    "casual_meetup": {
        "image_url": "https://raw.githubusercontent.com/KRISHTHICK/SAI-demo-photos/main/Gemini_Generated_Image_5yzpsl5yzpsl5yzp.png",  # ✅ Fixed GitHub raw URL
        "description": "Casual meetup outfit with white shirt, jeans, brown shoes"
    }
}

# ===== FUSION SUSTAINABLE AGENT DEMO DATA =====

# Your trendy style photos (replace with your actual image URLs)
DEMO_TRENDY_STYLES = {
    "shrewani": {
        "image_url": "https://raw.githubusercontent.com/KRISHTHICK/SAI-demo-photos/main/sharwama.png",  # ✅ Fixed GitHub raw URL
        "description": "Modern shrewani style with urban elements"
    },
    "minimalist": {
        "image_url": "YOUR_TRENDY_MINIMALIST_URL_HERE",  # 👈 Upload your trendy style photo
        "description": "Clean minimalist modern style"
    }
}

# Your traditional style photos (replace with your actual image URLs)
DEMO_TRADITIONAL_STYLES = {
    "Dosti": {
        "image_url": "https://raw.githubusercontent.com/KRISHTHICK/SAI-demo-photos/main/white%20shirt.png",  # ✅ Fixed GitHub raw URL
        "description": "Traditional Indian dosti design"
    },
    "sari": {
        "image_url": "YOUR_TRADITIONAL_SARI_URL_HERE",  # 👈 Upload your traditional style photo
        "description": "Traditional Indian sari with cultural patterns"
    }
}

# Your fusion result photos (replace with your actual fusion result URLs)
DEMO_FUSION_RESULTS = {
    "shrewani_dosti": {
        "image_url": "https://raw.githubusercontent.com/KRISHTHICK/SAI-demo-photos/main/Gemini_Generated_Image_1mwlwy1mwlwy1mwl.png",  # ✅ Fixed GitHub raw URL
        "name": "Urban dosti Fusion",
        "description": "Modern shrewani elements combined with traditional dosti aesthetics"
    },
    "minimalist_sari": {
        "image_url": "YOUR_FUSION_MINIMALIST_SARI_URL_HERE",  # 👈 Upload your fusion result photo
        "name": "Contemporary Sari Fusion", 
        "description": "Minimalist design principles merged with traditional sari draping"
    }
}

# ===== REAL MARKETPLACE LINKS =====

# Your real sustainable clothing links (replace with actual product URLs)
DEMO_MARKETPLACE_PRODUCTS = [
    {
        "name": "Eco-Fusion Cultural Dress",
        "brand": "Sustainable Threads",
        "price": 129,
        "image_url": "YOUR_PRODUCT_1_IMAGE_URL_HERE",  # 👈 Upload product image URL
        "description": "Beautiful fusion of traditional and modern elements",
        "sustainability_score": 4.8,
        "purchase_links": {
            "amazon": "YOUR_AMAZON_PRODUCT_LINK_HERE",  # 👈 Your real Amazon link
            "myntra": "YOUR_MYNTRA_PRODUCT_LINK_HERE",  # 👈 Your real Myntra link
            "trent": "YOUR_TRENT_PRODUCT_LINK_HERE"     # 👈 Your real Trent link
        }
    },
    {
        "name": "Traditional-Modern Fusion Top",
        "brand": "Cultural Heritage Co.",
        "price": 89,
        "image_url": "YOUR_PRODUCT_2_IMAGE_URL_HERE",  # 👈 Upload product image URL
        "description": "Elegant fusion top with contemporary silhouette",
        "sustainability_score": 4.5,
        "purchase_links": {
            "amazon": "YOUR_AMAZON_PRODUCT_LINK_2_HERE",  # 👈 Your real Amazon link
            "myntra": "YOUR_MYNTRA_PRODUCT_LINK_2_HERE",  # 👈 Your real Myntra link
            "trent": "YOUR_TRENT_PRODUCT_LINK_2_HERE"     # 👈 Your real Trent link
        }
    },
    {
        "name": "Sustainable Fusion Accessories",
        "brand": "EcoLux Designs", 
        "price": 65,
        "image_url": "YOUR_PRODUCT_3_IMAGE_URL_HERE",  # 👈 Upload product image URL
        "description": "Complete accessories set from sustainable materials",
        "sustainability_score": 4.3,
        "purchase_links": {
            "amazon": "https://www.amazon.com/Designer-Wedding-Jacquard-Indo-Western-Sherwani/dp/B0F1MMW7JC/ref=asc_df_B0F1MMW7JC?tag=bingshoppinga-20&linkCode=df0&hvadid=80608146995381&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=100903&hvtargid=pla-4584207611399609&msclkid=6a497ee311b31dded21217a0992e46cc&th=1&psc=1",  # 👈 Your real Amazon link
            "andaazfashion" : "https://www.andaazfashion.com/black-jacquard-embroidered-men-sherwani-mstv02000.html",  # 👈 Your real Myntra link
            "ajio": "https://www.ajio.com/kisah-men-embossed-indowestern-sherwani-dhoti-with-dupatta-set/p/466267497_black"     # 👈 Your real Trent link
        }
    }
]

# ===== DEMO SCENARIOS =====

# Predefined demo scenarios that will use your uploaded photos
DEMO_SCENARIOS = {
    "best_in_me_wedding": {
        "event": "wedding",
        "location": "Marriott Hotel Bangalore", 
        "time": "7:00 PM",
        "expected_result": "wedding_formal"
    },
    "best_in_me_casual": {
        "event": "friends meetup",
        "location": "Coffee shop",
        "time": "10:00 AM", 
        "expected_result": "casual_meetup"
    },
    "fusion_shrewani_dosti": {
        "trendy_style": "shrewani",
        "traditional_style": "dosti",
        "expected_result": "shrewani_dosti"
    },
    "fusion_minimalist_sari": {
        "trendy_style": "minimalist", 
        "traditional_style": "sari",
        "expected_result": "minimalist_sari"
    }
}

# ===== INSTRUCTIONS FOR UPLOADING =====
"""
📸 HOW TO UPLOAD YOUR DEMO PHOTOS:

1. Upload your photos to any image hosting service:
   - Google Drive (make public)
   - Imgur
   - GitHub (in a public repo)
   - Any cloud storage with public URLs

2. Replace the placeholder URLs above with your actual image URLs

3. For marketplace links, use real product URLs from:
   - Amazon India
   - Myntra
   - Trent/Westside

4. Save this file after updating all URLs

5. The system will automatically use your photos for demo purposes

EXAMPLE:
Instead of: "YOUR_SHIRT_1_URL_HERE"
Use: "https://i.imgur.com/abc123.jpg"

Instead of: "YOUR_AMAZON_PRODUCT_LINK_HERE" 
Use: "https://www.amazon.in/dp/B08XYZ123"
"""