"""Deterministic context selection. Inputs contain no gold or answer labels."""
from collections import defaultdict


class ContextBuilder:
    def __init__(self, chunks):
        self.pages = defaultdict(list)
        for chunk in chunks:
            self.pages[(chunk["source_id"], chunk["page"])].append(chunk)
        self.positions = {}
        for key, page in self.pages.items():
            page.sort(key=lambda c: (c["metadata"]["char_start"], c["id"]))
            for index, chunk in enumerate(page):
                if chunk["id"] in self.positions:
                    raise ValueError("Duplicate corpus chunk ID")
                self.positions[chunk["id"]] = (key, index)

    def build(self, seeds, *, budget=6000, neighbors=False, filters=None):
        if type(budget) is not int or budget < 1:
            raise ValueError("Require positive integer character budget")
        candidates, seen = [], set()

        def add(chunk, reason, seed_id):
            if chunk["id"] in seen:
                return
            if any(chunk["metadata"].get(k) != v for k, v in (filters or {}).items()):
                return
            seen.add(chunk["id"])
            candidates.append({"chunk": chunk, "reason": reason, "seed_id": seed_id})

        for seed in seeds:
            add(seed, "retrieved", seed["id"])
        if neighbors:
            for seed in seeds:
                key, index = self.positions[seed["id"]]
                page = self.pages[key]
                if index > 0 and page[index - 1]["metadata"]["char_end"] == seed["metadata"]["char_start"]:
                    add(page[index - 1], "previous", seed["id"])
                if index + 1 < len(page) and seed["metadata"]["char_end"] == page[index + 1]["metadata"]["char_start"]:
                    add(page[index + 1], "next", seed["id"])
        blocks, selected, decisions = [], [], []
        for candidate in candidates:
            c = candidate["chunk"]
            block = f"[{c['id']} | {c['source']} | page {c['page']}]\n{c['text']}"
            fits = len("\n\n".join(blocks + [block])) <= budget
            decisions.append({"id": c["id"], "reason": candidate["reason"],
                              "seed_id": candidate["seed_id"], "selected": fits,
                              "skip_reason": None if fits else "budget"})
            if fits:
                blocks.append(block)
                selected.append(c)
        context = "\n\n".join(blocks)
        return {"context": context, "context_chars": len(context),
                "context_ids": [c["id"] for c in selected], "selected_chunks": selected,
                "candidate_count": len(candidates), "decisions": decisions}
