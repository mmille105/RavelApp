"""
Ravel Route Optimizer
─────────────────────
Logic layers:

  1. Geographic corridor filter
     Candidate cities must lie within an ellipse defined by origin/destination
     as foci. Detour tolerance scales with the traveller's top trait.

  2. Profile scoring
     Dot product of traveller score vector × city trait vector, normalised 0–5.

  3. Event bonus
     Travel month × event month × matching trait → +1.5 pts.

  4. Budget short-circuit
     Budget score ≥ 4.0 AND top trait IS Budget → recommend direct route.

  5. Travel-time feasibility
     Estimate transit hours per leg. Flag if there is not enough time to
     meaningfully explore each stop.

  6. Day-by-day itinerary
     Allocate exploration days to stops, build a narrative day plan.

  7. Trip cost estimate
     Sum daily_budget_eur per stop × allocated days.
"""

import math
from cities import CITIES, CITY_TAGS
from scoring import CATEGORIES

# ── Tuning constants ────────────────────────────────────────────────────────
EVENT_BONUS      = 1.5
BUDGET_THRESHOLD = 4.0

DETOUR_FACTORS = {
    "Budget":     1.20,
    "Relaxation": 1.45,
    "Culture":    1.65,
    "Food":       1.65,
    "Shopping":   1.55,
    "Adventure":  2.10,
}

MONTH_NAMES = {
    1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
    7:"July",8:"August",9:"September",10:"October",11:"November",12:"December",
}

TRANSPORT_ADVICE = {
    "Budget":     "🚌  Book FlixBus or Ouibus well in advance — you can often get cross-border tickets for under €20. Check Omio for the cheapest combination of bus and budget train.",
    "Adventure":  "🚗  Hire a car and give yourself permission to stop whenever the road looks interesting. The detours are usually the best part.",
    "Culture":    "🚆  Trains are the right call — they drop you into city centres, leave your hands free for reading, and the countryside between stops is often worth watching.",
    "Relaxation": "🚆  A scenic Interrail pass lets you travel without booking pressure. Hop on, find a window seat, and let the scenery do the work.",
    "Food":       "🚆  Trains mean you can pick up market food at each stop and eat on board. Half the culinary experience of a trip is in the stations.",
    "Shopping":   "🚆  No baggage fees, generous luggage allowance, and city-centre arrivals. Trains are made for people who buy things.",
}

