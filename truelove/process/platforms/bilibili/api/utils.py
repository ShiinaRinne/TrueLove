
def get_params(mid: int, web_location: int = 1550101, platform: str = "web", **kwargs) -> dict:
    base = {
        "mid": mid,
        "web_location": web_location,
        "platform": platform,
    }
    base.update(kwargs.get("params", {}))
    
    return base
