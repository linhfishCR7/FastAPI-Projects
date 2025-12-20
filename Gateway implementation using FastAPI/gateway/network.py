from typing import Dict, Optional
from fastapi import Request
from fastapi.responses import Response
import httpx

from conf import settings
from auth import AuthHandler
from models import _auth_skip

# Configuration: map path prefixes to upstream base URLs
# Add or change mappings here to point to the correct services/hosts.
ROUTE_CONFIG: Dict[str, str] = {
	"order": settings.ORDER_URL,
	"product": settings.PRODUCT_URL,
	"auth": settings.AUTH_URL
}


def find_upstream(path: str) -> Optional[str]:
	"""Find upstream base URL for the incoming request path.

	Chooses the longest matching prefix from ROUTE_CONFIG.
	Returns the base URL (e.g. http://127.0.0.1:8001) or None.
	"""
	# Longest-prefix match so nested prefixes work properly.
	matches = [(p, u) for p, u in ROUTE_CONFIG.items() if path.startswith(p)]
	if not matches:
		return None
	# choose longest prefix
	matches.sort(key=lambda item: len(item[0]), reverse=True)
	return matches[0][1]


async def proxy_request(full_path: str, request: Request) -> Response:
	"""Proxy an incoming FastAPI request to the configured upstream.

	Preserves method, query params, headers (filtered), and body. Returns
	a FastAPI Response with upstream status, headers, and content.
	"""
	service_name = full_path.split("/")[0]
	upstream = find_upstream(service_name)
	
	if not upstream:
		return Response(content=b"Not Found", status_code=404)
	

	# Build upstream URL (include the full path and query params handled separately)
	upstream_url = f"{upstream}{full_path}"

	# Prepare headers (remove hop-by-hop headers that should not be forwarded)
	headers = dict(request.headers)
	token =headers.get('authorization', None)
	
	
    ## check full part is part of _auth_skip
	if full_path not in _auth_skip:
		if token is None:
			return Response(content=b"Authorization Required", status_code=401)
		auth_user = AuthHandler()
		user_auth = await auth_user.auth_wrapper(token= token)
		headers["X-User-Name"] = user_auth.username

    
	for h in ["host", "content-length", "transfer-encoding", "connection"]:
		headers.pop(h, None)

	body = await request.body()

	async with httpx.AsyncClient(follow_redirects=False, timeout=10.0) as client:
		try:
			resp = await client.request(
				request.method,
				upstream_url,
				params=request.query_params,
				content=body,
				headers=headers,
			)
		except httpx.RequestError as exc:
			return Response(content=f"Upstream request failed: {exc}".encode(), status_code=502)

	# Filter response headers: remove hop-by-hop and any headers FastAPI will set
	response_headers = dict(resp.headers)
	for h in ["transfer-encoding", "connection", "content-encoding"]:
		response_headers.pop(h, None)

	return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)