# ── Known transit times (hours, point-to-point including transfers) ─────────
_TRANSIT_HOURS = {
    frozenset(["Prague",    "Vienna"]):      4.0,
    frozenset(["Prague",    "Berlin"]):      4.5,
    frozenset(["Prague",    "Krakow"]):      7.0,
    frozenset(["Prague",    "Budapest"]):    7.0,
    frozenset(["Prague",    "Frankfurt"]):   5.5,
    frozenset(["Vienna",    "Budapest"]):    2.5,
    frozenset(["Vienna",    "Munich"]):      4.0,
    frozenset(["Vienna",    "Zurich"]):      9.0,
    frozenset(["Vienna",    "Ljubljana"]):   6.0,
    frozenset(["Budapest",  "Ljubljana"]):   6.5,
    frozenset(["Budapest",  "Krakow"]):      8.0,
    frozenset(["Berlin",    "Amsterdam"]):   6.0,
    frozenset(["Berlin",    "Frankfurt"]):   3.5,
    frozenset(["Berlin",    "Copenhagen"]):  5.5,
    frozenset(["Berlin",    "Warsaw"]):      5.5,
    frozenset(["Amsterdam", "Brussels"]):    2.0,
    frozenset(["Amsterdam", "Paris"]):       3.5,
    frozenset(["Amsterdam", "London"]):      4.0,
    frozenset(["Brussels",  "Paris"]):       1.5,
    frozenset(["Brussels",  "London"]):      2.5,
    frozenset(["Paris",     "London"]):      2.5,
    frozenset(["Paris",     "Lyon"]):        2.0,
    frozenset(["Paris",     "Barcelona"]):   6.5,
    frozenset(["Paris",     "Madrid"]):      9.5,
    frozenset(["Paris",     "Frankfurt"]):   3.5,
    frozenset(["Paris",     "Nice"]):        5.5,
    frozenset(["Paris",     "Milan"]):       7.0,
    frozenset(["Lyon",      "Barcelona"]):   5.0,
    frozenset(["Lyon",      "Nice"]):        3.0,
    frozenset(["Lyon",      "Milan"]):       5.5,
    frozenset(["Barcelona", "Madrid"]):      2.5,
    frozenset(["Barcelona", "Bilbao"]):      5.5,
    frozenset(["Madrid",    "Seville"]):     2.5,
    frozenset(["Madrid",    "Lisbon"]):      9.0,
    frozenset(["Seville",   "Lisbon"]):      3.5,
    frozenset(["Seville",   "Porto"]):       5.0,
    frozenset(["Lisbon",    "Porto"]):       3.0,
    frozenset(["Frankfurt", "Munich"]):      3.5,
    frozenset(["Frankfurt", "Amsterdam"]):   4.0,
    frozenset(["Frankfurt", "Zurich"]):      3.5,
    frozenset(["Munich",    "Zurich"]):      3.5,
    frozenset(["Munich",    "Milan"]):       6.0,
    frozenset(["Zurich",    "Milan"]):       3.5,
    frozenset(["Milan",     "Florence"]):    1.75,
    frozenset(["Milan",     "Rome"]):        3.0,
    frozenset(["Florence",  "Rome"]):        1.5,
    frozenset(["Rome",      "Athens"]):      2.0,  # fly
    frozenset(["Athens",    "Dubrovnik"]):   3.0,  # fly/ferry
    frozenset(["Copenhagen","Stockholm"]):   5.0,
    frozenset(["Stockholm", "Tallinn"]):     2.5,  # ferry
    frozenset(["London",    "Edinburgh"]):   4.5,
    frozenset(["London",    "Dublin"]):      2.5,  # fly or ferry
    frozenset(["Edinburgh", "Dublin"]):      2.0,  # fly
    frozenset(["Krakow",    "Tallinn"]):     9.0,
    frozenset(["Ljubljana", "Venice"]):      2.0,
    frozenset(["Bruges",    "Brussels"]):    1.0,
    frozenset(["Bruges",    "Amsterdam"]):   2.5,
    frozenset(["Brussels",  "Frankfurt"]):   3.0,
}

def _transit_hours(a: str, b: str) -> float:
    """Return estimated transit hours between two cities."""
    key = frozenset([a, b])
    if key in _TRANSIT_HOURS:
        return _TRANSIT_HOURS[key]
    # Fall back to distance-based estimate
    dist = _haversine(CITIES[a]["lat"], CITIES[a]["lon"], CITIES[b]["lat"], CITIES[b]["lon"])
    if dist < 300:  return 3.0
    if dist < 600:  return 5.0
    if dist < 1000: return 7.0
    if dist < 1500: return 10.0
    return 13.0  # long-haul, likely a flight


def _transit_mode(a: str, b: str) -> str:
    dist = _haversine(CITIES[a]["lat"], CITIES[a]["lon"], CITIES[b]["lat"], CITIES[b]["lon"])
    hrs  = _transit_hours(a, b)
    if dist > 1200 or hrs <= 3.5:
        return "✈ Fly"
    elif hrs <= 5:
        return "🚆 Train"
    elif hrs <= 8:
        return "🚆 Train or ✈ Fly"
    else:
        return "✈ Fly (recommended)"


# ── Haversine distance ───────────────────────────────────────────────────────
def _haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a  = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def _city_dist(a: str, b: str) -> float:
    ca, cb = CITIES[a], CITIES[b]
    return _haversine(ca["lat"], ca["lon"], cb["lat"], cb["lon"])


# ── Corridor filter ──────────────────────────────────────────────────────────
def _is_feasible(origin, dest, candidate, detour_factor) -> bool:
    direct = _city_dist(origin, dest)
    via    = _city_dist(origin, candidate) + _city_dist(candidate, dest)
    return via <= detour_factor * direct


# ── City scoring ─────────────────────────────────────────────────────────────
def _score_city(city_name, traveler_scores, travel_month):
    city   = CITIES[city_name]
    traits = city["traits"]
    raw    = sum(traveler_scores.get(t, 3) * traits.get(t, 3) for t in CATEGORIES)
    score  = (raw / (5 * len(CATEGORIES))) * 5

    matching_events = []
    if travel_month:
        top2 = sorted(traveler_scores, key=traveler_scores.get, reverse=True)[:2]
        for ev in city.get("events", []):
            if travel_month in ev["months"] and any(tag in top2 for tag in ev["tags"]):
                score += EVENT_BONUS
                matching_events.append(ev["name"])

    return score, matching_events


