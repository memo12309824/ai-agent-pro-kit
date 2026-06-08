#!/usr/bin/env python3
"""Exa Neural Search Integration Setup for AI Agent Pro Kit"""

def setup_exa_client():
    """Configure Exa search client for your agent"""
    api_key = input("Enter your Exa API key (get at exa.ai): ").strip()
    if not api_key:
        print("⚠️  No API key provided. Using mock mode for testing.")
        return None
    
    print(f"✅ Exa client configured with key: {api_key[:8]}...")
    return {
        "api_key": api_key,
        "base_url": "https://api.exa.ai",
        "usage": {
            "search": "semantic search across web",
            "contents": "fetch page contents",
            "similar": "find similar pages"
        }
    }

def test_search(client):
    """Quick test of the search functionality"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {client['api_key']}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{client['base_url']}/search",
        json={"query": "AI agents autonomous", "num_results": 3},
        headers=headers
    )
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        print(f"✅ Search works! Found {len(results)} results")
        return True
    else:
        print(f"❌ Search API error: {response.status_code}")
        return False

if __name__ == "__main__":
    print("🔍 Exa Neural Search Integration")
    print("=" * 40)
    client = setup_exa_client()
    if client:
        test_search(client)
