import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ProxyConfig:
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"

    def to_dict(self) -> Dict:
        """Convert proxy details to dict format for requests"""
        proxy_url = f"{self.protocol}://"
        if self.username and self.password:
            proxy_url += f"{self.username}:{self.password}@"
        proxy_url += f"{self.host}:{self.port}"
        
        return {"http": proxy_url, "https": proxy_url}

class ProxyManager:
    """Manage rotating proxies for bot detection bypass"""
    
    def __init__(self):
        self.proxies: List[ProxyConfig] = []
        self.current_proxy_index = 0
        self.failed_proxies = set()
    
    def add_proxy(self, host: str, port: int, username: str = None, password: str = None, protocol: str = "http"):
        """Add a proxy to the rotation"""
        proxy = ProxyConfig(host, port, username, password, protocol)
        self.proxies.append(proxy)
    
    def get_free_proxies(self) -> List[ProxyConfig]:
        """Fetch free proxies from public sources (use cautiously)"""
        try:
            response = requests.get("https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
            proxy_list = response.text.strip().split('\n')
            
            proxies = []
            for proxy in proxy_list[:10]:  # Limit to 10 proxies
                if ':' in proxy:
                    host, port = proxy.split(':')
                    proxies.append(ProxyConfig(host, int(port)))
            
            return proxies
        except Exception as e:
            print(f"Error fetching free proxies: {e}")
            return []
    
    def test_proxy(self, proxy: ProxyConfig, timeout: int = 10) -> bool:
        """Test if a proxy is working"""
        try:
            response = requests.get("http://httpbin.org/ip", proxies=proxy.to_dict(), timeout=timeout)
            return response.status_code == 200
        except Exception:
            return False

    def test_proxies_parallel(self) -> Dict[ProxyConfig, bool]:
        """Test multiple proxies in parallel and return working ones"""
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_proxy = {executor.submit(self.test_proxy, proxy): proxy for proxy in self.proxies}
            
            working_proxies = {}
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    if future.result():
                        working_proxies[proxy] = True
                except Exception as e:
                    working_proxies[proxy] = False
                    print(f"Error testing proxy {proxy.host}:{proxy.port} -> {e}")

        return working_proxies

    def get_working_proxy(self) -> Optional[ProxyConfig]:
        """Get a working proxy from the list"""
        if not self.proxies:
            return None
        
        for i in range(len(self.proxies)):
            proxy_index = (self.current_proxy_index + i) % len(self.proxies)
            proxy = self.proxies[proxy_index]
            
            if proxy_index in self.failed_proxies:
                continue
            
            if self.test_proxy(proxy):
                self.current_proxy_index = proxy_index
                return proxy
            else:
                self.failed_proxies.add(proxy_index)
        
        return None
    
    def rotate_proxy(self) -> Optional[ProxyConfig]:
        """Rotate to the next working proxy"""
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return self.get_working_proxy()