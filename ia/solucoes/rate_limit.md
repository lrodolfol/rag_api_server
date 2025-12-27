# Rate limit for `/api/v1/askme-chat-online`

1. **Flask-Limiter** using a local cache or Redis to keep per-IP or per-API-key counters; apply a `@limiter.limit("10/minute")` decorator on the endpoint and ensure the storage backend is shared when running multiple instances.
2. **Token bucket per session**: each submission consumes a token and an async job refills the bucket on a fixed cadence; associate buckets with IP + user-agent to avoid abuse.
3. **API key / JWT-aware control**: use `g.user_code` or another token-derived identifier to cap the request volume within a window, storing counters in Redis or a lightweight in-memory table.
4. **Sliding window rate limiting** with shared cache storage (e.g., Redis sorted set) to allow controlled bursts, counting how many requests fall within the window and rejecting when the limit is exceeded.
5. **Lightweight circuit breaker**: monitor failures and volume to slow down the endpoint under heavy load, including a `Retry-After` header so clients respect the policy.

Each idea should include monitoring (hits vs rejects) and user-friendly error messaging (HTTP 429 + JSON explaining when to retry).

## Implemented approach
- Enabled `Flask-Limiter` with `key_func=get_remote_address` and `storage_uri="memory://"` to keep per-IP counters.
- Decorated `/api/v1/askme-chat-online` with `@limiter.limit("10/minute")`, so a 429 response is returned when an IP exceeds the window and the standard rate-limit headers are exposed for the front end.
