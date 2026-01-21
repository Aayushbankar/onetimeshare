import os
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

logger = logging.getLogger(__name__)

# Check if rate limiting is enabled (default True, set RATELIMIT_ENABLED=false to disable)
_ratelimit_enabled = os.environ.get('RATELIMIT_ENABLED', 'true').lower() == 'true'

def _on_breach(request_limit):
    """Callback when rate limit is breached - just log it."""
    logger.warning(f"Rate limit breached: {request_limit}")

limiter = Limiter(
    key_func=get_remote_address,
    enabled=_ratelimit_enabled,
    # Use memory storage as fallback when Redis is unavailable
    storage_uri="memory://",
    # Strategy for limiting
    strategy="fixed-window",
)