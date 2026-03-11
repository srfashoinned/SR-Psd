"""
Automated sync script - runs every 60 seconds
"""

import time
import schedule
import logging
from datetime import datetime
from export_items import export_inventory
from sync_to_github import GitHubSync

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sync.log'),
        logging.StreamHandler()
    ]
)

def sync_job():
    """Main sync job"""
    logging.info("Starting sync job...")
    
    # Export inventory
    if export_inventory():
        logging.info("✅ Inventory exported successfully")
        
        # Sync to GitHub
        sync = GitHubSync()
        if sync.push_to_github():
            logging.info("✅ GitHub sync completed")
        else:
            logging.error("❌ GitHub sync failed")
    else:
        logging.error("❌ Inventory export failed")

def main():
    """Main automation function"""
    logging.info("🚀 SR Fashion Auto-Sync Started")
    logging.info(f"⏰ Sync interval: 60 seconds")
    
    # Run immediately on start
    sync_job()
    
    # Schedule every 60 seconds
    schedule.every(60).seconds.do(sync_job)
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("👋 Sync stopped by user")
    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")