__all__ = ['get_env']  # Only get_env will be imported when using from my_module import *

def parse_token():
    file = open(".env", "r")
    tokens = {}             # Dictionary to store both tokens
    for line in file:
        if line.startswith("BOT_TOKEN"):
            tokens['BOT_TOKEN'] = parse_env(line)
        elif line.startswith("RIOT_TOKEN"):
            tokens['RIOT_TOKEN'] = parse_env(line)
    file.close()
    # Check if both tokens are found
    if 'BOT_TOKEN' in tokens and 'RIOT_TOKEN' in tokens:
        return (tokens)
    else:
        print("Error: One or both tokens are missing.")
        return (-1)

def parse_env(token_line):
    parts = token_line.split('=', 1)
    if len(parts) != 2:
        return (-1)  

    token_with_quotes = parts[1].strip()
    if token_with_quotes.startswith('"') and token_with_quotes.endswith('"'):
        return token_with_quotes[1:-1]
    else:
        return (token_with_quotes)

def get_env():
    token = parse_token()
    if (token):
        return (token)
    else:
        return (-1)