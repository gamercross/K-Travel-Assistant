# src/kakao_client.py
import requests

class KakaoClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    
    def search_restaurants(self, city, query="맛집", limit=5):
        """
        city: "제주" 형식
        반환: [{name, address, category, url, x, y}, ...]
        """
        headers = {
            "Authorization": f"KakaoAK {self.api_key}"
        }
        
        params = {
            "query": f"{city} {query}",
            "size": limit,
            "sort": "accuracy"
        }
        
        try:
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 401:
                return None, {"step": "place_search", "type": "AUTH_ERROR", "message": "HTTP 401"}
            if response.status_code == 403:
                return None, {"step": "place_search", "type": "AUTH_ERROR", "message": "HTTP 403"}
            
            response.raise_for_status()
            data = response.json()
            
            if not data.get("documents"):
                return [], {"step": "place_search", "type": "EMPTY_RESULT", "message": f"0 results for {city}"}
            
            restaurants = []
            for doc in data["documents"]:
                restaurants.append({
                    "name": doc["place_name"],
                    "address": doc["address_name"],
                    "category": doc.get("category_name", ""),
                    "url": doc.get("place_url", ""),
                    "x": float(doc["x"]),
                    "y": float(doc["y"])
                })
            
            return restaurants, None
        
        except requests.exceptions.RequestException as e:
            return None, {"step": "place_search", "type": "NETWORK_ERROR", "message": str(e)}