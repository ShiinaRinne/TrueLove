import yaml
from typing import List
from pathlib import Path

class Config:
    def __init__(self):
        with open('./config.yml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self._init_config()
        
    def _init_config(self):
        self.save_dir = self.config['save_dir']
        self.cookie = self.config['cookie']
        self.proxies: List[str] = self.config['proxies'] if self.config['proxies'] else []
        self.log_level = self.config['log_level']
        
        self.root_dir = Path(__file__).parent.parent.parent.resolve()

        self.download_settings = self.config['download-settings']
        self.cover = self.download_settings['cover']
        self.subtitle = self.download_settings['subtitle']
        self.dm = self.download_settings['dm']
        
config = Config()