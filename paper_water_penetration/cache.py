from collections import defaultdict
from typing import Any, Iterable, List


class Cache:
    def __init__(self) -> None:
        self._cache = defaultdict(list)

    def __del__(self) -> None:
        del self._cache

    def __setitem__(self, name: str, value: List[Any]) -> None:
        """
        Create new entry in cache dict.
        """
        self._cache[name] = value

    def __getitem__(self, name: str) -> List[Any]:
        """
        Return cached image list from cache dict by name.
        """
        return self._cache[name]

    def __delitem__(self, name: str) -> None:
        """remove cached list from cache"""

        if name in self._cache:
            del self._cache[name]

    def __iter__(self) -> Iterable:
        """Iterate all cache entries"""
        return iter(self._cache)
