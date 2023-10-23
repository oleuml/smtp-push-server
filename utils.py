def parse_ntfy_url(hostname: str, topic: str):
  # Remove all trailing slashes from hostname:
  while (len(hostname) > 1 and hostname[-1] == '/'):
    hostname = hostname[:-1]

  return hostname + "/" + topic