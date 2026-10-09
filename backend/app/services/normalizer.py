from urllib.parse import urlparse, unquote
import re

def normalize_url(raw_url: str) -> dict:
    changes = []
    url = raw_url.strip()

    # Prepend scheme if missing
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', url):
        url = 'http://' + url
        changes.append("Added default scheme 'http://'")

    try:
        parsed = urlparse(url)
    except Exception:
        # Invalid parsing
        return {
            "original_url": raw_url,
            "normalized_url": raw_url,
            "normalization_changes": ["Failed to parse URL"]
        }

    # Normalize hostname to lowercase
    normalized_hostname = (parsed.hostname or "").lower()
    if parsed.hostname and parsed.hostname != normalized_hostname:
        changes.append("Lowercased hostname")

    try:
        port_val = parsed.port
        port_str = f":{port_val}" if port_val else ""
        if (parsed.scheme == 'http' and port_val == 80) or \
           (parsed.scheme == 'https' and port_val == 443):
            port_str = ""
            changes.append("Removed default port")
    except ValueError:
        # Invalid port like a string instead of int
        port_str = ""
        changes.append("Removed invalid port string")

    # Reconstruct
    normalized_url = f"{parsed.scheme}://"
    
    if parsed.username:
        normalized_url += parsed.username
        if parsed.password:
            normalized_url += f":{parsed.password}"
        normalized_url += "@"
        
    normalized_url += normalized_hostname + port_str

    path = parsed.path
    if not path:
        path = "/"
        changes.append("Added trailing slash to empty path")
    normalized_url += path

    if parsed.query:
        normalized_url += f"?{parsed.query}"
    if parsed.fragment:
        normalized_url += f"#{parsed.fragment}"

    return {
        "original_url": raw_url,
        "normalized_url": normalized_url,
        "normalization_changes": changes,
        "parsed": parsed,
        "hostname": normalized_hostname
    }
