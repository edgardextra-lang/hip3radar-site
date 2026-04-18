/**
 * HIP3Radar JS SDK — wrap the public risk surveillance API.
 * Works in browsers, Node 18+, Deno, Bun. ESM and CommonJS-friendly.
 *
 * @example
 *   import { HIP3Radar, safetyGrade } from "hip3radar";
 *   const client = new HIP3Radar();
 *   const state = await client.state();
 *   for (const m of state.top_risk) {
 *     const g = safetyGrade(m.risk_score);
 *     console.log(m.name, g.grade, g.rating);
 *   }
 */

export const VERSION = "0.1.0";
const DEFAULT_BASE = "https://hip3radar.xyz";

/**
 * Convert a risk score (0-100, higher = worse) to safety rating + letter grade.
 * @param {number|null|undefined} riskScore
 * @returns {{rating: number|null, grade: string}}
 */
export function safetyGrade(riskScore) {
  if (riskScore === null || riskScore === undefined) return { rating: null, grade: "—" };
  const rs = Number(riskScore);
  if (Number.isNaN(rs)) return { rating: null, grade: "—" };
  const rating = Math.max(0, Math.min(100, 100 - rs));
  let g;
  if (rating >= 90) g = "AA";
  else if (rating >= 80) g = "A";
  else if (rating >= 70) g = "B+";
  else if (rating >= 60) g = "B";
  else if (rating >= 50) g = "C";
  else if (rating >= 30) g = "D";
  else g = "F";
  return { rating: Math.round(rating * 10) / 10, grade: g };
}

export class HIP3RadarError extends Error {
  constructor(message, status, body) {
    super(message);
    this.name = "HIP3RadarError";
    this.status = status;
    this.body = body;
  }
}

export class HIP3Radar {
  /**
   * @param {object} [opts]
   * @param {string} [opts.apiKey] - Optional. Required for paid tiers.
   * @param {string} [opts.baseUrl="https://hip3radar.xyz"]
   * @param {number} [opts.timeoutMs=10000]
   * @param {typeof fetch} [opts.fetch] - Custom fetch impl (default: globalThis.fetch)
   */
  constructor(opts = {}) {
    this.apiKey = opts.apiKey || null;
    this.baseUrl = (opts.baseUrl || DEFAULT_BASE).replace(/\/+$/, "");
    this.timeoutMs = opts.timeoutMs ?? 10000;
    this.fetchImpl = opts.fetch || globalThis.fetch;
    if (!this.fetchImpl) {
      throw new Error("HIP3Radar: no fetch available. Pass `fetch` in opts on Node <18.");
    }
  }

  async _get(path, params) {
    const url = new URL(this.baseUrl + path);
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
      }
    }
    const headers = { "User-Agent": `hip3radar-js/${VERSION}` };
    if (this.apiKey) headers["Authorization"] = `Bearer ${this.apiKey}`;

    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), this.timeoutMs);
    let res;
    try {
      res = await this.fetchImpl(url.toString(), { headers, signal: ctrl.signal });
    } finally {
      clearTimeout(timer);
    }
    let body;
    try { body = await res.json(); } catch { body = null; }
    if (!res.ok) {
      throw new HIP3RadarError(
        `HIP3Radar ${res.status} on ${path}`,
        res.status,
        body,
      );
    }
    return body;
  }

  // ─── scoreboard ───
  state()                 { return this._get("/hip3radar/api/state"); }
  allMarkets()            { return this._get("/hip3radar/api/all"); }
  dex(dex)                { return this._get(`/hip3radar/api/dex/${encodeURIComponent(dex)}`); }
  market(dex, coin)       { return this._get(`/hip3radar/api/market/${encodeURIComponent(dex)}/${encodeURIComponent(coin)}`); }
  history(dex, coin, hours = 24) {
    return this._get(`/hip3radar/api/history/${encodeURIComponent(dex)}/${encodeURIComponent(coin)}`, { hours });
  }

  // ─── alerts ───
  alerts({ limit = 100, level } = {}) {
    return this._get("/hip3radar/api/alerts", { limit, level });
  }

  // ─── incidents ───
  incidents()             { return this._get("/hip3radar/api/incidents"); }
  incident(slug)          { return this._get(`/hip3radar/api/incidents/${encodeURIComponent(slug)}`); }

  // ─── verification ───
  verifiedDeployers()     { return this._get("/hip3radar/api/verified"); }
  verification(slug)      { return this._get(`/hip3radar/api/verification/${encodeURIComponent(slug)}`); }

  // ─── system ───
  healthz()               { return this._get("/healthz"); }
  status()                { return this._get("/api/status"); }
}

// CommonJS compat
if (typeof module !== "undefined" && module.exports) {
  module.exports = { HIP3Radar, HIP3RadarError, safetyGrade, VERSION };
}
