"""HIP3Radar Python SDK — wrap the public risk surveillance API."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional

import httpx

__version__ = "0.1.0"

DEFAULT_BASE = "https://hip3radar.xyz"


def safety_grade(risk_score: Optional[float]) -> dict:
    """Convert risk score (0-100, higher=worse) to safety rating + letter grade."""
    if risk_score is None:
        return {"rating": None, "grade": "—"}
    rs = float(risk_score)
    rating = max(0.0, min(100.0, 100.0 - rs))
    if rating >= 90: g = "AA"
    elif rating >= 80: g = "A"
    elif rating >= 70: g = "B+"
    elif rating >= 60: g = "B"
    elif rating >= 50: g = "C"
    elif rating >= 30: g = "D"
    else: g = "F"
    return {"rating": round(rating, 1), "grade": g}


@dataclass
class HIP3Radar:
    """Synchronous client for the HIP3Radar public API.

    Usage:
        from hip3radar import HIP3Radar
        client = HIP3Radar()                 # free public tier
        client = HIP3Radar(api_key="...")    # paid tier

        state = client.state()
        for m in state["top_risk"]:
            grade = safety_grade(m["risk_score"])
            print(m["name"], grade["grade"], grade["rating"])
    """
    api_key: Optional[str] = None
    base_url: str = DEFAULT_BASE
    timeout: float = 10.0
    _http: httpx.Client = field(init=False, repr=False)

    def __post_init__(self) -> None:
        headers = {"User-Agent": f"hip3radar-python/{__version__}"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        self._http = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=headers,
        )

    def __enter__(self): return self
    def __exit__(self, *exc): self.close()
    def close(self) -> None: self._http.close()

    def _get(self, path: str, **params) -> Any:
        params = {k: v for k, v in params.items() if v is not None}
        r = self._http.get(path, params=params)
        r.raise_for_status()
        return r.json()

    # ─── scoreboard ───
    def state(self) -> dict:
        """Top 25 highest-risk markets right now."""
        return self._get("/hip3radar/api/state")

    def all_markets(self) -> dict:
        """Full snapshot — every market across every dex."""
        return self._get("/hip3radar/api/all")

    def dex(self, dex: str) -> dict:
        """All markets on one dex (hl, xyz, vntl, flx, hyna, km, cash, para, abcd)."""
        return self._get(f"/hip3radar/api/dex/{dex}")

    def market(self, dex: str, coin: str) -> dict:
        """Single market detail."""
        return self._get(f"/hip3radar/api/market/{dex}/{coin}")

    def history(self, dex: str, coin: str, hours: int = 24) -> dict:
        """Per-market time series (max 168 hours)."""
        return self._get(f"/hip3radar/api/history/{dex}/{coin}", hours=hours)

    # ─── alerts ───
    def alerts(self, limit: int = 100, level: Optional[str] = None) -> dict:
        """Recent alerts. level ∈ {warning, critical} or None for both."""
        return self._get("/hip3radar/api/alerts", limit=limit, level=level)

    # ─── incidents ───
    def incidents(self) -> dict:
        """All documented HL manipulation events."""
        return self._get("/hip3radar/api/incidents")

    def incident(self, slug: str) -> dict:
        """Single incident with replay data."""
        return self._get(f"/hip3radar/api/incidents/{slug}")

    # ─── verification ───
    def verified_deployers(self) -> dict:
        """All verified deployers."""
        return self._get("/hip3radar/api/verified")

    def verification(self, slug: str) -> dict:
        """One deployer's verification status."""
        return self._get(f"/hip3radar/api/verification/{slug}")

    # ─── system ───
    def healthz(self) -> dict:
        """Liveness probe."""
        return self._get("/healthz")

    def status(self) -> dict:
        """Aggregate health for the status page."""
        return self._get("/api/status")


__all__ = ["HIP3Radar", "safety_grade", "__version__"]
