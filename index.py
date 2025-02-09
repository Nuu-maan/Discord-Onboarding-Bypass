# onboarding_bypass (fixed)
import os
import json
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed 
from typing import List, Dict, Any, Optional

import tls_client
import colorama
from colorama import Fore, Style

from data.loggger import NovaLogger

colorama.init(autoreset=True)

BANNER = f"""
{Fore.CYAN}
                        █████▒██▓ ██▓     ██▓   ▓██   ██▓
                        ▓██   ▒▓██▒▓██▒    ▓██▒    ▒██  ██▒
                        ▒████ ░▒██▒▒██░    ▒██░     ▒██ ██░
                        ░▓█▒  ░░██░▒██░    ▒██░     ░ ▐██▓░
                        ░▒█░   ░██░░██████▒░██████▒ ░ ██▒▓░
                        ▒ ░   ░▓  ░ ▒░▓  ░░ ▒░▓  ░  ██▒▒▒ 
                        ░      ▒ ░░ ░ ▒  ░░ ░ ▒  ░▓██ ░▒░ 
                        ░ ░    ▒ ░  ░ ░     ░ ░   ▒ ▒ ░░  
                                ░      ░  ░    ░  ░░ ░     
                                                ░ ░     

                        {Fore.LIGHTCYAN_EX}https://discord.gg/api{Style.RESET_ALL}
"""

class ConfigurationManager:
    """Handles configuration loading with enhanced parsing"""
    def __init__(self):
        self.config = {}
        self.proxies = []
        self.tokens = []
        
    def load_config(self) -> None:
        """Load and validate configuration from files"""
        try:
            with open("input/config.json") as f:
                self.config = json.load(f)
            
            self.proxies = self._parse_proxies("input/proxies.txt")
            self.tokens = self._parse_tokens("input/tokens.txt")
            
            NovaLogger.event("Configuration loaded", 
                           tokens=len(self.tokens),
                           proxies=len(self.proxies),
                           threads=self.config.get("Threads"))
            
        except Exception as e:
            NovaLogger.fail("Config load error", error=str(e))
            raise

    def _parse_proxies(self, path: str) -> List[str]:
        """Parse proxies with various formats"""
        proxies = []
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        if not line.startswith("http"):
                            line = f"http://{line}"
                        proxies.append(line)
        return proxies

    def _parse_tokens(self, path: str) -> List[str]:
        """Extract tokens from multiple formats"""
        tokens = []
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        token = line.split(":")[-1]
                        tokens.append(token)
        return tokens


class DiscordSessionManager:
    """Manages TLS sessions with modern fingerprints"""
    def __init__(self, config: dict, proxies: List[str]):
        self.config = config
        self.proxies = proxies
        self.client_identifier = "chrome_133"
        
    def create_session(self) -> tls_client.Session:
        """Create new session with randomized parameters"""
        session = tls_client.Session(
            client_identifier=self.client_identifier,
            random_tls_extension_order=True
        )
        
        session.headers = self._modern_headers()
        
        if not self.config.get("Proxyless") and self.proxies:
            self._apply_proxy(session)
            
        return session
    
    def _apply_proxy(self, session: tls_client.Session) -> None:
        """Apply random proxy from list"""
        proxy = random.choice(self.proxies)
        session.proxies = {
            "http": proxy,
            "https": proxy
        }
        NovaLogger.trace("Proxy applied", proxy=proxy)

    def _modern_headers(self) -> dict:
        """Generate headers with 2025 Chrome 133 fingerprint"""
        return {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Google Chrome";v="133", "Chromium";v="133", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Asia/Calcutta',
            'x-super-properties': self._super_properties()
        }
    
    def _super_properties(self) -> str:
        """Generate modern super properties"""
        return "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMzLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjM0NTY3OCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="


class OnboardingHandler:
    """Handles Discord guild onboarding process"""
    def __init__(self, config: dict, proxies: List[str]):
        self.config = config
        self.session_manager = DiscordSessionManager(config, proxies)
        
    def execute(self, tokens: List[str], guild_id: str) -> None:
        """Execute onboarding bypass with thread pool"""
        NovaLogger.note("Starting mass onboarding", 
                      guild_id=guild_id, 
                      total_tokens=len(tokens))
        
        with ThreadPoolExecutor(max_workers=self.config["Threads"]) as executor:
            futures = {executor.submit(self.process_token, token, guild_id): token 
                      for token in tokens}
            
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    NovaLogger.fail("Thread error", error=str(e))

    def process_token(self, token: str, guild_id: str) -> None:
        """Process individual token through onboarding flow"""
        try:
            session = self.session_manager.create_session()
            session.headers["authorization"] = token
            
            onboarding_data = self._get_onboarding_data(session, guild_id)
            if onboarding_data:
                self._complete_onboarding(session, guild_id, onboarding_data)
                NovaLogger.win("Onboarding success", token=token[-15:])
            else:
                NovaLogger.note("No onboarding needed", token=token[-15:])
                
        except Exception as e:
            NovaLogger.fail("Processing failed", token=token[-15:], error=str(e))

    def _get_onboarding_data(self, session: tls_client.Session, guild_id: str) -> Optional[Dict[str, Any]]:
        """Fetch and parse onboarding data"""
        response = session.get(
            f"https://discord.com/api/v9/guilds/{guild_id}/onboarding"
        )
        
        if response.status_code != 200:
            raise Exception(f"Onboarding check failed ({response.status_code})")
            
        data = response.json()
        if not data.get("prompts"):
            return None
            
        return data

    def _complete_onboarding(self, session: tls_client.Session, guild_id: str, data: Dict[str, Any]) -> None:
        """Complete full onboarding process"""
        payload = self._prepare_payload(data)
        
        response = session.post(
            f"https://discord.com/api/v9/guilds/{guild_id}/onboarding-responses",
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"Onboarding failed ({response.status_code}): {response.text}")

    def _prepare_payload(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate valid onboarding payload"""
        now = int(datetime.now().timestamp())
        prompts = data.get("prompts", [])
        
        # Extract valid prompt and option IDs
        prompts_seen = {prompt["id"]: now for prompt in prompts}
        responses_seen = {
            option["id"]: now
            for prompt in prompts
            for option in prompt.get("options", [])
        }
        responses = [
            prompt["options"][-1]["id"]
            for prompt in prompts
            if prompt.get("options")
        ]
        
        return {
            "onboarding_responses": responses,
            "onboarding_prompts_seen": prompts_seen,
            "onboarding_responses_seen": responses_seen
        }


if __name__ == "__main__":
    print(BANNER)
    NovaLogger.config(debug=True)
    
    try:
        config_manager = ConfigurationManager()
        config_manager.load_config()
        
        if not config_manager.tokens:
            NovaLogger.fail("No valid tokens found in input file")
            exit(1)
            
        guild_id = input(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTMAGENTA_EX}{time.strftime('%H:%M:%S')}{Fore.LIGHTBLACK_EX}] {Fore.WHITE}[INFO] Guild ID: ")
        
        bypass = OnboardingHandler(config_manager.config, config_manager.proxies)
        bypass.execute(config_manager.tokens, guild_id)
        
    except KeyboardInterrupt:
        NovaLogger.alert("Process interrupted by user")
    except Exception as e:
        NovaLogger.fail("Critical failure", error=str(e))
    finally:
        NovaLogger.close()