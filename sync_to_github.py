"""
Sync JSON file to GitHub repository
"""

import base64
import json
import requests
from datetime import datetime
import config

class GitHubSync:
    def __init__(self):
        self.token = config.GITHUB['token']
        self.repo = config.GITHUB['repository']
        self.branch = config.GITHUB['branch']
        self.file_path = config.GITHUB['file_path']
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = f'https://api.github.com/repos/{self.repo}'
    
    def get_file_sha(self):
        """Get SHA of existing file if it exists"""
        url = f'{self.base_url}/contents/{self.file_path}'
        params = {'ref': self.branch}
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()['sha']
        return None
    
    def read_json_file(self):
        """Read local JSON file"""
        try:
            with open(config.JSON_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading JSON file: {e}")
            return None
    
    def push_to_github(self):
        """Push file to GitHub"""
        content = self.read_json_file()
        if not content:
            return False
        
        # Encode content
        encoded_content = base64.b64encode(content.encode()).decode()
        
        # Get existing file SHA
        sha = self.get_file_sha()
        
        # Prepare commit data
        data = {
            'message': f'Update inventory - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            'content': encoded_content,
            'branch': self.branch
        }
        
        if sha:
            data['sha'] = sha
        
        # Push to GitHub
        url = f'{self.base_url}/contents/{self.file_path}'
        response = requests.put(url, headers=self.headers, json=data)
        
        if response.status_code in [200, 201]:
            print(f"✅ Successfully synced to GitHub")
            print(f"📱 Live at: {config.WEBSITE_URL}")
            return True
        else:
            print(f"❌ GitHub sync failed: {response.status_code}")
            print(response.json())
            return False

if __name__ == "__main__":
    sync = GitHubSync()
    sync.push_to_github()