# ── Narrative explainer ───────────────────────────────────────────────────────
def _explain(city_name, traveler_scores, matching_events) -> str:
    city   = CITIES[city_name]
    traits = city["traits"]
    top2   = sorted(traveler_scores, key=traveler_scores.get, reverse=True)[:2]

    # Open with city narrative
    base = city["narrative"]

    # Event callout
    if matching_events:
        ev_str = " and ".join(f"**{e}**" for e in matching_events[:2])
        base += f" And your timing is perfect — {ev_str} falls during your visit."

    return base


# ── Travel-time feasibility ────────────────────────────────────────────────────
def _check_feasibility(full_route: list[str], days: int) -> tuple[bool, str]:
    """
    Returns (is_tight, warning_message).
    Considers: total transit hours / 10 = travel days consumed.
    Leaves at least 0.5 explore days per intermediate stop.
    """
    legs = [(full_route[i], full_route[i+1]) for i in range(len(full_route)-1)]
    total_transit_hrs = sum(_transit_hours(a, b) for a, b in legs)
    transit_days = total_transit_hrs / 10.0  # ~10 hrs travel = 1 full day
    n_stops      = len(full_route) - 2
    min_explore  = n_stops * 0.75  # want at least 0.75 days per stop
    days_needed  = transit_days + min_explore

    if days_needed > days * 0.95:
        transit_str = f"{total_transit_hrs:.0f} hrs"
        return True, (
            f"⚠️  **This route is ambitious for {days} day{'s' if days>1 else ''}.** "
            f"Total transit time is roughly {transit_str}. "
            f"You'll spend most of your time moving rather than exploring. "
            f"Consider adding a day, reducing stops, or choosing a single closer city."
        )
    return False, ""


# ── Day-by-day itinerary ───────────────────────────────────────────────────────
def _build_itinerary(origin, stops, destination, days, travel_month):
    """
    Returns a list of day dicts:
    { "day": int, "headline": str, "detail": str, "type": "travel"|"explore"|"mixed" }
    """
    itinerary = []
    day = 1

    all_legs = [(origin, stops[0]["city"] if stops else destination)] + \
               [(stops[i]["city"], stops[i+1]["city"]) for i in range(len(stops)-1)] + \
               ([(stops[-1]["city"], destination)] if stops else [])

    # Allocate: transit gets ≥0.5 day, explore gets remaining days split evenly
    transit_hrs_list = [_transit_hours(a, b) for a, b in all_legs]
    transit_days_list = [min(h / 10.0, 1.0) for h in transit_hrs_list]
    total_transit = sum(transit_days_list)
    explore_budget = max(days - total_transit, len(stops) * 0.5)
    explore_per_stop = explore_budget / max(len(stops), 1)

    for i, (a, b) in enumerate(all_legs):
        hrs      = transit_hrs_list[i]
        mode     = _transit_mode(a, b)
        hrs_disp = f"{hrs:.0f} hr{'s' if hrs != 1 else ''}"

        # Travel day
        itinerary.append({
            "day":      day,
            "type":     "travel",
            "headline": f"{a} → {b}",
            "detail":   f"{mode} · approx. {hrs_disp}",
            "city":     b,
        })

        # Explore days for intermediate stops
        if i < len(stops):
            stop       = stops[i]
            exp_days   = max(round(explore_per_stop), 1)
            city_obj   = CITIES[stop["city"]]
            highlights = city_obj["highlights"]
            events     = stop["events"]

            # Build activity string from highlights
            acts = []
            if len(highlights) >= 1: acts.append(f"**{highlights[0]}**")
            if len(highlights) >= 2: acts.append(f"**{highlights[1]}**")
            if events:
                acts.append(f"🎟 **{events[0]}** is on — don't miss it")

            for e in range(exp_days):
                day += 1
                itinerary.append({
                    "day":      day,
                    "type":     "explore",
                    "headline": f"{stop['city']}",
                    "detail":   " · ".join(acts) if acts else "Free exploration",
                    "city":     stop["city"],
                })

        day += 1

    return itinerary


