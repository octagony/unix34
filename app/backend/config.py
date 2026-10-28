from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
	reddit_subreddit_url: str
	reddrix_mode: str = "standard"
	reddrix_stealth: str = "adaptive"
	reddrix_max_posts: int = 100
	reddrix_sort: str = "new"
	reddrix_include_comments: bool = False
	supabase_url: str
	supabase_anon_key: str
	supabase_service_role_key: str
	app_env: str = "development"
	debug: bool = True
	log_level: str = "INFO"
	backend_port: int = 8000
	sync_interval_minutes: int = 15

	@property
	def subreddit_urls(self) -> List[str]:
			return [url.strip() for url in self.reddit_subreddit_url.split(",") if url.strip()]

	model_config = {
			"env_file": ".env",
			"env_file_encoding": "utf-8",
			"extra": "ignore"
	}

settings = Settings()