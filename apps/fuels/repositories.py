from dataclasses import dataclass
from typing import Dict, List, Optional
from apps.fuels.loaders import Station


@dataclass
class FuelRepo:
    by_state: Dict[str, List[Station]]

    @staticmethod
    def build(stations: List[Station]) -> "FuelRepo":
        by_state: Dict[str, List[Station]] = {}
        for s in stations:
            st = (s.state or "").strip().upper()
            if not st:
                continue
            by_state.setdefault(st, []).append(s)

        # opcional: ordenar por precio para que cheapest sea O(1)
        for st in by_state:
            by_state[st].sort(key=lambda x: x.price_per_gallon)

        return FuelRepo(by_state=by_state)

    def cheapest_in_state(self, state: str) -> Optional[Station]:
        state = (state or "").strip().upper()
        lst = self.by_state.get(state)
        if not lst:
            return None
        return lst[0]
