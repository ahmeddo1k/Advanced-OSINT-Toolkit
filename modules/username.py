import requests
from typing import Dict, List, Optional
from .utils import Logger, APIManager
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor, as_completed

console = Console()
logger = Logger.setup_logger(__name__)
api_manager = APIManager()

# قائمة المنصات الشائعة مع روابط التحقق
PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}",
    "Telegram": "https://t.me/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Twitch": "https://www.twitch.tv/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Keybase": "https://keybase.io/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "VK": "https://vk.com/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "About.me": "https://about.me/{}",
    "Imgur": "https://imgur.com/user/{}",
    "BitBucket": "https://bitbucket.org/{}/",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Lobsters": "https://lobste.rs/u/{}",
    "Medium": "https://medium.com/@{}",
    "Mastodon.social": "https://mastodon.social/@{}"
}

class UsernameChecker:
    """فحص وجود اسم المستخدم عبر منصات متعددة"""
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def check_platform(self, platform: str, url: str) -> Optional[Dict]:
        """فحص منصة واحدة"""
        try:
            api_manager.rate_limit()
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            
            # معالجة خاصة لبعض المنصات
            if platform == "Twitter" and response.status_code == 200:
                # تويتر يعيد 200 حتى لو الصفحة غير موجودة أحياناً
                if "This account doesn’t exist" in response.text:
                    return None
            elif platform == "Instagram" and response.status_code == 200:
                if "Page Not Found" in response.text:
                    return None
            
            if response.status_code == 200:
                return {
                    "platform": platform,
                    "url": url,
                    "status": "Found"
                }
            return None
        except Exception as e:
            logger.debug(f"Error checking {platform}: {e}")
            return None
    
    def check_all(self, username: str, max_workers: int = 10) -> List[Dict]:
        """فحص جميع المنصات بالتوازي"""
        found = []
        urls = {platform: url.format(username) for platform, url in PLATFORMS.items()}
        
        console.print(f"[yellow]🔎 Checking {len(PLATFORMS)} platforms for '{username}'...[/yellow]")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_platform = {
                executor.submit(self.check_platform, platform, url): platform
                for platform, url in urls.items()
            }
            
            for future in as_completed(future_to_platform):
                result = future.result()
                if result:
                    found.append(result)
                    console.print(f"[green]✅ Found on {result['platform']}: {result['url']}[/green]")
        
        return found

def username_lookup(username: str) -> dict:
    """دالة البحث الرئيسية عن اسم المستخدم"""
    checker = UsernameChecker()
    results = checker.check_all(username)
    
    return {
        "username": username,
        "platforms_found": len(results),
        "profiles": results
    }
