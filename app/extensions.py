import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Check if rate limiting is enabled (default True, set RATELIMIT_ENABLED=false to disable)
_ratelimit_enabled = os.environ.get('RATELIMIT_ENABLED', 'true').lower() == 'true'

limiter = Limiter(
    key_func=get_remote_address,
    enabled=_ratelimit_enabled
)