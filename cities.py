"""
Ravel city database — Europe.

Each city carries:
  lat / lon           Geographic centre
  traits              Scores 1–5 across the 6 Ravel dimensions
  price_tier          €  <€100/day  |  €€  €100–180  |  €€€  >€180
  daily_budget_eur    Mid-range all-in daily spend (hotel + meals + activities)
  narrative           2–3 sentences of warm, specific copy
  highlights          Top 3 things — used in itinerary cards
  events              Monthly events with matching trait tags
"""

CITIES = {

    # ── UK ──────────────────────────────────────────────────────────────────
    "London": {
        "country": "UK", "lat": 51.5074, "lon": -0.1278,
        "price_tier": "€€€", "daily_budget_eur": 230,
        "traits": {"Adventure":2.5,"Budget":1.5,"Culture":5.0,"Relaxation":2.5,"Food":4.5,"Shopping":5.0},
        "narrative": "The city that somehow contains every city inside it. From Borough Market at dawn to jazz in a Soho basement at midnight, London refuses to be one thing — which is exactly why it rewards every type of traveller.",
        "highlights": ["Borough Market & Southbank", "British Museum free collection", "Shoreditch street art + Brick Lane"],
        "events": [
            {"name": "Wimbledon",            "months": [6,7],    "tags": ["Adventure"]},
            {"name": "Notting Hill Carnival", "months": [8],     "tags": ["Culture","Food"]},
            {"name": "London Fashion Week",   "months": [2,9],   "tags": ["Shopping","Culture"]},
            {"name": "Chelsea Flower Show",   "months": [5],     "tags": ["Relaxation","Culture"]},
        ],
    },
    "Edinburgh": {
        "country": "UK", "lat": 55.9533, "lon": -3.1883,
        "price_tier": "€€", "daily_budget_eur": 145,
        "traits": {"Adventure":4.0,"Budget":3.0,"Culture":4.5,"Relaxation":3.0,"Food":3.5,"Shopping":3.0},
        "narrative": "Few cities wear their drama as openly as Edinburgh — a medieval castle perched on volcanic rock, whisky bars carved into cliff faces, and a coastline ten minutes from the centre. August turns the whole city into the world's biggest arts festival.",
        "highlights": ["Edinburgh Castle & Royal Mile", "Arthur's Seat sunrise hike", "Scotch whisky tasting in the Old Town"],
        "events": [
            {"name": "Edinburgh Festival Fringe", "months": [8], "tags": ["Culture","Adventure"]},
            {"name": "Hogmanay (New Year)", "months": [12,1], "tags": ["Culture","Food"]},
            {"name": "Edinburgh Marathon", "months": [5], "tags": ["Adventure"]},
        ],
    },

    # ── Ireland ─────────────────────────────────────────────────────────────
    "Dublin": {
        "country": "Ireland", "lat": 53.3498, "lon": -6.2603,
        "price_tier": "€€", "daily_budget_eur": 155,
        "traits": {"Adventure":3.0,"Budget":2.5,"Culture":4.0,"Relaxation":3.0,"Food":4.0,"Shopping":3.5},
        "narrative": "Smaller and more human-scaled than most capitals, Dublin rewards slow walking and long evenings. The pub is the living room here — order a Guinness and within twenty minutes you'll have heard someone's life story.",
        "highlights": ["Trinity College & Book of Kells", "Temple Bar & live trad music", "Grafton Street morning coffee"],
        "events": [
            {"name": "St. Patrick's Festival", "months": [3], "tags": ["Culture","Food"]},
            {"name": "Dublin Fringe Festival",  "months": [9], "tags": ["Culture"]},
        ],
    },

    # ── France ──────────────────────────────────────────────────────────────
    "Paris": {
        "country": "France", "lat": 48.8566, "lon": 2.3522,
        "price_tier": "€€€", "daily_budget_eur": 210,
        "traits": {"Adventure":2.0,"Budget":2.0,"Culture":5.0,"Relaxation":3.5,"Food":5.0,"Shopping":5.0},
        "narrative": "The city that set the bar for romance, culture, and cuisine — and hasn't stopped raising it since. Every arrondissement has its own obsession: art in the Marais, fashion on Saint-Germain, perfect coffee in a cave-like bistro you'll only find by getting lost.",
        "highlights": ["Louvre & the Marais neighbourhood", "Marché d'Aligre early morning", "Seine walk at dusk"],
        "events": [
            {"name": "Roland Garros (French Open)", "months": [5,6],    "tags": ["Adventure"]},
            {"name": "Paris Fashion Week",           "months": [3,9,10], "tags": ["Shopping","Culture"]},
            {"name": "Fête de la Musique",           "months": [6],     "tags": ["Culture","Food"]},
            {"name": "Paris Jazz Festival",          "months": [7],     "tags": ["Culture","Relaxation"]},
            {"name": "Nuit Blanche (art all night)", "months": [10],    "tags": ["Culture","Adventure"]},
        ],
    },
    "Lyon": {
        "country": "France", "lat": 45.7640, "lon": 4.8357,
        "price_tier": "€€", "daily_budget_eur": 120,
        "traits": {"Adventure":2.5,"Budget":3.0,"Culture":3.5,"Relaxation":3.0,"Food":5.0,"Shopping":3.0},
        "narrative": "Lyon is where France keeps its best food and pretends not to show off. Paul Bocuse shaped this city, and his influence is everywhere — in the bouchons, the covered markets, the reverence for a properly made quenelle.",
        "highlights": ["Les Halles de Lyon-Paul Bocuse", "Vieux-Lyon UNESCO traboules", "Croix-Rousse silk-workers quarter"],
        "events": [
            {"name": "Fête des Lumières (Festival of Lights)", "months": [12],  "tags": ["Culture"]},
            {"name": "Nuits de Fourvière Festival",            "months": [6,7], "tags": ["Culture"]},
            {"name": "Bocuse d'Or culinary competition",       "months": [1],   "tags": ["Food"]},
        ],
    },
    "Nice": {
        "country": "France", "lat": 43.7102, "lon": 7.2620,
        "price_tier": "€€", "daily_budget_eur": 140,
        "traits": {"Adventure":3.5,"Budget":2.5,"Culture":3.5,"Relaxation":5.0,"Food":4.5,"Shopping":3.5},
        "narrative": "The Promenade des Anglais was built so the English aristocracy could stroll in the winter sun — the instinct was right. Nice sits at the intersection of French sophistication and Mediterranean ease, with one of Europe's great old towns a ten-minute walk from the beach.",
        "highlights": ["Cours Saleya flower & food market", "Castle Hill panorama at sunset", "Promenade des Anglais morning run"],
        "events": [
            {"name": "Nice Carnival",          "months": [2,3], "tags": ["Culture","Adventure"]},
            {"name": "Nice Jazz Festival",     "months": [7],   "tags": ["Culture","Relaxation"]},
            {"name": "Cannes Film Festival",   "months": [5],   "tags": ["Culture","Shopping"]},
        ],
    },

    # ── Spain ────────────────────────────────────────────────────────────────
    "Barcelona": {
        "country": "Spain", "lat": 41.3851, "lon": 2.1734,
        "price_tier": "€€", "daily_budget_eur": 130,
        "traits": {"Adventure":4.0,"Budget":3.0,"Culture":4.5,"Relaxation":4.0,"Food":5.0,"Shopping":4.0},
        "narrative": "Europe's most kinetic city. The Gaudí architecture is alive in a way that marble museums never are, the beach is a fifteen-minute walk from the Gothic Quarter, and on match day the whole city breathes together as one.",
        "highlights": ["Sagrada Família & Park Güell", "La Boqueria + El Born neighbourhood", "Barceloneta beach at golden hour"],
        "events": [
            {"name": "FC Barcelona home match",  "months": [1,2,3,4,5,9,10,11,12], "tags": ["Adventure"]},
            {"name": "Primavera Sound Festival", "months": [6],  "tags": ["Culture","Adventure"]},
            {"name": "Sónar Festival",           "months": [6],  "tags": ["Culture","Adventure"]},
            {"name": "La Mercè street festival", "months": [9],  "tags": ["Culture","Food"]},
        ],
    },
    "Madrid": {
        "country": "Spain", "lat": 40.4168, "lon": -3.7038,
        "price_tier": "€€", "daily_budget_eur": 120,
        "traits": {"Adventure":3.5,"Budget":3.0,"Culture":4.5,"Relaxation":3.0,"Food":4.5,"Shopping":4.0},
        "narrative": "Madrid doesn't do subtle. The Prado houses one of the world's greatest art collections, the nightlife doesn't start until midnight, and the tapas culture means dinner is not an event — it's a three-hour negotiation with the best bars on the street.",
        "highlights": ["Prado & Reina Sofía museums", "Mercado de San Miguel tapas", "Retiro Park Sunday morning"],
        "events": [
            {"name": "Real Madrid home match",  "months": [1,2,3,4,5,9,10,11,12], "tags": ["Adventure"]},
            {"name": "Madrid Carnival",         "months": [2,3], "tags": ["Culture"]},
            {"name": "San Isidro Fiestas",      "months": [5],   "tags": ["Culture","Food"]},
            {"name": "Madrid Fusión (gastronomy summit)", "months": [1], "tags": ["Food"]},
        ],
    },
    "Seville": {
        "country": "Spain", "lat": 37.3891, "lon": -5.9845,
        "price_tier": "€", "daily_budget_eur": 95,
        "traits": {"Adventure":3.5,"Budget":4.0,"Culture":5.0,"Relaxation":3.5,"Food":4.5,"Shopping":3.5},
        "narrative": "The most theatrical city in Spain — flamenco wasn't invented here but it reached its peak here, and the streets of Triana still pulse with it on warm nights. Seville in April during Semana Santa is an experience for which there is no adequate comparison.",
        "highlights": ["Real Alcázar palace gardens", "Barrio Santa Cruz narrow streets", "Triana flamenco bars after dark"],
        "events": [
            {"name": "Semana Santa (Holy Week)",   "months": [3,4], "tags": ["Culture"]},
            {"name": "Feria de Abril",             "months": [4,5], "tags": ["Culture","Food","Adventure"]},
            {"name": "Seville European Film Festival", "months": [11], "tags": ["Culture"]},
        ],
    },
    "Bilbao": {
        "country": "Spain", "lat": 43.2627, "lon": -2.9253,
        "price_tier": "€€", "daily_budget_eur": 110,
        "traits": {"Adventure":3.5,"Budget":3.0,"Culture":4.5,"Relaxation":3.0,"Food":5.0,"Shopping":3.0},
        "narrative": "The Guggenheim put Bilbao on the map, but the pintxos scene is what makes people come back. The Basque Country has the highest concentration of Michelin stars in the world — even the neighbourhood bars treat food as a serious art form.",
        "highlights": ["Guggenheim Museum Bilbao", "Casco Viejo pintxos crawl", "San Mamés Stadium (Athletic Bilbao)"],
        "events": [
            {"name": "Aste Nagusia (Great Week festival)", "months": [8], "tags": ["Culture","Food","Adventure"]},
            {"name": "Athletic Bilbao home match",         "months": [1,2,3,4,5,9,10,11,12], "tags": ["Adventure"]},
        ],
    },

    # ── Portugal ─────────────────────────────────────────────────────────────
    "Lisbon": {
        "country": "Portugal", "lat": 38.7169, "lon": -9.1395,
        "price_tier": "€", "daily_budget_eur": 95,
        "traits": {"Adventure":3.5,"Budget":4.0,"Culture":4.0,"Relaxation":4.0,"Food":4.5,"Shopping":3.5},
        "narrative": "Lisbon does nostalgia better than anywhere in Europe — fado spills out of tiled doorways, trams clang up hills that shouldn't support trams, and the whole city smells faintly of salt and pastéis de nata. It's also genuinely affordable, which feels almost illegal for a capital this beautiful.",
        "highlights": ["Alfama tram ride & miradouros", "LX Factory Sunday market", "Pastéis de Belém at the original bakery"],
        "events": [
            {"name": "NOS Alive Music Festival",  "months": [7],   "tags": ["Culture","Adventure"]},
            {"name": "Festas de Lisboa (sardine season)", "months": [6], "tags": ["Culture","Food"]},
            {"name": "Web Summit",                "months": [11],  "tags": ["Culture"]},
        ],
    },
    "Porto": {
        "country": "Portugal", "lat": 41.1579, "lon": -8.6291,
        "price_tier": "€", "daily_budget_eur": 85,
        "traits": {"Adventure":3.5,"Budget":4.5,"Culture":4.0,"Relaxation":4.0,"Food":4.5,"Shopping":3.5},
        "narrative": "Porto is what happens when a city is too proud to chase trends. The azulejo-tiled facades, the port wine lodges across the Douro, the covered market spilling onto the street — it all feels genuinely lived-in, not curated for visitors. One of Europe's best-value cities, full stop.",
        "highlights": ["Ribeira waterfront & Dom Luís bridge", "Port wine tasting in Vila Nova de Gaia", "Livraria Lello bookshop"],
        "events": [
            {"name": "NOS Primavera Sound",   "months": [6],   "tags": ["Culture","Adventure"]},
            {"name": "São João Festival",     "months": [6],   "tags": ["Culture","Food"]},
            {"name": "Porto Wine Fest",       "months": [6],   "tags": ["Food","Relaxation"]},
        ],
    },

    # ── Netherlands ──────────────────────────────────────────────────────────
    "Amsterdam": {
        "country": "Netherlands", "lat": 52.3676, "lon": 4.9041,
        "price_tier": "€€", "daily_budget_eur": 155,
        "traits": {"Adventure":3.0,"Budget":2.5,"Culture":4.5,"Relaxation":3.5,"Food":3.5,"Shopping":4.0},
        "narrative": "Effortlessly cool without trying. The canal ring is one of the most elegant urban grids ever built, the Rijksmuseum is genuinely overwhelming, and once you're on a bike weaving through traffic you understand why Amsterdammers pity everyone who isn't.",
        "highlights": ["Rijksmuseum & Van Gogh Museum", "Canal boat at golden hour", "Jordaan neighbourhood antique markets"],
        "events": [
            {"name": "King's Day",            "months": [4],    "tags": ["Culture","Food"]},
            {"name": "Amsterdam Dance Event", "months": [10],   "tags": ["Adventure","Culture"]},
            {"name": "Tulip Season / Keukenhof", "months": [4,5], "tags": ["Relaxation","Culture"]},
            {"name": "International Documentary Film Festival", "months": [11], "tags": ["Culture"]},
        ],
    },

    # ── Belgium ──────────────────────────────────────────────────────────────
    "Brussels": {
        "country": "Belgium", "lat": 50.8503, "lon": 4.3517,
        "price_tier": "€€", "daily_budget_eur": 125,
        "traits": {"Adventure":2.0,"Budget":3.0,"Culture":4.0,"Relaxation":3.0,"Food":4.5,"Shopping":3.5},
        "narrative": "Brussels is perpetually underestimated, which suits it fine. Behind the EU buildings is a city that invented surrealism, makes the world's best beer and chocolate, and has an Art Nouveau architectural trail that puts Vienna's to shame.",
        "highlights": ["Grand Place & Galeries Royales St-Hubert", "Marolles flea market Saturday morning", "Cantillon brewery & lambic tasting"],
        "events": [
            {"name": "Brussels Jazz Weekend",  "months": [5],  "tags": ["Culture","Relaxation"]},
            {"name": "Ommegang Pageant",        "months": [7],  "tags": ["Culture"]},
            {"name": "Brussels Flower Carpet",  "months": [8],  "tags": ["Culture","Relaxation"]},
            {"name": "Belgian Beer Weekend",    "months": [9],  "tags": ["Food","Culture"]},
        ],
    },
    "Bruges": {
        "country": "Belgium", "lat": 51.2093, "lon": 3.2247,
        "price_tier": "€€", "daily_budget_eur": 130,
        "traits": {"Adventure":2.0,"Budget":2.5,"Culture":4.5,"Relaxation":5.0,"Food":4.0,"Shopping":3.5},
        "narrative": "Bruges is almost absurdly well-preserved — a medieval Flemish trading city that simply stopped growing in the 15th century and has been beautiful ever since. Walk the canals at 7am before the day-trippers arrive and you'll understand why painters kept coming back.",
        "highlights": ["Canal walk at sunrise", "Groeninge Museum Flemish primitives", "Chocolate & lace shops in the centre"],
        "events": [
            {"name": "Procession of the Holy Blood", "months": [5], "tags": ["Culture"]},
            {"name": "Bruges Beer Festival",         "months": [2], "tags": ["Food","Culture"]},
        ],
    },

    # ── Germany ──────────────────────────────────────────────────────────────
    "Berlin": {
        "country": "Germany", "lat": 52.5200, "lon": 13.4050,
        "price_tier": "€€", "daily_budget_eur": 115,
        "traits": {"Adventure":3.5,"Budget":3.5,"Culture":4.5,"Relaxation":2.5,"Food":3.5,"Shopping":3.5},
        "narrative": "Berlin has more museums than rainy days, a club scene that other cities stopped trying to compete with, and an energy that comes from being permanently, deliberately unfinished. The city still feels like it's deciding what it wants to be — which is precisely what makes it compelling.",
        "highlights": ["East Side Gallery & Checkpoint Charlie", "Pergamon Museum", "Markthalle Neun street food Thursday"],
        "events": [
            {"name": "Berlinale (International Film Festival)", "months": [2],    "tags": ["Culture"]},
            {"name": "Berlin Marathon",                        "months": [9],    "tags": ["Adventure"]},
            {"name": "Berlin Art Week",                        "months": [9],    "tags": ["Culture","Shopping"]},
            {"name": "CTM Festival (experimental music)",      "months": [1,2],  "tags": ["Culture","Adventure"]},
        ],
    },
    "Munich": {
        "country": "Germany", "lat": 48.1351, "lon": 11.5820,
        "price_tier": "€€", "daily_budget_eur": 140,
        "traits": {"Adventure":3.5,"Budget":2.5,"Culture":3.5,"Relaxation":3.5,"Food":4.5,"Shopping":3.5},
        "narrative": "Munich has resolved the tension between tradition and modernity better than anywhere in Germany. The English Garden is the city's living room — 3.7 km² where surfers ride a standing wave in the Eisbach and office workers eat pretzels in beer gardens at lunchtime.",
        "highlights": ["English Garden & Eisbach surfers", "Viktualienmarkt gourmet food market", "Deutsches Museum science collection"],
        "events": [
            {"name": "Oktoberfest",               "months": [9,10], "tags": ["Culture","Food","Adventure"]},
            {"name": "Tollwood Summer Festival",  "months": [6,7],  "tags": ["Culture","Food"]},
            {"name": "Starkbierfest (strong beer festival)", "months": [3], "tags": ["Food","Culture"]},
        ],
    },
    "Frankfurt": {
        "country": "Germany", "lat": 50.1109, "lon": 8.6821,
        "price_tier": "€€", "daily_budget_eur": 130,
        "traits": {"Adventure":2.0,"Budget":2.5,"Culture":3.5,"Relaxation":2.5,"Food":3.5,"Shopping":3.5},
        "narrative": "Frankfurt is a transit city that consistently undersells itself. The Städel is one of Europe's finest art museums, the Sachsenhausen cider district is genuinely charming, and the skyline — Europe's most American-looking — is striking at night from the river.",
        "highlights": ["Städel Museum collection", "Sachsenhausen Ebbelwei (cider) district", "Römerberg Old Town"],
        "events": [
            {"name": "Frankfurt Book Fair",  "months": [10], "tags": ["Culture"]},
            {"name": "Museumsuferfest",      "months": [8],  "tags": ["Culture","Food"]},
            {"name": "Frankfurt Christmas Market", "months": [12], "tags": ["Culture","Shopping"]},
        ],
    },

    # ── Austria ──────────────────────────────────────────────────────────────
    "Vienna": {
        "country": "Austria", "lat": 48.2082, "lon": 16.3738,
        "price_tier": "€€", "daily_budget_eur": 145,
        "traits": {"Adventure":2.0,"Budget":2.5,"Culture":5.0,"Relaxation":4.5,"Food":4.0,"Shopping":3.5},
        "narrative": "Vienna spent three centuries as the cultural capital of Europe and still acts the part. The museums here aren't just good — they're staggering. Sitting in Café Central with a Melange and a newspaper for three hours isn't laziness; it's the local sport, and it's protected by UNESCO.",
        "highlights": ["Kunsthistorisches Museum", "Café Central & Naschmarkt", "Belvedere Palace & Klimt's The Kiss"],
        "events": [
            {"name": "Vienna Opera Ball",           "months": [2],    "tags": ["Culture","Shopping"]},
            {"name": "Vienna City Marathon",        "months": [4],    "tags": ["Adventure"]},
            {"name": "Donauinselfest (free music)", "months": [6],    "tags": ["Culture","Food"]},
            {"name": "Vienna Film Festival",        "months": [10,11],"tags": ["Culture"]},
        ],
    },

    # ── Czech Republic ───────────────────────────────────────────────────────
    "Prague": {
        "country": "Czech Republic", "lat": 50.0755, "lon": 14.4378,
        "price_tier": "€", "daily_budget_eur": 80,
        "traits": {"Adventure":3.0,"Budget":4.5,"Culture":4.5,"Relaxation":3.5,"Food":3.5,"Shopping":3.0},
        "narrative": "Prague is the city central casting would design if you asked for 'medieval European capital' — but the real thing is better than any set. Cross Charles Bridge at 6am, look back at the castle, and try not to feel something. The beer is world-class and costs less than water.",
        "highlights": ["Charles Bridge & Prague Castle at dawn", "Old Town Square Astronomical Clock", "Lokál beer hall for tank-fresh Pilsner Urquell"],
        "events": [
            {"name": "Prague Spring Music Festival", "months": [5],    "tags": ["Culture"]},
            {"name": "Signal Festival (light art)",  "months": [10],   "tags": ["Culture","Adventure"]},
            {"name": "Prague Christmas Markets",     "months": [12],   "tags": ["Culture","Shopping"]},
        ],
    },

    # ── Hungary ──────────────────────────────────────────────────────────────
    "Budapest": {
        "country": "Hungary", "lat": 47.4979, "lon": 19.0402,
        "price_tier": "€", "daily_budget_eur": 75,
        "traits": {"Adventure":3.5,"Budget":4.5,"Culture":4.0,"Relaxation":5.0,"Food":4.0,"Shopping":3.0},
        "narrative": "Prague's more relaxed, more affordable cousin — and arguably more beautiful. Soak in a thermal bath built by the Ottomans, drink natural wine in a ruin bar that occupies an entire crumbling Jewish Quarter block, then watch the Danube go gold from the Chain Bridge.",
        "highlights": ["Széchenyi or Gellért thermal baths", "Ruin bars in the Jewish Quarter", "Fisherman's Bastion at sunset"],
        "events": [
            {"name": "Sziget Festival",          "months": [8],    "tags": ["Adventure","Culture"]},
            {"name": "Budapest Spring Festival", "months": [4],    "tags": ["Culture"]},
            {"name": "Budapest Wine Festival",   "months": [9],    "tags": ["Food","Relaxation"]},
        ],
    },

    # ── Poland ───────────────────────────────────────────────────────────────
    "Krakow": {
        "country": "Poland", "lat": 50.0647, "lon": 19.9450,
        "price_tier": "€", "daily_budget_eur": 65,
        "traits": {"Adventure":3.0,"Budget":5.0,"Culture":4.5,"Relaxation":3.0,"Food":3.5,"Shopping":3.0},
        "narrative": "One of Europe's great surprise packages. Krakow has a medieval centre that rivals Prague, a Jewish Quarter (Kazimierz) that has become one of the coolest neighbourhoods on the continent, and a daily budget that makes everywhere else feel expensive by comparison.",
        "highlights": ["Wawel Castle & cathedral", "Kazimierz Jewish Quarter bars & galleries", "Milk bar (bar mleczny) traditional Polish lunch"],
        "events": [
            {"name": "Krakow Film Festival",   "months": [5,6], "tags": ["Culture"]},
            {"name": "Wianki Midsummer",       "months": [6],   "tags": ["Culture","Adventure"]},
            {"name": "Jewish Culture Festival","months": [6,7], "tags": ["Culture","Food"]},
        ],
    },

    # ── Estonia ──────────────────────────────────────────────────────────────
    "Tallinn": {
        "country": "Estonia", "lat": 59.4370, "lon": 24.7536,
        "price_tier": "€", "daily_budget_eur": 70,
        "traits": {"Adventure":3.5,"Budget":4.5,"Culture":4.5,"Relaxation":3.0,"Food":3.5,"Shopping":3.0},
        "narrative": "Tallinn's Old Town is the best-preserved medieval city centre in Northern Europe, full stop. It hasn't been rebuilt or prettified — it's just survived, and walking its limestone streets feels genuinely different from anywhere further west.",
        "highlights": ["Old Town medieval walls & towers", "Telliskivi creative quarter", "Kadriorg Park & KUMU art museum"],
        "events": [
            {"name": "Tallinn Music Week",      "months": [4],  "tags": ["Culture","Adventure"]},
            {"name": "Black Nights Film Festival", "months": [11,12], "tags": ["Culture"]},
            {"name": "Old Town Days",           "months": [6],  "tags": ["Culture","Adventure"]},
        ],
    },

    # ── Switzerland ──────────────────────────────────────────────────────────
    "Zurich": {
        "country": "Switzerland", "lat": 47.3769, "lon": 8.5417,
        "price_tier": "€€€", "daily_budget_eur": 260,
        "traits": {"Adventure":3.5,"Budget":1.0,"Culture":3.5,"Relaxation":4.5,"Food":3.5,"Shopping":4.5},
        "narrative": "Zurich is expensive in the way that things designed to last are expensive. The lake is swimmable in summer, the trains run to the second, and the Bahnhofstrasse shopping strip is as good as anything in Milan or Paris. Come with a budget that won't give you anxiety.",
        "highlights": ["Lake Zurich swimming in summer", "Kunsthaus Museum (Monet, Giacometti, Warhol)", "Bahnhofstrasse & Old Town Niederdorf"],
        "events": [
            {"name": "Street Parade (techno festival)", "months": [8],   "tags": ["Adventure","Culture"]},
            {"name": "Zurich Film Festival",            "months": [9],   "tags": ["Culture"]},
            {"name": "Art Basel Zurich",                "months": [6],   "tags": ["Culture","Shopping"]},
        ],
    },

    # ── Italy ────────────────────────────────────────────────────────────────
    "Rome": {
        "country": "Italy", "lat": 41.9028, "lon": 12.4964,
        "price_tier": "€€", "daily_budget_eur": 140,
        "traits": {"Adventure":2.5,"Budget":2.5,"Culture":5.0,"Relaxation":3.5,"Food":5.0,"Shopping":4.0},
        "narrative": "Every street in Rome is stratigraphy — Ancient, Medieval, Baroque, and mid-century Fiat traffic layered on top of each other. You can have a coffee at a bar built on a forum where Caesar walked, and pay €1.20 for it. There is no city on earth more casually extraordinary.",
        "highlights": ["Colosseum & Roman Forum at opening time", "Vatican Museums & Sistine Chapel", "Trastevere neighbourhood dinner"],
        "events": [
            {"name": "Rome Marathon",           "months": [3],    "tags": ["Adventure"]},
            {"name": "Estate Romana (outdoor arts)", "months": [6,7,8], "tags": ["Culture","Relaxation"]},
            {"name": "Roma Incontra il Mondo (world music festival)", "months": [7], "tags": ["Culture"]},
        ],
    },
    "Florence": {
        "country": "Italy", "lat": 43.7696, "lon": 11.2558,
        "price_tier": "€€", "daily_budget_eur": 135,
        "traits": {"Adventure":2.0,"Budget":2.5,"Culture":5.0,"Relaxation":4.0,"Food":4.5,"Shopping":4.5},
        "narrative": "The Renaissance happened here, and Florence has been generously sharing the spoils ever since. The Uffizi alone could occupy a week. But the best Florence is the one behind the Oltrarno — leather workshops, natural wine bars, artisan cheese shops operated by the same families for four generations.",
        "highlights": ["Uffizi Gallery & Piazzale Michelangelo at dusk", "Oltrarno artisan workshops", "Mercato Centrale + Trattoria lunch"],
        "events": [
            {"name": "Calcio Storico (historic football)", "months": [6],    "tags": ["Adventure","Culture"]},
            {"name": "Florence Biennale",                  "months": [10],   "tags": ["Culture","Shopping"]},
            {"name": "Maggio Musicale Fiorentino",         "months": [4,5,6],"tags": ["Culture"]},
        ],
    },
    "Milan": {
        "country": "Italy", "lat": 45.4654, "lon": 9.1859,
        "price_tier": "€€€", "daily_budget_eur": 180,
        "traits": {"Adventure":2.0,"Budget":2.0,"Culture":4.0,"Relaxation":2.5,"Food":4.5,"Shopping":5.0},
        "narrative": "Milan runs on ambition. The Duomo is overwhelming, La Scala is unrivalled, and the Quadrilatero della Moda is where the fashion industry shows the world what it thinks beauty looks like this season. The aperitivo hour — Campari, free snacks, nobody in a hurry — is the city's gift to civilisation.",
        "highlights": ["Duomo rooftop at sunset", "Quadrilatero della Moda window shopping", "Navigli aperitivo hour"],
        "events": [
            {"name": "Milan Fashion Week",         "months": [2,3,9], "tags": ["Shopping","Culture"]},
            {"name": "Salone del Mobile (design)", "months": [4],     "tags": ["Culture","Shopping"]},
            {"name": "Milano Film Festival",       "months": [9],     "tags": ["Culture"]},
        ],
    },

    # ── Denmark ──────────────────────────────────────────────────────────────
    "Copenhagen": {
        "country": "Denmark", "lat": 55.6761, "lon": 12.5683,
        "price_tier": "€€€", "daily_budget_eur": 210,
        "traits": {"Adventure":3.0,"Budget":1.5,"Culture":4.0,"Relaxation":4.5,"Food":5.0,"Shopping":4.0},
        "narrative": "Copenhagen invented the way the world wants to live now: bikes everywhere, Nordic design, the best restaurants on the planet, a harbour you can swim in. It's expensive in the honest way — you pay more and you get more, and you leave wondering why everywhere else feels slightly wrong.",
        "highlights": ["Noma & New Nordic food scene", "Tivoli Gardens summer evenings", "Designmuseum Danmark & Nørreport neighbourhood"],
        "events": [
            {"name": "Copenhagen Jazz Festival",  "months": [7],    "tags": ["Culture","Relaxation"]},
            {"name": "Copenhagen Fashion Week",   "months": [2,8],  "tags": ["Shopping","Culture"]},
            {"name": "Copenhagen Cooking Festival","months": [8],   "tags": ["Food"]},
        ],
    },

    # ── Sweden ───────────────────────────────────────────────────────────────
    "Stockholm": {
        "country": "Sweden", "lat": 59.3293, "lon": 18.0686,
        "price_tier": "€€€", "daily_budget_eur": 195,
        "traits": {"Adventure":3.0,"Budget":1.5,"Culture":4.0,"Relaxation":4.0,"Food":4.0,"Shopping":4.0},
        "narrative": "Stockholm is built across 14 islands and almost every view has water in it. Gamla Stan is one of the best-preserved Old Towns in Scandinavia, the design culture is pervasive in the best way, and the archipelago — 30,000 islands accessible by ferry — is one of Europe's great natural escapes.",
        "highlights": ["Gamla Stan (Old Town) cobblestones", "Fotografiska contemporary photography museum", "Archipelago ferry day trip"],
        "events": [
            {"name": "Stockholm Jazz Festival", "months": [6],  "tags": ["Culture","Relaxation"]},
            {"name": "Way Out West Festival",   "months": [8],  "tags": ["Adventure","Culture"]},
        ],
    },

    # ── Greece ───────────────────────────────────────────────────────────────
    "Athens": {
        "country": "Greece", "lat": 37.9838, "lon": 23.7275,
        "price_tier": "€€", "daily_budget_eur": 110,
        "traits": {"Adventure":3.0,"Budget":3.5,"Culture":5.0,"Relaxation":3.5,"Food":4.5,"Shopping":3.5},
        "narrative": "Athens is the beginning of everything, and spending time here feels like getting the first chapter you always skipped. The Acropolis at sunrise, before the crowds, is one of the genuinely transcendent experiences available to a traveller in Europe. The food scene has quietly become one of the continent's best.",
        "highlights": ["Acropolis & Parthenon at opening time", "Monastiraki flea market", "Rooftop dinner with Acropolis view"],
        "events": [
            {"name": "Athens Epidaurus Festival (theatre & music)", "months": [6,7,8], "tags": ["Culture"]},
            {"name": "Athens Marathon",                             "months": [11],    "tags": ["Adventure"]},
            {"name": "Athens Street Food Festival",                "months": [5],     "tags": ["Food"]},
        ],
    },

    # ── Croatia ──────────────────────────────────────────────────────────────
    "Dubrovnik": {
        "country": "Croatia", "lat": 42.6507, "lon": 18.0944,
        "price_tier": "€€", "daily_budget_eur": 130,
        "traits": {"Adventure":4.0,"Budget":2.5,"Culture":4.5,"Relaxation":5.0,"Food":4.0,"Shopping":3.0},
        "narrative": "Dubrovnik is one of those places where you turn a corner and stop walking because the view is too good. The City Walls circuit at sunset, sea on one side and terracotta rooftops on the other, is a 2km argument that beauty is worth going slightly out of your way for.",
        "highlights": ["City Walls sunset walk", "Sea kayaking around the Old Town", "Lokrum Island day trip"],
        "events": [
            {"name": "Dubrovnik Summer Festival", "months": [7,8], "tags": ["Culture","Relaxation"]},
            {"name": "Good Food Festival",        "months": [10],  "tags": ["Food","Culture"]},
        ],
    },

    # ── Slovenia ─────────────────────────────────────────────────────────────
    "Ljubljana": {
        "country": "Slovenia", "lat": 46.0569, "lon": 14.5058,
        "price_tier": "€", "daily_budget_eur": 80,
        "traits": {"Adventure":4.0,"Budget":4.5,"Culture":3.5,"Relaxation":4.0,"Food":3.5,"Shopping":3.0},
        "narrative": "Europe's most manageable capital — you can walk the entire old town in thirty minutes, hire a bike, ride to Lake Bled, and be back for dinner in a riverside restaurant. Ljubljana is the base camp for one of the continent's most underrated adventure playgrounds: the Julian Alps.",
        "highlights": ["Ljubljana Castle & Dragon Bridge", "Metelkova arts district", "Lake Bled day trip (40 min by car)"],
        "events": [
            {"name": "Ljubljana Festival (outdoor arts)", "months": [7,8], "tags": ["Culture","Relaxation"]},
            {"name": "Ana Desetnica Street Theatre",     "months": [7],   "tags": ["Culture","Adventure"]},
        ],
    },

    # ── Norway ───────────────────────────────────────────────────────────────
    "Oslo": {
        "country": "Norway", "lat": 59.9139, "lon": 10.7522,
        "price_tier": "€€€", "daily_budget_eur": 240,
        "traits": {"Adventure":4.5,"Budget":1.0,"Culture":3.5,"Relaxation":4.0,"Food":3.5,"Shopping":3.5},
        "narrative": "Oslo sits at the end of a fjord and has designed its entire city around the fact that nature is ten minutes away in any direction. The waterfront has been completely transformed — world-class architecture, swimming straight off public piers, and an opera house you can walk across the roof of.",
        "highlights": ["Vigeland Sculpture Park", "Aker Brygge waterfront & Oslofjord swimming", "Munch Museum"],
        "events": [
            {"name": "Oslo Jazz Festival",          "months": [8],    "tags": ["Culture","Relaxation"]},
            {"name": "Øya Music Festival",          "months": [8],    "tags": ["Adventure","Culture"]},
            {"name": "Oslo Marathon",               "months": [9],    "tags": ["Adventure"]},
        ],
    },

    # ── Finland ──────────────────────────────────────────────────────────────
    "Helsinki": {
        "country": "Finland", "lat": 60.1699, "lon": 24.9384,
        "price_tier": "€€€", "daily_budget_eur": 200,
        "traits": {"Adventure":3.5,"Budget":1.5,"Culture":4.0,"Relaxation":4.5,"Food":3.5,"Shopping":3.5},
        "narrative": "Helsinki is Scandinavian design distilled into a city — clean lines, extraordinary public saunas, and an archipelago of 330 islands you can island-hop by ferry for the price of a bus ticket. The Design District alone is worth the flight.",
        "highlights": ["Löyly & Allas Sea Pool (harbour saunas)", "Helsinki Design District", "Suomenlinna sea fortress island"],
        "events": [
            {"name": "Flow Festival (music & arts)", "months": [8],  "tags": ["Culture","Adventure"]},
            {"name": "Helsinki Design Week",         "months": [9],  "tags": ["Culture","Shopping"]},
            {"name": "Vappu (May Day festival)",     "months": [5],  "tags": ["Culture","Food"]},
        ],
    },

    # ── Iceland ──────────────────────────────────────────────────────────────
    "Reykjavik": {
        "country": "Iceland", "lat": 64.1265, "lon": -21.8174,
        "price_tier": "€€€", "daily_budget_eur": 280,
        "traits": {"Adventure":5.0,"Budget":1.0,"Culture":3.5,"Relaxation":4.0,"Food":3.5,"Shopping":3.0},
        "narrative": "Reykjavik is the smallest capital in the world with the most dramatic surroundings — geysers, glaciers, lava fields, and the Northern Lights all within two hours of the centre. The city itself punches well above its weight: a bar scene that runs until 5am, a thriving music culture, and hot dogs that are genuinely world-famous.",
        "highlights": ["Golden Circle (Geysir, Gullfoss, Þingvellir)", "Blue Lagoon or Sky Lagoon geothermal pools", "Hallgrímskirkja & Laugavegur street"],
        "events": [
            {"name": "Iceland Airwaves Music Festival", "months": [11],   "tags": ["Culture","Adventure"]},
            {"name": "Secret Solstice Festival",        "months": [6],    "tags": ["Adventure","Culture"]},
            {"name": "Northern Lights season",          "months": [10,11,12,1,2], "tags": ["Adventure","Relaxation"]},
        ],
    },

    # ── Latvia ───────────────────────────────────────────────────────────────
    "Riga": {
        "country": "Latvia", "lat": 56.9496, "lon": 24.1052,
        "price_tier": "€", "daily_budget_eur": 65,
        "traits": {"Adventure":3.0,"Budget":5.0,"Culture":4.5,"Relaxation":3.0,"Food":3.5,"Shopping":3.0},
        "narrative": "Riga has the largest collection of Art Nouveau architecture in the world — entire streets of it, in various states of grandeur and decay, which makes it feel more honest than a museum piece. Combine that with a medieval Old Town, a brilliant central market in old zeppelin hangars, and prices that feel like a different era.",
        "highlights": ["Art Nouveau district & Alberta iela", "Central Market in WWI zeppelin hangars", "Old Town & House of the Blackheads"],
        "events": [
            {"name": "Riga City Festival",       "months": [8],  "tags": ["Culture","Food"]},
            {"name": "Riga International Film Festival", "months": [10], "tags": ["Culture"]},
            {"name": "Song & Dance Celebration", "months": [7],  "tags": ["Culture","Adventure"]},
        ],
    },

    # ── Lithuania ────────────────────────────────────────────────────────────
    "Vilnius": {
        "country": "Lithuania", "lat": 54.6872, "lon": 25.2797,
        "price_tier": "€", "daily_budget_eur": 60,
        "traits": {"Adventure":3.0,"Budget":5.0,"Culture":4.5,"Relaxation":3.5,"Food":3.5,"Shopping":3.0},
        "narrative": "Vilnius is Eastern Europe's best-kept secret — a Baroque Old Town so well-preserved it's UNESCO-listed, a thriving café culture, and a microrepublic (Užupis) that declared independence as a piece of performance art and has its own constitution printed on mirrors. Extraordinary value for money.",
        "highlights": ["Vilnius Old Town & Gediminas Castle", "Užupis Republic & bohemian quarter", "Gate of Dawn & Cathedral Square"],
        "events": [
            {"name": "Vilnius Film Festival",   "months": [3],  "tags": ["Culture"]},
            {"name": "Skamba Skamba Kankliai (folk festival)", "months": [5], "tags": ["Culture","Adventure"]},
            {"name": "Capital Days street festival", "months": [9], "tags": ["Culture","Food"]},
        ],
    },

    # ── Turkey (European) ────────────────────────────────────────────────────
    "Istanbul": {
        "country": "Turkey", "lat": 41.0082, "lon": 28.9784,
        "price_tier": "€", "daily_budget_eur": 70,
        "traits": {"Adventure":4.0,"Budget":4.5,"Culture":5.0,"Relaxation":3.0,"Food":5.0,"Shopping":4.5},
        "narrative": "Istanbul is the only city in the world on two continents, and it has been the centre of three empires — which explains why the skyline looks the way it does. The Grand Bazaar has 4,000 shops. The Bosphorus strait is swimmable. The breakfast culture is worth the flight on its own.",
        "highlights": ["Hagia Sophia & Blue Mosque", "Grand Bazaar & Spice Market", "Bosphorus boat cruise at sunset"],
        "events": [
            {"name": "Istanbul Film Festival",      "months": [4],    "tags": ["Culture"]},
            {"name": "Istanbul Music Festival",     "months": [6],    "tags": ["Culture","Relaxation"]},
            {"name": "Istanbul Biennial (art)",     "months": [9,10,11], "tags": ["Culture","Shopping"]},
        ],
    },

    # ── Romania ──────────────────────────────────────────────────────────────
    "Bucharest": {
        "country": "Romania", "lat": 44.4268, "lon": 26.1025,
        "price_tier": "€", "daily_budget_eur": 55,
        "traits": {"Adventure":3.0,"Budget":5.0,"Culture":4.0,"Relaxation":3.0,"Food":4.0,"Shopping":3.5},
        "narrative": "Bucharest is chaotic, contradictory, and genuinely compelling. Belle Époque mansions sit next to Ceaușescu's megalomaniacal Palace of Parliament (the second-largest building in the world), and the nightlife in the old Floreasca district rivals anything in Berlin. One of Europe's cheapest capitals with one of its most interesting food scenes.",
        "highlights": ["Palace of Parliament (largest building in Europe)", "Floreasca & Florilor district bars & restaurants", "Village Museum open-air ethnographic park"],
        "events": [
            {"name": "George Enescu International Festival (classical music)", "months": [9], "tags": ["Culture"]},
            {"name": "Street Food Festival",   "months": [5,9], "tags": ["Food","Culture"]},
            {"name": "Electric Castle Festival", "months": [7], "tags": ["Adventure","Culture"]},
        ],
    },

    # ── Montenegro ───────────────────────────────────────────────────────────
    "Kotor": {
        "country": "Montenegro", "lat": 42.4247, "lon": 18.7712,
        "price_tier": "€", "daily_budget_eur": 75,
        "traits": {"Adventure":4.5,"Budget":4.0,"Culture":4.0,"Relaxation":5.0,"Food":3.5,"Shopping":2.5},
        "narrative": "Kotor is a medieval walled city at the bottom of Europe's southernmost fjord — dramatic mountains plunge straight into the bay, cats roam the cobblestone streets (the city maintains an official cat welfare programme), and the fortification walls climb 1,350 steps up the cliff behind it. Almost absurdly beautiful.",
        "highlights": ["City Walls hike to St. John's Fortress", "Bay of Kotor boat trip", "Old Town cats & Church of St. Tryphon"],
        "events": [
            {"name": "Kotor Carnival",              "months": [2],    "tags": ["Culture","Adventure"]},
            {"name": "KotorArt Festival",           "months": [7,8],  "tags": ["Culture","Relaxation"]},
            {"name": "Boka Night Naval Procession", "months": [8],    "tags": ["Culture","Adventure"]},
        ],
    },

    # ── Serbia ───────────────────────────────────────────────────────────────
    "Belgrade": {
        "country": "Serbia", "lat": 44.7866, "lon": 20.4489,
        "price_tier": "€", "daily_budget_eur": 50,
        "traits": {"Adventure":4.0,"Budget":5.0,"Culture":3.5,"Relaxation":2.5,"Food":4.0,"Shopping":3.0},
        "narrative": "Belgrade is the most underrated nightlife city in Europe — a floating club scene on the Sava and Danube rivers, a fortress overlooking two rivers, and a café culture so entrenched that sitting for three hours over one coffee is not just acceptable but expected. The cheapest city on this list with some of the most energy.",
        "highlights": ["Kalemegdan Fortress at sunset", "Skadarlija bohemian quarter", "Floating clubs (splavovi) on the Sava river"],
        "events": [
            {"name": "EXIT Festival (Novi Sad, 90 min away)", "months": [7], "tags": ["Adventure","Culture"]},
            {"name": "Belgrade Beer Fest",    "months": [8],  "tags": ["Food","Culture"]},
            {"name": "Belgrade Music Festival", "months": [10], "tags": ["Culture"]},
        ],
    },

    # ── France (additions) ────────────────────────────────────────────────────
    "Bordeaux": {
        "country": "France", "lat": 44.8378, "lon": -0.5792,
        "price_tier": "€€", "daily_budget_eur": 125,
        "traits": {"Adventure":2.5,"Budget":3.0,"Culture":3.5,"Relaxation":4.5,"Food":5.0,"Shopping":3.5},
        "narrative": "Bordeaux is a city that takes the pleasure principle seriously. The wine region stretching out in every direction is obvious, but the city itself has one of the longest pedestrianised waterfronts in Europe, a covered market that could occupy a morning, and a food and wine culture of extraordinary depth.",
        "highlights": ["La Cité du Vin (wine museum & tasting)", "Saint-Michel & Saint-Pierre neighbourhood markets", "Miroir d'eau water mirror at dusk"],
        "events": [
            {"name": "Bordeaux Wine Festival",      "months": [6],    "tags": ["Food","Relaxation"]},
            {"name": "Bordeaux Open Air (music)",   "months": [6,7],  "tags": ["Culture","Food"]},
            {"name": "Vinexpo",                     "months": [6],    "tags": ["Food","Culture"]},
        ],
    },
    "Marseille": {
        "country": "France", "lat": 43.2965, "lon": 5.3698,
        "price_tier": "€€", "daily_budget_eur": 115,
        "traits": {"Adventure":4.0,"Budget":3.5,"Culture":3.5,"Relaxation":3.5,"Food":4.5,"Shopping":3.0},
        "narrative": "Marseille is France's wild card — older than Paris, rougher around the edges, and completely indifferent to what anyone thinks of it. The Calanques (limestone fjords accessible by boat or trail) are among the most dramatic landscapes in Western Europe, and the bouillabaisse here is a different dish entirely from anything made outside this city.",
        "highlights": ["Calanques National Park by boat or trail", "Vieux-Port fish market at 6am", "MuCEM (Museum of European & Mediterranean Civilisations)"],
        "events": [
            {"name": "Fiesta des Suds (world music)", "months": [10],  "tags": ["Culture","Adventure"]},
            {"name": "Marseille-Cassis race",         "months": [10],  "tags": ["Adventure"]},
            {"name": "Carnival of Marseille",         "months": [2,3], "tags": ["Culture"]},
        ],
    },

    # ── Spain (additions) ─────────────────────────────────────────────────────
    "Granada": {
        "country": "Spain", "lat": 37.1773, "lon": -3.5986,
        "price_tier": "€", "daily_budget_eur": 80,
        "traits": {"Adventure":3.5,"Budget":4.5,"Culture":5.0,"Relaxation":4.0,"Food":4.0,"Shopping":3.5},
        "narrative": "Granada is where the Moorish world left its most extraordinary mark on Europe. The Alhambra palace complex is the single most visited monument in Spain for good reason — it's genuinely one of the finest things ever built. Tapas here are still free with every drink, which makes Granada one of Europe's great budget food cities.",
        "highlights": ["Alhambra & Generalife gardens (book weeks ahead)", "Sacromonte cave flamenco performances", "Albaicín Moorish quarter at sunset"],
        "events": [
            {"name": "Festival Internacional de Música y Danza", "months": [6,7], "tags": ["Culture"]},
            {"name": "Corpus Christi festivities",               "months": [6],   "tags": ["Culture","Food"]},
            {"name": "Día de la Toma (Reconquista commemoration)","months": [1],  "tags": ["Culture"]},
        ],
    },
    "Valencia": {
        "country": "Spain", "lat": 39.4699, "lon": -0.3763,
        "price_tier": "€€", "daily_budget_eur": 100,
        "traits": {"Adventure":4.0,"Budget":3.5,"Culture":4.0,"Relaxation":4.5,"Food":5.0,"Shopping":3.5},
        "narrative": "Valencia invented paella and has the confidence to prove it to you. The City of Arts and Sciences is the most architecturally ambitious complex built in Spain in a generation, the beach is fifteen minutes from the centre by bike path, and the whole city shuts down for a week every March to set things on fire (Las Fallas).",
        "highlights": ["City of Arts and Sciences (Calatrava architecture)", "Malvarrosa Beach by bike", "Central Market & authentic paella in the Albufera"],
        "events": [
            {"name": "Las Fallas (fire festival)", "months": [3],  "tags": ["Adventure","Culture"]},
            {"name": "Valencia Marathon",          "months": [12], "tags": ["Adventure"]},
            {"name": "Tomatina (Buñol, nearby)",   "months": [8],  "tags": ["Adventure","Culture"]},
        ],
    },

    # ── Italy (additions) ─────────────────────────────────────────────────────
    "Bologna": {
        "country": "Italy", "lat": 44.4949, "lon": 11.3426,
        "price_tier": "€€", "daily_budget_eur": 115,
        "traits": {"Adventure":2.0,"Budget":3.0,"Culture":4.0,"Relaxation":3.5,"Food":5.0,"Shopping":3.5},
        "narrative": "Bologna is where Italy keeps its best food and its best-kept secret. La grassa (the fat one) is the city's nickname — earned by inventing Bolognese ragù, mortadella, and tortellini. The medieval arcades (porticoes) stretch for 40km through the city, keeping you dry in the rain and cool in the sun.",
        "highlights": ["Quadrilatero food market & Eataly", "Due Torri medieval towers", "40km of medieval porticoes (UNESCO)"],
        "events": [
            {"name": "Cineteca di Bologna (cinema restoration festival)", "months": [6,7], "tags": ["Culture"]},
            {"name": "Motor Valley Fest (Ferrari, Lamborghini, Ducati)", "months": [5],   "tags": ["Adventure","Culture"]},
            {"name": "Sana (organic food fair)",                          "months": [9],   "tags": ["Food"]},
        ],
    },
    "Naples": {
        "country": "Italy", "lat": 40.8518, "lon": 14.2681,
        "price_tier": "€", "daily_budget_eur": 85,
        "traits": {"Adventure":3.5,"Budget":4.0,"Culture":4.5,"Relaxation":2.5,"Food":5.0,"Shopping":3.0},
        "narrative": "Naples is the most intense city in Italy — chaotic, magnificent, and proud of both. The pizza here is a different category of food from anything elsewhere in the world (UNESCO recognised it as intangible cultural heritage). Pompeii is forty minutes away by train, and the whole city sits under Vesuvius, which gives it an energy that feels like nothing else.",
        "highlights": ["Pizza at Da Michele or Sorbillo (arrive early)", "National Archaeological Museum (world's finest Roman collection)", "Pompeii & Herculaneum day trip"],
        "events": [
            {"name": "Pizza Village (world's largest pizza festival)", "months": [6],  "tags": ["Food","Culture"]},
            {"name": "Napoli Teatro Festival",                         "months": [6,7],"tags": ["Culture"]},
            {"name": "Feast of San Gennaro",                          "months": [9],  "tags": ["Culture","Food"]},
        ],
    },
    "Venice": {
        "country": "Italy", "lat": 45.4408, "lon": 12.3155,
        "price_tier": "€€€", "daily_budget_eur": 200,
        "traits": {"Adventure":2.5,"Budget":1.5,"Culture":5.0,"Relaxation":4.5,"Food":3.5,"Shopping":4.0},
        "narrative": "Venice is not a real city — it's a collective hallucination that somehow works. 118 islands, 400 bridges, no cars, and a Grand Canal used as a main road since the 5th century. Visit in January for the atmospheric fog and none of the crowds, or surrender to high season knowing that nowhere else looks like this.",
        "highlights": ["San Marco Basilica at opening time (8:45am)", "Dorsoduro & Cannaregio neighbourhoods away from tourists", "Vaporetto (water bus) on the Grand Canal"],
        "events": [
            {"name": "Venice Carnival",              "months": [2],      "tags": ["Culture","Shopping"]},
            {"name": "Venice Biennale (Art & Architecture)", "months": [5,6,7,8,9,10,11], "tags": ["Culture","Shopping"]},
            {"name": "Venice Film Festival",         "months": [8,9],    "tags": ["Culture"]},
            {"name": "Festa del Redentore (fireworks on the lagoon)", "months": [7], "tags": ["Culture","Relaxation"]},
        ],
    },

    # ── Germany (additions) ───────────────────────────────────────────────────
    "Hamburg": {
        "country": "Germany", "lat": 53.5753, "lon": 10.0153,
        "price_tier": "€€", "daily_budget_eur": 130,
        "traits": {"Adventure":3.5,"Budget":3.0,"Culture":4.0,"Relaxation":3.0,"Food":4.0,"Shopping":4.0},
        "narrative": "Hamburg has more bridges than Venice and Amsterdam combined, a port that still handles 10,000 ships a year, and a music history that includes the Beatles' residency and a current club scene that takes itself very seriously. The Elbphilharmonie concert hall — a glass wave sitting on top of an old warehouse — is one of the finest pieces of architecture built anywhere in the 21st century.",
        "highlights": ["Elbphilharmonie & HafenCity waterfront", "Reeperbahn & Schanzenviertel nightlife", "Fischmarkt Sunday morning (5am opening)"],
        "events": [
            {"name": "Reeperbahn Festival (music)",  "months": [9],    "tags": ["Culture","Adventure"]},
            {"name": "Hamburg Marathon",             "months": [4],    "tags": ["Adventure"]},
            {"name": "Hamburg DOM (funfair)",        "months": [3,4,7,8,11,12], "tags": ["Culture","Food"]},
        ],
    },
    "Cologne": {
        "country": "Germany", "lat": 50.9333, "lon": 6.9500,
        "price_tier": "€€", "daily_budget_eur": 120,
        "traits": {"Adventure":2.5,"Budget":3.0,"Culture":4.0,"Relaxation":3.0,"Food":3.5,"Shopping":4.0},
        "narrative": "Cologne has one of the greatest Gothic cathedrals in the world — the Dom took 632 years to complete and towers over the Rhine in a way that never stops being impressive. The city is also one of Germany's great carnival cities, and the Kölsch beer culture (served in tiny 200ml glasses, replaced before you finish) is a charming local religion.",
        "highlights": ["Cologne Cathedral (Dom) & Treasury", "Museum Ludwig (Picasso & pop art collection)", "Rhine riverfront & Kölsch beer halls"],
        "events": [
            {"name": "Cologne Carnival",            "months": [2,3],  "tags": ["Culture","Food","Adventure"]},
            {"name": "Cologne Pride (Christopher Street Day)", "months": [7], "tags": ["Culture","Adventure"]},
            {"name": "Art Cologne",                 "months": [4],    "tags": ["Culture","Shopping"]},
        ],
    },

    # ── Belgium (additions) ───────────────────────────────────────────────────
    "Ghent": {
        "country": "Belgium", "lat": 51.0543, "lon": 3.7174,
        "price_tier": "€€", "daily_budget_eur": 115,
        "traits": {"Adventure":2.5,"Budget":3.5,"Culture":4.5,"Relaxation":3.5,"Food":4.5,"Shopping":3.5},
        "narrative": "Ghent is what Brussels wants to be when it grows up — a medieval Flemish city with three imposing towers, a river running through it, and an authenticity that Bruges lost to the tourist coaches. The Ghent Altarpiece (the most stolen artwork in history) lives here in a dedicated room in St Bavo's Cathedral, and the food scene is one of Belgium's best.",
        "highlights": ["Graslei & Korenlei medieval waterfront", "St Bavo's Cathedral & the Ghent Altarpiece", "Vrijdagmarkt & Friday street market"],
        "events": [
            {"name": "Ghent Festivities (10-day city festival)", "months": [7], "tags": ["Culture","Food","Adventure"]},
            {"name": "Film Fest Gent",               "months": [10], "tags": ["Culture"]},
        ],
    },

    # ── Switzerland (additions) ───────────────────────────────────────────────
    "Geneva": {
        "country": "Switzerland", "lat": 46.2044, "lon": 6.1432,
        "price_tier": "€€€", "daily_budget_eur": 270,
        "traits": {"Adventure":3.0,"Budget":1.0,"Culture":3.5,"Relaxation":5.0,"Food":4.0,"Shopping":4.5},
        "narrative": "Geneva sits at the end of Europe's largest Alpine lake and takes the concept of civilised living more seriously than anywhere else on the continent. The Old Town is compact and beautiful, the lake is swimmable in summer, and the watch and jewellery shopping is in a category of its own. Come with a generous budget and an unhurried pace.",
        "highlights": ["Lake Geneva & Jet d'Eau fountain", "Old Town & St. Peter's Cathedral", "CERN (Large Hadron Collider) free tours"],
        "events": [
            {"name": "Geneva International Motor Show", "months": [3],  "tags": ["Adventure","Culture"]},
            {"name": "Fêtes de Genève (fireworks on the lake)", "months": [8], "tags": ["Relaxation","Culture"]},
            {"name": "L'Escalade (medieval festival)", "months": [12], "tags": ["Culture","Food"]},
        ],
    },

}

