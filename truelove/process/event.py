from typing import List, Dict, Any

class EventManager:
    def __init__(self):
        self.listeners:Dict[str, List[Any]] = {}

    def subscribe(self, event_name: str, listener):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    async def emit(self, event_name: str, *args, **kwargs):
            for listener in self.listeners.get(event_name, []):
                result = await listener(*args, **kwargs)
                if result is not None:
                    args, kwargs = result
            return args, kwargs


def tl_event(event_name):
    def decorator(func):
        tl_event_mgr.subscribe(event_name, func)
        return func
    return decorator

tl_event_mgr = EventManager()