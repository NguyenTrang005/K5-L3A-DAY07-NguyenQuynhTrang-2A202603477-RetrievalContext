"""Post-hoc cost estimate; does not change frozen traces or run new API calls."""
from datetime import datetime
from decimal import Decimal
import json

from .day6_retriever import ROOT


def main():
    # Official pricing checked 2026-11-14. All observed runs are Saturday UTC.
    rates = {"prompt_cache_hit_tokens": Decimal("0.003"),
             "prompt_cache_miss_tokens": Decimal("0.15"),
             "completion_tokens": Decimal("0.6")}
    runs = []
    for folder in sorted((ROOT / "results").glob("agent-*")):
        if not (folder / "config.json").exists() or not (folder / "traces.json").exists():
            continue
        config = json.loads((folder / "config.json").read_text(encoding="utf-8"))
        traces = json.loads((folder / "traces.json").read_text(encoding="utf-8"))
        if config["model"] != "deepseek-flash":
            raise ValueError("Unsupported model for this price snapshot")
        if datetime.fromisoformat(config["run_at_utc"]).weekday() < 5:
            raise ValueError("This snapshot assumes weekend off-peak; check time-specific rates")
        usage = {key: sum(t["usage"].get(key,0) for t in traces) for key in rates}
        for t in traces:
            u = t["usage"]
            if u.get("prompt_tokens",0) != u.get("prompt_cache_hit_tokens",0)+u.get("prompt_cache_miss_tokens",0):
                raise ValueError("Missing input cache breakdown")
        cost = sum(Decimal(usage[key])*rate for key,rate in rates.items())/Decimal(1000000)
        runs.append({"run": folder.name, "usage": usage, "total_tokens": sum(t["usage"]["total_tokens"] for t in traces),
                     "observed_response_cost_estimate_usd": float(cost),
                     "errors": sum(t["status"] == "error" for t in traces)})
    report = {"source": "https://api-docs.deepseek.com/quick_start/pricing/", "checked_on": "2026-11-14",
              "model": "deepseek-flash", "assumed_price_period": "off-peak: all recorded run timestamps are Saturday UTC",
              "usd_per_million_tokens": {k:float(v) for k,v in rates.items()},
              "formula": "(cache_hit*0.003 + cache_miss*0.15 + completion*0.6)/1e6",
              "runs": runs, "total_observed_estimate_usd": sum(r["observed_response_cost_estimate_usd"] for r in runs),
              "limitations": "Post-hoc estimate using official price snapshot and reported token usage, not an invoice. Excludes credits, taxes, rate changes, unobserved billed requests, and local hardware/electricity. Zero observed tokens for a connection failure is not proof of zero provider billing. No paid DeepSeek search/OCR services called; search_documents is a local tool."}
    (ROOT / "results/cost_estimate.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({r["run"]:r["observed_response_cost_estimate_usd"] for r in runs},indent=2))


if __name__ == "__main__":
    main()
