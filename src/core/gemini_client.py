"""
Google Gemini API Client - High-Performance AI Integration
"""

import requests
import aiohttp
from core.config import config
from aiohttp import ClientTimeout


class GeminiClient:
    """Fast and reliable Google Gemini API client"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-2.0-flash"

    def generate_content(self, prompt: str, max_tokens: int = 800) -> str:
        """Generate content using Gemini API (synchronous)"""
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"

        headers = {"Content-Type": "application/json"}

        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": config.OPENAI_TEMPERATURE,
            },
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    content = result["candidates"][0]["content"]["parts"][0]["text"]
                    return content.strip()
                else:
                    return "No response generated"
            else:
                raise Exception(f"Gemini API Error {response.status_code}: {response.text}")

        except Exception as e:
            raise Exception(f"Gemini API call failed: {str(e)}")

    async def generate_content_async(self, prompt: str, max_tokens: int = 800) -> str:
        """Generate content using Gemini API (asynchronous)"""
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"

        headers = {"Content-Type": "application/json"}

        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": config.OPENAI_TEMPERATURE,
            },
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data, timeout=ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        result = await response.json()
                        if "candidates" in result and len(result["candidates"]) > 0:
                            content = result["candidates"][0]["content"]["parts"][0]["text"]
                            return content.strip()
                        else:
                            return "No response generated"
                    else:
                        error_text = await response.text()
                        raise Exception(f"Gemini API Error {response.status}: {error_text}")

        except Exception as e:
            raise Exception(f"Gemini API async call failed: {str(e)}")


# Global Gemini client instance
gemini_client = GeminiClient()
