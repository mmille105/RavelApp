import streamlit as st
import streamlit.components.v1 as stc
import plotly.graph_objects as go
import json

from scoring import calculate_scores, classify_traveler, CATEGORIES
from routing import optimise_route, MONTH_NAMES, generate_share_html
from cities  import CITIES

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ravel — Where are you going?",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# Brand CSS — Ravel design system
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Tokens ── */
:root {
  --blue:     #1375f0;
  --blue-dk:  #0d5ec4;
  --blue-lt:  #e8f0fe;
  --yellow:   #feda31;
  --green:    #1bb368;
  --red:      #ef4444;
  --text:     #111827;
  --muted:    #6b7280;
  --border:   #e5e7eb;
  --bg:       #f8fafc;
  --card:     #ffffff;
  --radius:   0.875rem;
  --shadow:   0 2px 16px rgba(0,0,0,0.07);
}

/* ── Global resets ── */
#MainMenu, footer, header { visibility: hidden; }

/* Desktop: centre content in 820px column */
.block-container {
  padding: 1.75rem 2rem 3rem !important;
  max-width: 820px !important;
  margin: 0 auto !important;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg);
  font-family: ui-sans-serif, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: var(--text);
}

/* ── Tablet (≤ 900px) ── */
@media (max-width: 900px) {
  .block-container { padding: 1.25rem 1.25rem 2.5rem !important; }
  .hero-title { font-size: 2rem !important; }
}

