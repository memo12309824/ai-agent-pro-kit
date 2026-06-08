#!/usr/bin/env python3
"""
Gumroad Auto-Setup Script for AI Agent Pro Kit
Run this after you get your Gumroad access token.
"""

import json, urllib.request, base64, os

GUMROAD_API = "https://api.gumroad.com/v2"

def setup_products(access_token):
    """Create all 3 product tiers on Gumroad"""
    
    params = f"access_token={access_token}"
    
    products = [
        {
            "name": "AI Agent Pro Kit — Pro",
            "price": 490,  # ¥49 = 490 cents
            "description": "🤖 AI Agent Pro Kit (Pro Tier)\n\nIncludes:\n• FreeLLMAPI (98 AI models, one API)\n• Docker Compose one-click deploy\n• Exa Neural Search integration\n• Hermes Agent config templates\n• Setup scripts & documentation\n\n📦 Delivered via GitHub private repo access",
            "file": "pro/setup.sh",
            "customizable_price": False,
            "max_purchase_count": None,
        },
        {
            "name": "AI Agent Pro Kit — Enterprise",
            "price": 4990,  # ¥499 = 4990 cents
            "description": "🤖 AI Agent Pro Kit (Enterprise Tier)\n\nEverything in Pro, plus:\n• Custom integration scripts\n• Priority 24h support\n• Custom model routing configs\n• Early access to new features\n• Private channel access\n\n📦 Delivered via GitHub private repo + email",
            "file": None,
            "customizable_price": False,
            "max_purchase_count": None,
        }
    ]
    
    results = []
    for product in products:
        # Build form data
        data = {
            "access_token": access_token,
            "name": product["name"],
            "price": product["price"],
            "description": product["description"],
            "customizable_price": "false",
        }
        
        req = urllib.request.Request(
            f"{GUMROAD_API}/products",
            data=urllib.parse.urlencode(data).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            result = json.loads(resp.read())
            results.append(result)
            product_url = result.get("product", {}).get("short_url", "unknown")
            print(f"✅ Created: {product['name']}")
            print(f"   URL: https://gumroad.com{product_url}")
        except Exception as e:
            print(f"❌ Failed: {product['name']} — {e}")
            results.append({"error": str(e)})
    
    return results

if __name__ == "__main__":
    token = input("Paste your Gumroad access token: ").strip()
    if token:
        setup_products(token)
    else:
        print("No token provided. Exiting.")