# ── Place-type tags for Route Optimizer filter ───────────────────────────────
# Tags: "urban" | "coastal" | "historic" | "nature"
CITY_TAGS = {
    "London":     ["urban"],
    "Edinburgh":  ["urban", "nature"],
    "Dublin":     ["urban", "coastal"],
    "Paris":      ["urban", "historic"],
    "Lyon":       ["urban"],
    "Nice":       ["coastal", "urban"],
    "Barcelona":  ["urban", "coastal"],
    "Madrid":     ["urban"],
    "Seville":    ["urban", "historic"],
    "Bilbao":     ["urban", "coastal"],
    "Lisbon":     ["urban", "coastal"],
    "Porto":      ["urban", "coastal"],
    "Amsterdam":  ["urban"],
    "Brussels":   ["urban"],
    "Bruges":     ["historic"],
    "Berlin":     ["urban"],
    "Munich":     ["urban"],
    "Frankfurt":  ["urban"],
    "Vienna":     ["urban", "historic"],
    "Prague":     ["urban", "historic"],
    "Budapest":   ["urban", "historic"],
    "Krakow":     ["urban", "historic"],
    "Tallinn":    ["urban", "historic", "coastal"],
    "Zurich":     ["urban", "nature"],
    "Rome":       ["urban", "historic"],
    "Florence":   ["urban", "historic"],
    "Milan":      ["urban"],
    "Copenhagen": ["urban", "coastal"],
    "Stockholm":  ["urban", "coastal", "nature"],
    "Athens":     ["urban", "historic"],
    "Dubrovnik":  ["coastal", "historic"],
    "Ljubljana":  ["urban", "nature"],
    "Oslo":       ["urban", "coastal", "nature"],
    "Helsinki":   ["urban", "coastal"],
    "Reykjavik":  ["urban", "nature", "coastal"],
    "Riga":       ["urban", "historic"],
    "Vilnius":    ["urban", "historic"],
    "Istanbul":   ["urban", "historic", "coastal"],
    "Bucharest":  ["urban"],
    "Kotor":      ["coastal", "historic", "nature"],
    "Belgrade":   ["urban"],
    "Bordeaux":   ["urban"],
    "Marseille":  ["coastal", "urban", "nature"],
    "Granada":    ["urban", "historic"],
    "Valencia":   ["urban", "coastal"],
    "Bologna":    ["urban", "historic"],
    "Naples":     ["urban", "coastal", "historic"],
    "Venice":     ["coastal", "historic"],
    "Hamburg":    ["urban", "coastal"],
    "Cologne":    ["urban", "historic"],
    "Ghent":      ["urban", "historic"],
    "Geneva":     ["urban", "nature"],
}