/* ── Mobile (≤ 640px) ── */
@media (max-width: 640px) {
  .block-container { padding: 1rem 0.85rem 2rem !important; max-width: 100% !important; }

  /* Typography scale-down */
  .hero-title { font-size: 1.75rem !important; }
  .hero-sub   { font-size: .93rem !important; }
  .type-name  { font-size: 1.5rem !important; }
  .cat-name   { font-size: 1.2rem !important; }

  /* Cards: tighten padding */
  .card { padding: 1.2rem 1.1rem !important; }
  .type-card { padding: 1.4rem 1.2rem !important; }
  .stop-card { padding: .9rem 1rem !important; }

  /* Nav: stack wordmark above nav pills */
  [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }

  /* Quiz pills on mobile — keep branded style, compact gap */
  [data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: .3rem !important;
  }
  [data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label {
    font-size: 1rem !important;
    min-height: 2.75rem !important;
    border-width: 1.5px !important;
  }

  /* Scale legend: stays visible on mobile — numbers need the context */

  /* Stat pills: 2 columns on mobile */
  .stat-row { gap: .5rem !important; }
  .stat-pill { min-width: calc(50% - .25rem) !important; }

  /* Intro 3-col grid → single column */
  div[style*="grid-template-columns: 1fr 1fr 1fr"] {
    grid-template-columns: 1fr !important;
  }

  /* Phase 2 & cost 2-col grid → single column */
  div[style*="grid-template-columns: 1fr 1fr"] {
    grid-template-columns: 1fr !important;
  }

  /* Timeline: tighten left spacing */
  .timeline { padding-left: 1rem !important; }
  .tl-item  { padding-left: .9rem !important; }

  /* Map: shorter on mobile */
  [data-testid="stPlotlyChart"] { min-height: 240px !important; }

  /* Expander headers */
  [data-testid="stExpander"] summary { font-size: .88rem !important; }

  /* Download buttons: full width on mobile */
  .stDownloadButton button { width: 100% !important; font-size: .83rem !important; }

  /* Selectbox labels */
  [data-testid="stSelectbox"] label { font-size: .85rem !important; }

  /* Slider */
  [data-testid="stSlider"] label { font-size: .85rem !important; }
}

/* ── Page-entry fade ── */
.block-container { animation: fadeUp 0.22s ease both; }
@keyframes fadeUp {
  from { opacity:0; transform:translateY(6px); }
  to   { opacity:1; transform:translateY(0); }
}

/* ── Wordmark ── */
.wordmark {
  font-size: 1.15rem; font-weight: 800; color: var(--blue);
  letter-spacing: -.03em;
}

/* ── Nav ── */
.nav { display:flex; align-items:center; justify-content:space-between;
       padding-bottom: 1.25rem; border-bottom: 1px solid var(--border);
       margin-bottom: 2rem; }

/* ── Cards ── */
.card { background:var(--card); border-radius:var(--radius);
        box-shadow:var(--shadow); padding:1.75rem 2rem; margin-bottom:1.25rem; }
.card-flush { background:var(--card); border-radius:var(--radius);
              box-shadow:var(--shadow); overflow:hidden; margin-bottom:1.25rem; }

/* ── Hero ── */
.hero-title { font-size:2.5rem; font-weight:800; line-height:1.1;
              letter-spacing:-.03em; margin-bottom:.4rem; }
.hero-sub   { font-size:1.05rem; color:var(--muted); line-height:1.6; margin-bottom:1.5rem; }

/* ── Progress ── */
.prog-track { background:var(--border); border-radius:99px; height:4px;
              width:100%; margin-bottom:.4rem; }
.prog-fill  { background:var(--blue); border-radius:99px; height:4px;
              transition:width .35s ease; }
.prog-label { font-size:.75rem; color:var(--muted); margin-bottom:1.5rem;
              font-weight:500; letter-spacing:.02em; text-transform:uppercase; }

/* ── Category header ── */
.cat-row  { display:flex; align-items:center; gap:.5rem; margin-bottom:.5rem; }
.cat-name { font-size:1.4rem; font-weight:800; }
.cat-sub  { font-size:.88rem; color:var(--muted); margin-bottom:1.5rem; }

/* ── Nav radio — slim tab-style pills ── */
div[data-testid="stRadio"] div[role="radiogroup"] {
  display: flex !important;
  flex-direction: row !important;
  gap: .4rem !important;
  margin-top: 0 !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] label {
  background: #fff !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 99px !important;
  padding: .3rem .95rem !important;
  font-size: .82rem !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: background .12s, border-color .12s, color .12s !important;
  white-space: nowrap !important;
  color: var(--muted) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: 0 1px 3px rgba(0,0,0,.07) !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
  background: var(--blue) !important;
  border-color: var(--blue) !important;
  color: #fff !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 8px rgba(19,117,240,.28) !important;
}
/* Hide the actual radio circle on all radio buttons */
div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {
  display: none !important;
  width: 0 !important;
  height: 0 !important;
  overflow: hidden !important;
  position: absolute !important;
}

/* ── Quiz radio pills — scoped to inside st.form only ── */

/* Kill the "rating" ghost label */
[data-testid="stForm"] div[data-testid="stRadio"] [data-testid="stWidgetLabel"],
[data-testid="stForm"] div[data-testid="stRadio"] [data-testid="stWidgetLabel"] * {
  display: none !important;
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}

/* 5-column grid — always fits any screen width */
[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] {
  display: grid !important;
  grid-template-columns: repeat(5, 1fr) !important;
  gap: .4rem !important;
  margin-top: .5rem !important;
  width: 100% !important;
}

/* Hide the radio circle dot — force truly centered number */
[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {
  display: none !important;
  width: 0 !important;
  height: 0 !important;
  overflow: hidden !important;
  position: absolute !important;
  pointer-events: none !important;
}

/* Quiz pill cells — branded number buttons */
[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label {
  background: #fff !important;
  border: 2px solid var(--blue) !important;
  border-radius: .65rem !important;
  padding: 0 !important;
  font-size: 1.05rem !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  white-space: nowrap !important;
  color: var(--blue) !important;
  text-align: center !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1 !important;
  min-height: 2.75rem !important;
  transition: background .12s, border-color .12s, color .12s, box-shadow .12s !important;
  letter-spacing: 0 !important;
  box-shadow: 0 1px 4px rgba(19,117,240,.12) !important;
}
[data-testid="stForm"] div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
  background: var(--blue) !important;
  border-color: var(--blue) !important;
  color: #fff !important;
  font-weight: 800 !important;
  box-shadow: 0 3px 10px rgba(19,117,240,.35) !important;
}

/* ── Question card wrapper for quiz ── */
.q-card {
  background: var(--card);
  border-radius: .75rem;
  border: 1.5px solid var(--border);
  padding: 1.1rem 1.3rem 1rem;
  margin-bottom: .75rem;
}
.q-text {
  font-size: .975rem;
  font-weight: 600;
  color: var(--text);
  line-height: 1.5;
  margin-bottom: .75rem;
}
.q-scale-legend {
  display: flex;
  justify-content: space-between;
  font-size: .7rem;
  color: var(--muted);
  margin-bottom: .4rem;
  padding: 0 .1rem;
  font-weight: 500;
}

/* ── Primary button ── */
.stButton > button {
  background: var(--blue) !important;
  color: #fff !important;
  border: none !important;
  border-radius: .6rem !important;
  font-weight: 600 !important;
  font-size: .95rem !important;
  padding: .6rem 1.5rem !important;
  box-shadow: 0 2px 8px rgba(19,117,240,.22) !important;
  transition: background .15s;
}
.stButton > button:hover { background: var(--blue-dk) !important; }

/* ── Traveler type result card ── */
.type-card {
  background: linear-gradient(135deg, #1375f0 0%, #0d5ec4 100%);
  color: #fff; border-radius: var(--radius);
  padding: 1.9rem 2.1rem; margin-bottom: 1.25rem;
  box-shadow: 0 4px 24px rgba(19,117,240,.3);
}
.type-eyebrow { font-size:.7rem; font-weight:700; text-transform:uppercase;
                letter-spacing:.12em; opacity:.65; margin-bottom:.25rem; }
.type-name    { font-size:2rem; font-weight:800; letter-spacing:-.025em; margin-bottom:.55rem; }
.type-desc    { font-size:.95rem; line-height:1.6; opacity:.9; }
.type-badge   { display:inline-flex; align-items:center; gap:.3rem;
                background:var(--yellow); color:#111; font-weight:700;
                font-size:.75rem; border-radius:99px;
                padding:.22rem .8rem; margin-top:.9rem; }

/* ── Score bars ── */
.sbar-row  { display:flex; align-items:center; gap:.65rem; padding:.45rem 0;
             border-bottom:1px solid #f3f4f6; }
.sbar-row:last-child { border-bottom:none; }
.sbar-cat  { flex:1; font-size:.875rem; }
.sbar-wrap { flex:2.5; background:#f3f4f6; border-radius:99px; height:7px; }
.sbar-fill { height:7px; border-radius:99px; }
.sbar-val  { width:2.2rem; text-align:right; font-size:.8rem; font-weight:600; color:var(--muted); }

/* ── Route stop cards ── */
.stop-card {
  background: var(--card); border-radius: var(--radius);
  box-shadow: var(--shadow); padding: 1.1rem 1.4rem;
  margin-bottom: .75rem; border-left: 4px solid var(--blue);
}
.stop-city    { font-size:1.05rem; font-weight:700; }
.stop-meta    { font-size:.73rem; color:var(--muted); font-weight:600;
                text-transform:uppercase; letter-spacing:.07em; margin-bottom:.4rem; }
.stop-why     { font-size:.875rem; color:#374151; line-height:1.55; margin-bottom:.4rem; }
.stop-hl      { font-size:.8rem; color:var(--muted); }
.stop-event   { display:inline-block; background:#fef9c3; color:#854d0e;
                font-size:.73rem; font-weight:700; border-radius:99px;
                padding:.15rem .65rem; margin-top:.4rem; margin-right:.3rem; }
.stop-tier    { display:inline-block; background:#f0fdf4; color:#166534;
                font-size:.73rem; font-weight:700; border-radius:99px;
                padding:.15rem .65rem; margin-top:.4rem; margin-right:.3rem; }

/* ── Timeline itinerary ── */
.timeline { padding-left:1.5rem; border-left: 2px solid var(--border);
            margin:1rem 0 1.5rem; }
.tl-item  { position:relative; padding:.6rem 0 .6rem 1.2rem; }
.tl-item::before {
  content:""; position:absolute; left:-1.45rem; top:.8rem;
  width:.75rem; height:.75rem; border-radius:50%;
  background:var(--blue); border:2px solid var(--card);
  box-shadow:0 0 0 2px var(--blue);
}
.tl-travel::before { background:#e5e7eb; box-shadow:0 0 0 2px #9ca3af; }
.tl-day   { font-size:.7rem; font-weight:700; color:var(--muted);
            text-transform:uppercase; letter-spacing:.07em; margin-bottom:.1rem; }
.tl-head  { font-size:.9rem; font-weight:700; color:var(--text); }
.tl-detail{ font-size:.8rem; color:var(--muted); margin-top:.1rem; }

/* ── Stat pills ── */
.stat-row { display:flex; gap:.75rem; flex-wrap:wrap; margin-bottom:1rem; }
.stat-pill { background:var(--card); border-radius:.65rem; padding:.65rem 1rem;
             box-shadow:var(--shadow); flex:1; min-width:110px; }
.stat-label { font-size:.68rem; color:var(--muted); text-transform:uppercase;
              letter-spacing:.07em; margin-bottom:.15rem; font-weight:600; }
.stat-val   { font-size:.95rem; font-weight:700; }

/* ── Warning box ── */
.warn-box { background:#fff7ed; border:1.5px solid #fed7aa; border-radius:.65rem;
            padding:.85rem 1.1rem; font-size:.85rem; color:#92400e; margin-bottom:1rem; }

/* ── Transport tip ── */
.tip-box { background:var(--blue-lt); border-radius:.65rem; padding:.8rem 1.1rem;
           font-size:.83rem; color:#1e3a8a; margin-bottom:1rem; }

/* ── Direct route ── */
.direct-box { background:#f0fdf4; border:1.5px solid #bbf7d0; border-radius:.65rem;
              padding:1.1rem 1.4rem; margin-bottom:1rem; }

/* ── Cost box ── */
.cost-box { background:linear-gradient(135deg,#f0fdf4,#dcfce7);
            border-radius:var(--radius); padding:1.2rem 1.6rem;
            margin-bottom:1rem; border:1.5px solid #bbf7d0; }

/* ── Selectbox & slider ── */
[data-testid="stSelectbox"] { margin-bottom:.25rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS = {
    "page": "profile",
    "quiz_step": 0,
    "responses": {},
    "scores": {},
    "traveler_type": "",
    "traveler_desc": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# Top navigation
# ─────────────────────────────────────────────────────────────────────────────
c_logo, c_nav = st.columns([1, 2])
with c_logo:
    st.markdown('<div class="wordmark">ravel ✈</div>', unsafe_allow_html=True)
with c_nav:
    nav = st.radio("nav", ["Travel Profile", "Route Optimizer"],
                   horizontal=True, label_visibility="collapsed")
st.markdown("<hr style='margin:0 0 1.75rem;border-color:#e5e7eb'>", unsafe_allow_html=True)

page = "profile" if nav == "Travel Profile" else "router"

# ─────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────────────
CAT_COLORS = {
    "Adventure":"#1375f0","Budget":"#1bb368","Culture":"#8b5cf6",
    "Relaxation":"#f59e0b","Food":"#ef4444","Shopping":"#ec4899",
}

# Numeric pills — always fit any screen width; legend provides context
LIKERT = ["1", "2", "3", "4", "5"]

def likert_val(label: str) -> int:
    """Convert pill label to 1-5 int score."""
    return LIKERT.index(label) + 1

def render_score_bars(scores):
    rows = "".join(f"""
    <div class="sbar-row">
      <span class="sbar-cat">{cat}</span>
      <div class="sbar-wrap">
        <div class="sbar-fill" style="width:{int((v/5)*100)}%;background:{CAT_COLORS.get(cat,'#1375f0')}"></div>
      </div>
      <span class="sbar-val">{v:.1f}</span>
    </div>""" for cat, v in scores.items())
    st.markdown(f'<div class="card">{rows}</div>', unsafe_allow_html=True)

def render_radar(scores, title="Your Travel Profile"):
    cats = list(scores.keys()); vals = list(scores.values())
    fig = go.Figure(go.Scatterpolar(
        r=vals+[vals[0]], theta=cats+[cats[0]],
        fill="toself", fillcolor="rgba(19,117,240,0.12)",
        line=dict(color="#1375f0", width=2.5),
        hovertemplate="<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="#f8fafc",
            radialaxis=dict(visible=True, range=[0,5], tickvals=[1,2,3,4,5],
                            tickfont=dict(size=9,color="#9ca3af"),
                            gridcolor="#e5e7eb", linecolor="#e5e7eb"),
            angularaxis=dict(tickfont=dict(size=11,color="#111827"),
                             gridcolor="#e5e7eb", linecolor="#e5e7eb"),
        ),
        paper_bgcolor="#ffffff", showlegend=False,
        autosize=True,
        margin=dict(t=40,b=40,l=30,r=30),
        title=dict(text=title, font=dict(size=14,color="#111827"), x=0.5),
    )
    st.markdown('<div class="card" style="padding:.75rem">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: TRAVEL PROFILE
# ═════════════════════════════════════════════════════════════════════════════

STEPS = [
    {"category":"Adventure",  "emoji":"🧗", "tagline":"How much do you crave the wild side?",
     "questions":[
         ("Q1",  "I enjoy physically demanding activities like hiking, climbing, or extreme sports."),
         ("Q2",  "I prefer destinations that are off the beaten path."),
         ("Q3",  "I'm comfortable with uncertainty and unplanned situations while travelling."),
         ("Q4",  "I seek out adrenaline-inducing experiences when I travel."),
         ("Q5",  "I'd rather explore wild nature than spend time in a city."),
     ]},
    {"category":"Budget",     "emoji":"💰", "tagline":"How do you think about spending on travel?",
     "questions":[
         ("Q6",  "Transportation: I search for the cheapest flights, trains, or buses rather than paying for speed or comfort."),
         ("Q7",  "Accommodation: I choose budget stays (hostels, budget hotels, Airbnb) over comfort or luxury options."),
         ("Q8",  "Food: I prefer eating at local, inexpensive spots rather than restaurants or fine dining."),
         ("Q9",  "Activities: I prioritise free or low-cost attractions over paid experiences or guided tours."),
         ("Q10", "Souvenirs & Shopping: I set a strict budget for souvenirs and stick to it, even when tempted."),
     ]},
    {"category":"Culture",    "emoji":"🏛️", "tagline":"How deeply do you dive into local culture?",
     "questions":[
         ("Q11", "I visit museums, galleries, or historical sites on most trips."),
         ("Q12", "I make an effort to learn about local customs before I travel."),
         ("Q13", "I enjoy attending local festivals or cultural events."),
         ("Q14", "I try to learn a few words of the local language before I visit."),
         ("Q15", "I prefer destinations with rich history or cultural heritage."),
     ]},
    {"category":"Relaxation", "emoji":"🌅", "tagline":"How much do you value rest and recharge?",
     "questions":[
         ("Q16", "I prefer vacations where I can slow down and genuinely recharge."),
         ("Q17", "Spa treatments, yoga, or wellness activities appeal to me when travelling."),
         ("Q18", "I enjoy spending time by the pool or on the beach with nowhere to be."),
         ("Q19", "I avoid overly packed itineraries — a relaxed pace is important to me."),
         ("Q20", "My ideal trip involves minimal stress and maximum comfort."),
     ]},
    {"category":"Food",       "emoji":"🍜", "tagline":"How central is food to your travel experience?",
     "questions":[
         ("Q21", "Trying local cuisine is one of the highlights of any trip for me."),
         ("Q22", "I research restaurants and food markets before visiting a destination."),
         ("Q23", "I'd choose a destination partly because of its food scene."),
         ("Q24", "I enjoy cooking classes, food tours, or market visits when I travel."),
         ("Q25", "I'm adventurous and open to trying unfamiliar foods."),
     ]},
    {"category":"Shopping",   "emoji":"🛍️", "tagline":"How much does shopping shape your trips?",
     "questions":[
         ("Q26", "Shopping for souvenirs or local goods is an important part of my travels."),
         ("Q27", "I visit local markets or bazaars as a cultural experience, not just to buy."),
         ("Q28", "I set aside a specific budget for shopping on trips."),
         ("Q29", "I enjoy browsing boutiques, design stores, or flagship shops when I travel."),
     ]},
]

if page == "profile":
    step = st.session_state.quiz_step

    # ── 0: Intro ──────────────────────────────────────────────────────────
    if step == 0:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1375f0 0%,#0d5ec4 100%);
                    border-radius:var(--radius);padding:2.5rem 2.25rem 2rem;
                    margin-bottom:1.25rem;box-shadow:0 4px 24px rgba(19,117,240,.28)">
          <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                      letter-spacing:.14em;color:rgba(255,255,255,.6);margin-bottom:.6rem">
            Ravel · Phase 1 Prototype
          </div>
          <p style="font-size:2.5rem;font-weight:800;line-height:1.1;
                    letter-spacing:-.03em;color:#fff;margin-bottom:.6rem">
            Where inspiration<br>meets organization.
          </p>
          <p style="font-size:1rem;color:rgba(255,255,255,.85);line-height:1.6;
                    margin-bottom:1.5rem">
            The fun is in the daydreaming phase.<br>
            Tell us who you are as a traveller — we'll do the rest.
          </p>
          <div style="display:flex;gap:.6rem;flex-wrap:wrap">
            <span style="background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);
                         border-radius:99px;padding:.25rem .85rem;font-size:.78rem;
                         font-weight:600;color:#fff">✦ 29 questions</span>
            <span style="background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);
                         border-radius:99px;padding:.25rem .85rem;font-size:.78rem;
                         font-weight:600;color:#fff">✦ 6 travel dimensions</span>
            <span style="background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);
                         border-radius:99px;padding:.25rem .85rem;font-size:.78rem;
                         font-weight:600;color:#fff">✦ 10 traveler types</span>
            <span style="background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);
                         border-radius:99px;padding:.25rem .85rem;font-size:.78rem;
                         font-weight:600;color:#fff">✦ ~3 minutes</span>
          </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:.75rem;margin-bottom:1.25rem">
          <div class="card" style="padding:1.1rem 1.2rem;text-align:center">
            <div style="font-size:1.5rem;margin-bottom:.4rem">🧭</div>
            <div style="font-size:.82rem;font-weight:700;color:var(--text);margin-bottom:.2rem">
              Travel Profile
            </div>
            <div style="font-size:.75rem;color:var(--muted);line-height:1.4">
              Discover your traveler type & radar chart
            </div>
          </div>
          <div class="card" style="padding:1.1rem 1.2rem;text-align:center">
            <div style="font-size:1.5rem;margin-bottom:.4rem">🗺️</div>
            <div style="font-size:.82rem;font-weight:700;color:var(--text);margin-bottom:.2rem">
              Route Optimizer
            </div>
            <div style="font-size:.75rem;color:var(--muted);line-height:1.4">
              Persona-matched stops, events & budget
            </div>
          </div>
          <div class="card" style="padding:1.1rem 1.2rem;text-align:center;
                                   border:1.5px dashed var(--border)">
            <div style="font-size:1.5rem;margin-bottom:.4rem">🏨</div>
            <div style="font-size:.82rem;font-weight:700;color:var(--muted);margin-bottom:.2rem">
              Coming in v2
            </div>
            <div style="font-size:.75rem;color:var(--muted);line-height:1.4">
              Hotel picks, intra-city transit & dining
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        _, c, _ = st.columns([1,2,1])
        with c:
            if st.button("Start my profile →", use_container_width=True):
                st.session_state.quiz_step = 1
                st.rerun()

    # ── 1-6: Questions ────────────────────────────────────────────────────
    elif 1 <= step <= 6:
        # Scroll to top of page on every step load (fires on Next / Back only,
        # since questions live inside st.form which suppresses interim reruns)
        stc.html("""
        <script>
          (function() {
            var tries = 0;
            function scrollUp() {
              var el = window.parent.document.querySelector('section[data-testid="stMain"]')
                    || window.parent.document.querySelector('.main');
              if (el) { el.scrollTo({top: 0, behavior: 'smooth'}); }
              window.parent.scrollTo(0, 0);
              if (tries++ < 5) setTimeout(scrollUp, 80);
            }
            scrollUp();
          })();
        </script>
        """, height=0)

        data = STEPS[step - 1]
        pct  = int(((step-1) / 6) * 100)
        st.markdown(f"""
        <div class="prog-track"><div class="prog-fill" style="width:{pct}%"></div></div>
        <p class="prog-label">Step {step} of 6 — {data['category']}</p>
        <div class="cat-row">
          <span style="font-size:1.6rem">{data['emoji']}</span>
          <span class="cat-name">{data['category']}</span>
        </div>
        <p class="cat-sub">{data['tagline']}</p>
        """, unsafe_allow_html=True)

        with st.form(f"quiz_{step}"):
            resp = {}
            for i, (qid, text) in enumerate(data["questions"]):
                saved_int = st.session_state.responses.get(qid, 3)
                saved_lbl = LIKERT[saved_int - 1]
                st.markdown(f"""
                <div class="q-card">
                  <div class="q-text">{i+1}. {text}</div>
                  <div class="q-scale-legend">
                    <span>1 = Strongly disagree</span>
                    <span>5 = Strongly agree</span>
                  </div>
                </div>""", unsafe_allow_html=True)
                resp[qid] = st.radio(
                    label="rating",           # hidden — question shown above
                    options=LIKERT,
                    index=LIKERT.index(saved_lbl),
                    horizontal=True,
                    label_visibility="collapsed",
                    key=f"r_{qid}",
                )
                st.markdown("<div style='height:.25rem'></div>", unsafe_allow_html=True)

            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            cb, _, cn = st.columns([1, 2, 1])
            with cb:
                back = st.form_submit_button("← Back", use_container_width=True)
            with cn:
                label = "Next →" if step < 6 else "See my results ✨"
                nxt   = st.form_submit_button(label, use_container_width=True)

            if nxt:
                st.session_state.responses.update({k: likert_val(v) for k, v in resp.items()})
                st.session_state.quiz_step += 1
                st.rerun()
            if back and step > 1:
                st.session_state.responses.update({k: likert_val(v) for k, v in resp.items()})
                st.session_state.quiz_step -= 1
                st.rerun()

    # ── 7: Results ────────────────────────────────────────────────────────
    elif step == 7:
        scores = calculate_scores(st.session_state.responses, CATEGORIES)
        traveler_type, description, dominant = classify_traveler(scores)
        st.session_state.scores         = scores
        st.session_state.traveler_type  = traveler_type
        st.session_state.traveler_desc  = description

        top2    = sorted(scores, key=scores.get, reverse=True)[:2]
        top_val = scores[dominant]

        # ── Type card ──
        st.markdown(f"""
        <div class="type-card">
          <p class="type-eyebrow">Your traveler type</p>
          <p class="type-name">{traveler_type}</p>
          <p class="type-desc">{description}</p>
          <span class="type-badge">✦ Top trait: {dominant}</span>
        </div>""", unsafe_allow_html=True)

        # ── Insight sentence ──
        runner_up = top2[1] if len(top2) > 1 else None
        insight = (
            f"Your **{dominant}** score of **{top_val:.1f}/5** is your strongest signal. "
            + (f"**{runner_up}** runs close behind, so your ideal route should deliver both." if runner_up else "")
        )
        st.markdown(f"<p style='font-size:.9rem;color:#374151;margin-bottom:1rem'>{insight}</p>",
                    unsafe_allow_html=True)

        render_score_bars(scores)
        render_radar(scores)

        # ── Actions ──
        c1, c2 = st.columns(2)
        with c1:
            share_html = generate_share_html(
                {"waypoints":[],"stops":[],"transport_tip":"","direct":True,
                 "direct_reason":"","total_km":0,"month":None},
                scores, traveler_type, description
            )
            st.download_button("Share profile (HTML)", data=share_html,
                               file_name="ravel_profile.html", mime="text/html",
                               use_container_width=True)
        with c2:
            if st.button("Retake quiz", use_container_width=True):
                st.session_state.quiz_step = 0
                st.session_state.responses = {}
                st.rerun()

        st.markdown("""
        <div style="background:var(--blue-lt);border-radius:.65rem;padding:.85rem 1.1rem;
                    font-size:.875rem;color:#1e3a8a;margin-top:.5rem">
          ✈  <strong>Ready to plan your trip?</strong>
          Switch to the <strong>Route Optimizer</strong> tab — your profile loads automatically.
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#fff;border:1.5px dashed #e5e7eb;border-radius:var(--radius);
                    padding:1.2rem 1.5rem;margin-top:.75rem">
          <div style="font-size:.7rem;font-weight:700;text-transform:uppercase;
                      letter-spacing:.1em;color:var(--muted);margin-bottom:.5rem">
            Coming in Ravel v2
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem">
            <div style="font-size:.82rem;color:#374151">
              🏨 <strong>Hotel recommendations</strong><br>
              <span style="color:var(--muted)">Matched to your profile — boutique, budget, or luxury</span>
            </div>
            <div style="font-size:.82rem;color:#374151">
              🚇 <strong>Intra-city transit</strong><br>
              <span style="color:var(--muted)">"Take the 2 train — €2.35, 0.25mi walk to the Louvre"</span>
            </div>
            <div style="font-size:.82rem;color:#374151">
              🍽️ <strong>Restaurant matching</strong><br>
              <span style="color:var(--muted)">Dining picks near your hotel and your stops</span>
            </div>
            <div style="font-size:.82rem;color:#374151">
              🤝 <strong>Group profiles</strong><br>
              <span style="color:var(--muted)">Blend multiple traveler types into one shared route</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ROUTE OPTIMIZER
# ═════════════════════════════════════════════════════════════════════════════

elif page == "router":

    st.markdown("""
    <div class="card">
      <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                  letter-spacing:.12em;color:var(--blue);margin-bottom:.4rem">
        Ravel · Route Optimizer
      </div>
      <p class="hero-title">The fun is in the<br>daydreaming phase.</p>
      <p class="hero-sub">
        Pick your start, your end, and how long you have.<br>
        Your traveler profile does the rest — matched stops, live events, and a budget breakdown.
      </p>
      <div style="display:flex;gap:.5rem;flex-wrap:wrap">
        <span style="background:var(--blue-lt);color:var(--blue);border-radius:99px;
                     padding:.2rem .75rem;font-size:.75rem;font-weight:600">52 cities</span>
        <span style="background:var(--blue-lt);color:var(--blue);border-radius:99px;
                     padding:.2rem .75rem;font-size:.75rem;font-weight:600">Real monthly events</span>
        <span style="background:var(--blue-lt);color:var(--blue);border-radius:99px;
                     padding:.2rem .75rem;font-size:.75rem;font-weight:600">Day-by-day itinerary</span>
        <span style="background:var(--blue-lt);color:var(--blue);border-radius:99px;
                     padding:.2rem .75rem;font-size:.75rem;font-weight:600">Budget estimate</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Persona library ────────────────────────────────────────────────────
    PERSONAS = {
        "The Adventurer":           {"Adventure":4.6,"Budget":2.5,"Culture":3.0,"Relaxation":2.0,"Food":3.0,"Shopping":2.0},
        "The Budget Explorer":      {"Adventure":3.0,"Budget":4.8,"Culture":3.0,"Relaxation":2.5,"Food":2.5,"Shopping":2.0},
        "The Cultural Connoisseur": {"Adventure":2.0,"Budget":2.5,"Culture":4.8,"Relaxation":3.5,"Food":3.5,"Shopping":3.0},
        "The Wellness Wanderer":    {"Adventure":2.0,"Budget":2.5,"Culture":3.0,"Relaxation":4.8,"Food":3.5,"Shopping":3.0},
        "The Culinary Nomad":       {"Adventure":2.5,"Budget":3.0,"Culture":3.5,"Relaxation":3.0,"Food":4.8,"Shopping":2.5},
        "The Style Traveler":       {"Adventure":2.0,"Budget":2.0,"Culture":3.5,"Relaxation":3.5,"Food":3.5,"Shopping":4.8},
    }

    # ── Profile source ─────────────────────────────────────────────────────
    has_profile = bool(st.session_state.scores)

    if has_profile:
        src = st.radio("Use", ["My saved profile", "A preset persona"],
                       horizontal=True, label_visibility="collapsed")
    else:
        src = "A preset persona"
        st.caption("💡 Complete the **Travel Profile** quiz to unlock your personal scores.")

    if src == "My saved profile" and has_profile:
        active_scores = st.session_state.scores
        saved_type    = st.session_state.traveler_type
        st.markdown(
            f'<p style="font-size:.82rem;color:var(--muted);margin-bottom:.5rem">'
            f'Using profile: <strong>{saved_type}</strong></p>',
            unsafe_allow_html=True
        )
    else:
        persona_name  = st.selectbox("Persona", list(PERSONAS.keys()), label_visibility="collapsed")
        active_scores = PERSONAS[persona_name]

    st.markdown("<hr style='margin:.75rem 0;border-color:var(--border)'>", unsafe_allow_html=True)

    # ── Build hierarchical Country → City options ─────────────────────────
    # Groups cities by country, sorts both alphabetically, then renders as
    # "Country — City" option strings with non-selectable country headers.
    from collections import defaultdict
    country_map = defaultdict(list)
    for city_name, city_data in CITIES.items():
        country_map[city_data["country"]].append(city_name)

    # Build ordered option list: header rows (prefixed ▸) + indented city rows
    CITY_OPTIONS   = []   # selectable city strings shown in dropdown
    DISPLAY_OPTIONS = []  # includes non-selectable country headers
    for country in sorted(country_map.keys()):
        cities_in_country = sorted(country_map[country])
        for city in cities_in_country:
            CITY_OPTIONS.append(f"{country} — {city}")

    def city_label_to_name(label: str) -> str:
        """Extract just the city name from 'Country — City'."""
        return label.split(" — ", 1)[1] if " — " in label else label

    def city_name_to_label(city: str) -> str:
        country = CITIES[city]["country"]
        return f"{country} — {city}"

    # ── Trip inputs ────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        origin_label = st.selectbox(
            "Flying / travelling from",
            CITY_OPTIONS,
            index=CITY_OPTIONS.index(city_name_to_label("Prague")),
        )
        origin = city_label_to_name(origin_label)
    with c2:
        destination_label = st.selectbox(
            "Final destination",
            CITY_OPTIONS,
            index=CITY_OPTIONS.index(city_name_to_label("London")),
        )
        destination = city_label_to_name(destination_label)

    c3, c4 = st.columns(2)
    with c3:
        month_name = st.selectbox("Month of travel", list(MONTH_NAMES.values()),
                                  index=5)  # June default
    with c4:
        days = st.slider("Days available", min_value=1, max_value=10, value=3)

    travel_month = next(k for k, v in MONTH_NAMES.items() if v == month_name)

    if origin == destination:
        st.warning("Origin and destination can't be the same city.")
        st.stop()

    st.markdown("<div style='height:.25rem'></div>", unsafe_allow_html=True)
    _, run_col, _ = st.columns([1, 2, 1])
    with run_col:
        run = st.button("Find my route →", use_container_width=True)

    # ── Results ────────────────────────────────────────────────────────────
    if run:
        with st.spinner("Building your route…"):
            try:
                result = optimise_route(
                    origin=origin, destination=destination,
                    days=days, traveler_scores=active_scores,
                    travel_month=travel_month,
                )
            except Exception as e:
                st.error(f"Couldn't build a route: {e}")
                st.stop()

        top_trait    = max(active_scores, key=active_scores.get)
        top_score    = active_scores[top_trait]
        waypoints    = result["waypoints"]

        # ── Opening narrative ─────────────────────────────────────────────
        type_label = st.session_state.traveler_type if has_profile and src == "My saved profile" else persona_name
        runner_up  = sorted(active_scores, key=active_scores.get, reverse=True)[1]

        narrative_opener = (
            f"Your route leans into your love of **{top_trait}** "
            f"(score {top_score:.1f}/5)"
        )
        if result["stops"]:
            narrative_opener += (
                f", with a strong secondary pull toward **{runner_up}**. "
                f"Every stop below was chosen because it delivers on both — not just geographically, "
                f"but in terms of what you'll actually do when you get there."
            )
        else:
            narrative_opener += ". Since efficiency matters most to you, the direct route wins."

        st.markdown(
            f'<p style="font-size:.9rem;color:#374151;line-height:1.65;margin-bottom:1rem">'
            f'{narrative_opener}</p>', unsafe_allow_html=True
        )

        # ── Feasibility warning ───────────────────────────────────────────
        if result.get("feasibility_warning"):
            st.markdown(f'<div class="warn-box">{result["feasibility_warning"]}</div>',
                        unsafe_allow_html=True)

        # ── Map ───────────────────────────────────────────────────────────
        lats = [CITIES[c]["lat"] for c in waypoints]
        lons = [CITIES[c]["lon"] for c in waypoints]

        fig_map = go.Figure()
        fig_map.add_trace(go.Scattergeo(
            lat=lats, lon=lons, mode="lines",
            line=dict(width=2.5, color="#1375f0", dash="dot"),
            hoverinfo="skip",
        ))
        labels = []
        for i, c in enumerate(waypoints):
            if i == 0:             labels.append(f"🛫 {c}")
            elif i == len(waypoints)-1: labels.append(f"🛬 {c}")
            else:                  labels.append(f"📍 {c}")

        fig_map.add_trace(go.Scattergeo(
            lat=lats, lon=lons, mode="markers+text",
            marker=dict(size=11, color="#1375f0",
                        line=dict(width=2, color="white")),
            text=labels, textposition="top center",
            textfont=dict(size=11, color="#111827"),
            hovertemplate="<b>%{text}</b><extra></extra>",
        ))
        lat_pad = max((max(lats)-min(lats))*0.45, 3)
        lon_pad = max((max(lons)-min(lons))*0.45, 3)
        fig_map.update_layout(
            geo=dict(
                scope="europe",
                showland=True, landcolor="#f1f5f9",
                showocean=True, oceancolor="#dbeafe",
                showcoastlines=True, coastlinecolor="#cbd5e1",
                showcountries=True, countrycolor="#e2e8f0",
                lataxis_range=[min(lats)-lat_pad, max(lats)+lat_pad],
                lonaxis_range=[min(lons)-lon_pad, max(lons)+lon_pad],
                bgcolor="#f8fafc",
            ),
            margin=dict(t=8, b=8, l=0, r=0),
            paper_bgcolor="#ffffff",
            showlegend=False, height=320,
        )
        st.markdown('<div class="card" style="padding:.75rem">', unsafe_allow_html=True)
        st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Stat pills ────────────────────────────────────────────────────
        cost    = result["cost"]
        n_stops = len(result["stops"])
        st.markdown(f"""
        <div class="stat-row">
          <div class="stat-pill">
            <div class="stat-label">Route</div>
            <div class="stat-val">{origin} → {destination}</div>
          </div>
          <div class="stat-pill">
            <div class="stat-label">Stopovers</div>
            <div class="stat-val">{n_stops} {"stop" if n_stops==1 else "stops"}</div>
          </div>
          <div class="stat-pill">
            <div class="stat-label">Distance</div>
            <div class="stat-val">{result["total_km"]:,} km</div>
          </div>
          <div class="stat-pill">
            <div class="stat-label">Est. budget</div>
            <div class="stat-val">€{cost["low"]:,} – €{cost["high"]:,}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── Transport tip ─────────────────────────────────────────────────
        st.markdown(f'<div class="tip-box">{result["transport_tip"]}</div>',
                    unsafe_allow_html=True)

        # ── Direct route ──────────────────────────────────────────────────
        if result["direct"]:
            st.markdown(f"""
            <div class="direct-box">
              <strong style="font-size:.9rem">✅ Direct route recommended</strong>
              <p style="font-size:.84rem;color:#374151;margin-top:.4rem">
                {result["direct_reason"]}
              </p>
            </div>""", unsafe_allow_html=True)

        # ── Stop cards ────────────────────────────────────────────────────
        else:
            st.markdown("#### Your stops")

            # Origin
            st.markdown(f"""
            <div class="stop-card" style="border-left-color:#9ca3af">
              <div class="stop-city">🛫 {origin}</div>
              <div class="stop-meta">{CITIES[origin]["country"]} · Departure point</div>
            </div>""", unsafe_allow_html=True)

            for stop in result["stops"]:
                events_html = "".join(
                    f'<span class="stop-event">🎟 {ev}</span>'
                    for ev in stop["events"]
                )
                tier_html = f'<span class="stop-tier">{stop["price_tier"]} per day</span>'
                hl = " · ".join(stop["highlights"])
                st.markdown(f"""
                <div class="stop-card">
                  <div class="stop-city">📍 {stop["city"]}</div>
                  <div class="stop-meta">{stop["country"]} {tier_html}</div>
                  <div class="stop-why">{stop["why"]}</div>
                  <div class="stop-hl">✦ {hl}</div>
                  {events_html}
                </div>""", unsafe_allow_html=True)

            # Destination
            st.markdown(f"""
            <div class="stop-card" style="border-left-color:var(--green)">
              <div class="stop-city">🛬 {destination}</div>
              <div class="stop-meta">{CITIES[destination]["country"]} · Final destination</div>
            </div>""", unsafe_allow_html=True)

        # ── Day-by-day itinerary ──────────────────────────────────────────
        with st.expander("📅  Day-by-day itinerary", expanded=True):
            itinerary = result.get("itinerary", [])
            if itinerary:
                tl_html = '<div class="timeline">'
                for item in itinerary:
                    cls  = "tl-travel" if item["type"] == "travel" else "tl-item"
                    tl_html += f"""
                    <div class="tl-item {cls}">
                      <div class="tl-day">Day {item["day"]}</div>
                      <div class="tl-head">{item["headline"]}</div>
                      <div class="tl-detail">{item["detail"]}</div>
                    </div>"""
                tl_html += "</div>"
                st.markdown(tl_html, unsafe_allow_html=True)
            else:
                st.caption("No itinerary available for this route.")

        # ── Budget breakdown ──────────────────────────────────────────────
        with st.expander("💶  Budget breakdown"):
            if cost["breakdown"]:
                rows = "".join(f"""
                <div style="display:flex;justify-content:space-between;padding:.4rem 0;
                             border-bottom:1px solid #f3f4f6;font-size:.85rem">
                  <span><strong>{b['city']}</strong> · {b['tier']} · {b['days']} day{'s' if b['days']!=1 else ''}</span>
                  <span style="font-weight:600">~€{b['est']:,}</span>
                </div>""" for b in cost["breakdown"])
                total_row = f"""
                <div style="display:flex;justify-content:space-between;padding:.6rem 0 0;
                             font-size:.9rem;font-weight:700;color:var(--text)">
                  <span>Total estimate</span>
                  <span>€{cost["low"]:,} – €{cost["high"]:,}</span>
                </div>"""
                st.markdown(
                    f'<div style="padding:.5rem 0">{rows}{total_row}'
                    f'<p style="font-size:.75rem;color:var(--muted);margin-top:.6rem">'
                    f'Includes mid-range accommodation, meals, and activities. '
                    f'Excludes flights and transport between cities.</p></div>',
                    unsafe_allow_html=True
                )

        # ── Share / download ──────────────────────────────────────────────
        st.markdown("<div style='height:.25rem'></div>", unsafe_allow_html=True)
        c_share, c_json = st.columns(2)
        with c_share:
            share_html = generate_share_html(
                result, active_scores,
                st.session_state.traveler_type if has_profile and src == "My saved profile" else persona_name,
                st.session_state.traveler_desc if has_profile and src == "My saved profile" else ""
            )
            st.download_button(
                "📤  Share this route (HTML)",
                data=share_html,
                file_name=f"ravel_{origin.lower()}_to_{destination.lower()}.html",
                mime="text/html",
                use_container_width=True,
            )
        with c_json:
            export = {
                "route": result["waypoints"],
                "month": result["month"],
                "days":  days,
                "stops": [{"city":s["city"],"why":s["why"],"events":s["events"]}
                          for s in result["stops"]],
                "cost_estimate_eur": {"low":cost["low"],"high":cost["high"]},
                "transport_tip": result["transport_tip"],
            }
            st.download_button(
                "⬇  Download route (JSON)",
                data=json.dumps(export, indent=2),
                file_name=f"ravel_route_{origin.lower()}_{destination.lower()}.json",
                mime="application/json",
                use_container_width=True,
            )

        # ── Phase 2 teaser ────────────────────────────────────────────────
        st.markdown("""
        <div style="margin-top:1.5rem;background:#fff;border:1.5px dashed #e5e7eb;
                    border-radius:var(--radius);padding:1.3rem 1.6rem">
          <div style="font-size:.7rem;font-weight:700;text-transform:uppercase;
                      letter-spacing:.1em;color:var(--muted);margin-bottom:.65rem">
            What's coming in Ravel v2
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:.75rem">
            <div style="font-size:.83rem;color:#374151;line-height:1.5">
              🏨 <strong>Hotel matching</strong><br>
              <span style="color:var(--muted)">Boutique, budget, or luxury picks — filtered to your profile and price tier</span>
            </div>
            <div style="font-size:.83rem;color:#374151;line-height:1.5">
              🚇 <strong>Intra-city navigation</strong><br>
              <span style="color:var(--muted)">"Take the 2 train (€2.35) — 0.25mi walk to the Louvre, great bistro next door"</span>
            </div>
            <div style="font-size:.83rem;color:#374151;line-height:1.5">
              🍽️ <strong>Restaurant recommendations</strong><br>
              <span style="color:var(--muted)">Curated dining near every stop, matched to your Food score</span>
            </div>
            <div style="font-size:.83rem;color:#374151;line-height:1.5">
              🤝 <strong>Group route blending</strong><br>
              <span style="color:var(--muted)">Combine profiles from multiple travellers into one optimised shared route</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
