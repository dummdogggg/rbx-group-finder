import os
import threading
import requests
import random
from dhooks import Webhook, Embed
import ctypes
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Set console title (Windows-specific)
ctypes.windll.kernel32.SetConsoleTitleW("Aleks Group Finder")

# Group finder function with enhanced logging
def groupfinder(hook, proxy):
    try:
        group_id = random.randint(1000000, 1150000)
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        logging.info(f"Checking group ID: {group_id}")
        
        # First request to check if group is owned
        response = requests.get(
            f"https://www.roblox.com/groups/group.aspx?gid={group_id}",
            proxies=proxies,
            timeout=30
        )
        
        if 'owned' not in response.text:
            # Second request to get group details
            api_response = requests.get(
                f"https://groups.roblox.com/v1/groups/{group_id}",
                proxies=proxies,
                timeout=30
            )
            
            if api_response.status_code != 429:
                data = api_response.json()
                
                if 'errors' not in data:
                    if not data.get('isLocked') and 'owner' in data:
                        if data.get('publicEntryAllowed') and data.get('owner') is None:
                            hit_url = f'https://www.roblox.com/groups/group.aspx?gid={group_id}'
                            
                            # Send hit message to Discord webhook
                            hook.send(f'🎯 **Hit:** {hit_url}')
                            logging.info(f"Hit: {group_id}")
                        else:
                            logging.info(f"No Entry Allowed: {group_id}")
                    else:
                        logging.info(f"Group Locked: {group_id}")
                else:
                    logging.warning(f"API returned errors for group ID {group_id}")
            else:
                logging.warning("Group API Rate Limited")
        else:
            logging.info(f"Group Already Owned: {group_id}")
            
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Network error with group ID {group_id}: {req_err}")
    except ValueError as val_err:
        logging.error(f"JSON decoding failed for group ID {group_id}: {val_err}")
    except Exception as e:
        logging.error(f"Unexpected error with group ID {group_id}: {e}")

def main():
    # Hardcoded Discord webhook URL
    hook_url = "https://discord.com/api/webhooks/1300547375340716073/9aoYaB6GhBZcUe2J9PggygQ-De3Lpb17PKEWhPn8qebSD_pAMSUWZWoH1I6bCZS86oW8"
    hook = Webhook(hook_url)
    
    # Send "Started looking" message to Discord webhook
    start_embed = Embed(
        description="🔍 **Started looking for Roblox groups...**",
        color=0x00ff00
    )
    hook.send(embed=start_embed)
    logging.info("Sent 'Started looking for Roblox groups...' message to Discord webhook.")
    
    # Hardcoded number of threads
    thread_count = 50
    logging.info(f"Starting with {thread_count} threads.")
    
    # Configure your SOCKS proxy details
    # Example: "socks5://username:password@host:port"
    # If no authentication is required, use "socks5://host:port"
    socks_proxy = "socks5://T8bG2grGMDGQP447oBjrt2aF:SidnvUVLHdQn2d6oRhV9KH4w@nl.socks.nordhold.net:1080"
    
    # Main execution loop
    while True:
        threads_list = []
        for _ in range(thread_count):
            thread = threading.Thread(target=groupfinder, args=(hook, socks_proxy))
            thread.start()
            threads_list.append(thread)
        
        # Wait for all threads to complete before starting new ones
        for thread in threads_list:
            thread.join()
        
        # Optional: Add a delay before the next iteration to prevent rapid looping
        time.sleep(1)

if __name__ == "__main__":
    main()
