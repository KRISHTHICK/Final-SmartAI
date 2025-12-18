"""
Sample data for Best in Me Agent demo
Contains base64-encoded sample images for demonstration
Using placeholder images that will be replaced with actual product images
"""

# Sample white dress shirt image - using a white placeholder
# In production, replace with actual base64 encoded image
SAMPLE_WHITE_SHIRT_BASE64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2Y4ZjhmOCIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IiM2NjYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7wn5GVIFdoaXRlIFNoaXJ0PC90ZXh0Pjwvc3ZnPg=="

# Sample blue jeans image - using a blue placeholder
SAMPLE_BLUE_JEANS_BASE64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzRhNjliZCIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IiNmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7wn5GWIEJsdWUgSmVhbnM8L3RleHQ+PC9zdmc+"

# Sample brown shoes image - using a brown placeholder
SAMPLE_BROWN_SHOES_BASE64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzhhNjI0YSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IiNmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7wn5GfIEJyb3duIFNob2VzPC90ZXh0Pjwvc3ZnPg=="

# Sample generated outfit image - man wearing white shirt and jeans
# Using a professional stock photo for realistic demonstration
SAMPLE_OUTFIT_IMAGE_URL = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80"

def get_sample_collection():
    """Returns sample clothing collection for demo"""
    return {
        "shirts": [
            {
                "id": "sample-shirt-001",
                "name": "White cotton dress shirt with long sleeves",
                "image": SAMPLE_WHITE_SHIRT_BASE64.strip(),
                "category": "shirts",
                "added_at": "2024-01-15T10:00:00",
                "is_sample": True
            }
        ],
        "pants": [
            {
                "id": "sample-pants-001",
                "name": "Blue denim jeans with straight fit",
                "image": SAMPLE_BLUE_JEANS_BASE64.strip(),
                "category": "pants",
                "added_at": "2024-01-15T10:00:00",
                "is_sample": True
            }
        ],
        "shoes": [
            {
                "id": "sample-shoes-001",
                "name": "Brown leather casual shoes",
                "image": SAMPLE_BROWN_SHOES_BASE64.strip(),
                "category": "shoes",
                "added_at": "2024-01-15T10:00:00",
                "is_sample": True
            }
        ],
        "socks": [],
        "watches": [],
        "accessories": [],
        "others": []
    }

def get_sample_outfit():
    """Returns sample generated outfit for demo"""
    return {
        "success": True,
        "event": "Friends meetup",
        "location": "Marriott Hotel",
        "time": "10:00 AM",
        "selected_outfit": {
            "shirt": {
                "name": "White cotton dress shirt with long sleeves",
                "image": SAMPLE_WHITE_SHIRT_BASE64.strip(),
                "id": "sample-shirt-001"
            },
            "pants": {
                "name": "Blue denim jeans with straight fit",
                "image": SAMPLE_BLUE_JEANS_BASE64.strip(),
                "id": "sample-pants-001"
            },
            "shoes": {
                "name": "Brown leather casual shoes",
                "image": SAMPLE_BROWN_SHOES_BASE64.strip(),
                "id": "sample-shoes-001"
            }
        },
        "style_description": "Outfit for a Friends meetup at Marriott Hotel at 10:00 AM. The outfit includes: White cotton dress shirt with long sleeves, Blue denim jeans with straight fit, Brown leather casual shoes. Perfect for a casual yet smart look.",
        "image_url": SAMPLE_OUTFIT_IMAGE_URL,
        "image_type": "realistic",
        "generated_at": "2024-01-15T10:00:00",
        "is_sample": True
    }

# URLs for sample images (using free stock photos)
SAMPLE_IMAGE_URLS = {
    "white_shirt": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&q=80",
    "blue_jeans": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&q=80",
    "brown_shoes": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=400&q=80",
    "outfit_result": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80"
}