# ── Trip cost estimate ────────────────────────────────────────────────────────
def _estimate_cost(stops: list, days: int, origin: str, destination: str,
                   budget_weights: dict = None) -> dict:
    """Returns low/high estimate and a per-city breakdown, adjusted by budget weights."""
    budget_weights = budget_weights or {"transport": 25, "accommodation": 40, "activities": 35}

    # Budget weight multiplier: default weights assume a balanced spend.
    # If user skews toward cheaper accommodation, the multiplier drops.
    accom_w  = budget_weights.get("accommodation", 40) / 40   # normalise to default
    act_w    = budget_weights.get("activities", 35) / 35
    trans_w  = budget_weights.get("transport", 25) / 25
    # Blend into a single cost multiplier (accommodation dominates daily budget)
    cost_mult = (accom_w * 0.45) + (act_w * 0.30) + (trans_w * 0.25)

    if not stops:
        city = CITIES[destination]
        base = city["daily_budget_eur"] * days * cost_mult
        low  = int(base * 0.85)
        high = int(base * 1.35)
        return {"low": low, "high": high, "currency": "EUR",
                "breakdown": [{
                    "city": destination,
                    "tier": city["price_tier"],
                    "days": days,
                    "est":  int(base),
                }]}

    days_per_stop = max(days // max(len(stops), 1), 1)
    breakdown = []
    total = 0
    for stop in stops:
        city = CITIES[stop["city"]]
        est  = int(city["daily_budget_eur"] * days_per_stop * cost_mult)
        total += est
        breakdown.append({
            "city": stop["city"],
            "tier": city["price_tier"],
            "days": days_per_stop,
            "est":  est,
        })
    return {
        "low":       int(total * 0.85),
        "high":      int(total * 1.35),
        "currency":  "EUR",
        "breakdown": breakdown,
    }


# ── Shareable HTML ────────────────────────────────────────────────────────────
def generate_share_html(result: dict, scores: dict, traveler_type: str, description: str) -> str:
    stops_html = ""
    for s in result["stops"]:
        events_html = "".join(
            f'<span style="background:#fef9c3;color:#854d0e;font-size:11px;font-weight:600;'
            f'border-radius:99px;padding:2px 10px;margin-right:4px">🎟 {ev}</span>'
            for ev in s["events"]
        )
        stops_html += f"""
        <div style="border-left:4px solid #1375f0;padding:12px 16px;margin-bottom:12px;
                    background:#fff;border-radius:0 10px 10px 0;
                    box-shadow:0 1px 6px rgba(0,0,0,0.07)">
          <div style="font-size:16px;font-weight:700;color:#111827">📍 {s['city']}
            <span style="font-size:11px;font-weight:500;color:#6b7280;
                         text-transform:uppercase;letter-spacing:.06em;margin-left:8px">{s['country']}</span>
          </div>
          <div style="font-size:13px;color:#374151;margin:6px 0">{s['why']}</div>
          {events_html}
        </div>"""

    waypoints_str = " → ".join(result["waypoints"])
    score_bars_html = ""
    for cat, val in scores.items():
        pct = int((val / 5) * 100)
        score_bars_html += f"""
        <div style="display:flex;align-items:center;gap:10px;padding:5px 0;
                    border-bottom:1px solid #f3f4f6">
          <span style="flex:1;font-size:12px;color:#374151">{cat}</span>
          <div style="flex:2;background:#f3f4f6;border-radius:99px;height:7px">
            <div style="width:{pct}%;height:7px;border-radius:99px;background:#1375f0"></div>
          </div>
          <span style="width:28px;text-align:right;font-size:11px;font-weight:600;color:#6b7280">{val:.1f}</span>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>My Ravel Route — {traveler_type}</title>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:ui-sans-serif,"Segoe UI",Roboto,Arial,sans-serif;
          background:#f8fafc; color:#111827; padding:24px; }}
  .container {{ max-width:640px; margin:0 auto; }}
  .logo {{ font-size:20px; font-weight:800; color:#1375f0; letter-spacing:-.03em;
           margin-bottom:24px; }}
  .type-card {{ background:linear-gradient(135deg,#1375f0,#0d5ec4); color:#fff;
                border-radius:14px; padding:24px 28px; margin-bottom:20px;
                box-shadow:0 4px 20px rgba(19,117,240,.3); }}
  .type-label {{ font-size:11px; font-weight:700; text-transform:uppercase;
                 letter-spacing:.1em; opacity:.7; margin-bottom:4px; }}
  .type-name {{ font-size:28px; font-weight:800; letter-spacing:-.02em; margin-bottom:8px; }}
  .type-desc {{ font-size:14px; line-height:1.55; opacity:.9; }}
  .section-title {{ font-size:13px; font-weight:700; text-transform:uppercase;
                    letter-spacing:.08em; color:#6b7280; margin:20px 0 10px; }}
  .route-pill {{ background:#fff; border-radius:99px; padding:8px 16px; display:inline-block;
                 font-size:14px; font-weight:600; color:#1375f0;
                 box-shadow:0 1px 6px rgba(0,0,0,.08); margin-bottom:16px; }}
  .tip {{ background:#e8f0fe; border-radius:8px; padding:10px 14px;
          font-size:12px; color:#1e3a8a; margin-bottom:16px; }}
  .footer {{ margin-top:28px; font-size:11px; color:#9ca3af; text-align:center; }}
</style>
</head>
<body>
<div class="container">
  <div class="logo">ravel ✈</div>

  <div class="type-card">
    <div class="type-label">Your traveler type</div>
    <div class="type-name">{traveler_type}</div>
    <div class="type-desc">{description}</div>
  </div>

  <div class="section-title">Profile scores</div>
  {score_bars_html}

  <div class="section-title" style="margin-top:24px">Your route</div>
  <div class="route-pill">{waypoints_str}</div>
  {"<div class='tip'>" + result["transport_tip"] + "</div>" if result.get("transport_tip") else ""}
  {stops_html if stops_html else "<p style='font-size:13px;color:#6b7280'>Direct route — no stopovers.</p>"}

  <div class="footer">
    Ravel · Phase 1 Prototype
  </div>
</div>
</body>
</html>"""


# ── Main optimizer ─────────────────────────────────────────────────────────────
def optimise_route(
    origin, destination, days, traveler_scores,
    travel_month=None,
    pinned_stops=None,        # list of city names that MUST appear as stops
    place_type_filter=None,   # list of tags to allow e.g. ["urban","coastal"] — None = all
    budget_weights=None,      # dict {"transport":%, "accommodation":%, "activities":%} summing to 100
    days_at_dest=None,        # int — days to spend at final destination (rest = travel + stops)
) -> dict:
    if origin not in CITIES:
        raise ValueError(f"Unknown city: {origin}")
    if destination not in CITIES:
        raise ValueError(f"Unknown city: {destination}")
    if origin == destination:
        raise ValueError("Origin and destination must be different")

    pinned_stops      = [c for c in (pinned_stops or []) if c not in (origin, destination)]
    place_type_filter = place_type_filter or []
    budget_weights    = budget_weights or {"transport": 25, "accommodation": 40, "activities": 35}

    top_trait    = max(traveler_scores, key=traveler_scores.get)
    budget_score = traveler_scores.get("Budget", 3)

    # ── Budget short-circuit (skip if user pinned stops) ──────────────────
    if budget_score >= BUDGET_THRESHOLD and top_trait == "Budget" and not pinned_stops:
        direct_km  = _city_dist(origin, destination)
        mode       = _transit_mode(origin, destination)
        hrs        = _transit_hours(origin, destination)
        cost       = _estimate_cost([], days, origin, destination, budget_weights)
        itinerary  = [
            {"day":1,"type":"travel","headline":f"{origin} → {destination}",
             "detail":f"{mode} · approx. {hrs:.0f} hrs","city":destination},
            {"day":2,"type":"explore","headline":destination,
             "detail": " · ".join(CITIES[destination]["highlights"][:2]),"city":destination},
        ]
        return {
            "waypoints":     [origin, destination],
            "stops":         [],
            "direct":        True,
            "direct_reason": (
                f"Your profile is optimised for budget travel (score {budget_score:.1f}/5). "
                f"A direct {origin} → {destination} means no extra hotel nights and no detour fares. "
                f"The money you save goes toward experiences, not transport."
            ),
            "transport_tip": TRANSPORT_ADVICE["Budget"],
            "total_km":      round(direct_km),
            "month":         MONTH_NAMES.get(travel_month),
            "itinerary":     itinerary,
            "cost":          cost,
            "feasibility_warning": "",
            "days_breakdown": {"travel": 1, "stays": {destination: days - 1}},
        }

    # ── Score candidate cities ─────────────────────────────────────────────
    detour = DETOUR_FACTORS.get(top_trait, 1.5)
    # Widen corridor if user pinned stops that might be off-corridor
    if pinned_stops:
        detour = max(detour, 2.0)

    candidates = []
    for city_name in CITIES:
        if city_name in (origin, destination):
            continue
        if city_name in pinned_stops:
            continue  # pinned stops added separately below
        if not _is_feasible(origin, destination, city_name, detour):
            continue
        # Place-type filter
        if place_type_filter:
            tags = CITY_TAGS.get(city_name, [])
            if not any(t in tags for t in place_type_filter):
                continue
        score, events = _score_city(city_name, traveler_scores, travel_month)
        candidates.append((city_name, score, events))

    candidates.sort(key=lambda x: x[1], reverse=True)

    # Reserve slots for pinned stops; fill remaining with top scored candidates
    n_stops    = min(max(days - 1, 1), 3)
    n_fill     = max(n_stops - len(pinned_stops), 0)
    chosen     = candidates[:n_fill]

    # Score pinned stops too (for events / narrative)
    pinned_scored = []
    for p in pinned_stops:
        if p in CITIES:
            sc, ev = _score_city(p, traveler_scores, travel_month)
            pinned_scored.append((p, sc, ev))

    all_stops_unordered = pinned_scored + chosen

    # ── Order stops geographically (greedy nearest-neighbour) ──────────────
    remaining, ordered, current = list(all_stops_unordered), [], origin
    while remaining:
        remaining.sort(key=lambda x: _city_dist(current, x[0]))
        nxt = remaining.pop(0)
        ordered.append(nxt)
        current = nxt[0]

    # ── Build stop dicts ───────────────────────────────────────────────────
    stops = []
    for city_name, score, events in ordered:
        city = CITIES[city_name]
        stops.append({
            "city":       city_name,
            "country":    city["country"],
            "price_tier": city["price_tier"],
            "score":      round(score, 2),
            "highlights": city["highlights"],
            "events":     events,
            "why":        _explain(city_name, traveler_scores, events),
            "pinned":     city_name in pinned_stops,
        })

    full_route = [origin] + [s["city"] for s in stops] + [destination]
    total_km   = sum(_city_dist(full_route[i], full_route[i+1]) for i in range(len(full_route)-1))

    # ── Feasibility check ──────────────────────────────────────────────────
    tight, warning = _check_feasibility(full_route, days)

    # ── Days breakdown ─────────────────────────────────────────────────────
    legs = list(zip(full_route, full_route[1:]))
    total_transit_hrs = sum(_transit_hours(a, b) for a, b in legs)
    travel_days = round(total_transit_hrs / 10.0, 1)
    explore_days = max(days - travel_days, len(stops) * 0.5)
    days_per_stop = round(explore_days / max(len(stops) + (1 if days_at_dest else 0), 1), 1)
    dest_days = days_at_dest if days_at_dest else days_per_stop

    stays = {s["city"]: days_per_stop for s in stops}
    stays[destination] = dest_days

    days_breakdown = {
        "travel_days":     round(travel_days, 1),
        "explore_days":    round(explore_days, 1),
        "stays":           stays,
        "dest_days":       round(dest_days, 1),
    }

    # ── Itinerary + cost ───────────────────────────────────────────────────
    itinerary = _build_itinerary(origin, stops, destination, days, travel_month)
    cost      = _estimate_cost(stops, days, origin, destination, budget_weights)

    return {
        "waypoints":           full_route,
        "stops":               stops,
        "direct":              False,
        "direct_reason":       None,
        "transport_tip":       TRANSPORT_ADVICE.get(top_trait, TRANSPORT_ADVICE["Culture"]),
        "total_km":            round(total_km),
        "month":               MONTH_NAMES.get(travel_month),
        "itinerary":           itinerary,
        "cost":                cost,
        "feasibility_warning": warning,
        "days_breakdown":      days_breakdown,
    }
