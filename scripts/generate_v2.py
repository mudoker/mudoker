import xml.etree.ElementTree as ET
import os, json, urllib.request, subprocess, math
from collections import defaultdict
from datetime import datetime

ICONS = {
    "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>',
    "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    "brain-circuit": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M9 13a4.5 4.5 0 0 0 3-4"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M6 18a4 4 0 0 1-1.967-.518"/><path d="M12 13h4"/><path d="M12 18h6a2 2 0 0 1 2 2v1"/><path d="M12 8h8"/><path d="M16 8V5a2 2 0 0 1 2-2"/><circle cx="16" cy="13" r=".5"/><circle cx="18" cy="3" r=".5"/><circle cx="20" cy="21" r=".5"/><circle cx="20" cy="8" r=".5"/>',
    "folder-code": '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/><path d="m10 13-2 2 2 2"/><path d="m14 17 2-2-2-2"/>',
    "code-2": '<path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/>',
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "github": '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
    "external-link": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "trending-up": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
    "terminal": '<polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/>'
}

def truncate_ellipsis(text, max_len=16):
    """Safely truncate text with ellipsis to prevent visual overflow across viewports."""
    if not text:
        return ""
    if len(text) > max_len:
        return text[:max_len-1].strip() + "&#8230;"
    return text

def generate_icons(base_dir):
    os.makedirs(f"{base_dir}/assets/icons", exist_ok=True)
    for name, inner in ICONS.items():
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <style>
    path, circle, rect, line, polyline, polygon {{ stroke: #475569; }}
    @media (prefers-color-scheme: dark) {{
      path, circle, rect, line, polyline, polygon {{ stroke: #94A3B8; }}
    }}
  </style>
  {inner}
</svg>'''
        with open(f"{base_dir}/assets/icons/{name}.svg", "w") as f:
            f.write(svg)
        ET.fromstring(svg)

# ==========================================
# 0. LIVE DATA FETCHER & REALTIME METRICS
# ==========================================

def get_live_github_data(base_dir):
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not token:
        try:
            token = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True).stdout.strip()
        except Exception:
            token = None

    cache_file = os.path.join(base_dir, 'data', 'telemetry_cache.json')
    os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)

    data = None
    if token:
        query = '''
query {
  viewer {
    login
    contributionsCollection {
      restrictedContributionsCount
      totalCommitContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      totalRepositoryContributions
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            weekday
          }
        }
      }
    }
    pullRequests(states: [MERGED, OPEN]) {
      totalCount
    }
    repositories(ownerAffiliations: OWNER, first: 100, isFork: false) {
      nodes {
        name
        isPrivate
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node { name color }
          }
        }
      }
    }
  }
}
'''
        try:
            req = urllib.request.Request(
                'https://api.github.com/graphql',
                data=json.dumps({'query': query}).encode(),
                headers={
                    'Authorization': f'Bearer {token}',
                    'User-Agent': 'Mudoker-Telemetry-Updater',
                    'Content-Type': 'application/json'
                }
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw_json = json.loads(resp.read().decode())
                if 'data' in raw_json and 'viewer' in raw_json['data']:
                    data = raw_json['data']['viewer']
                    with open(cache_file, 'w') as f:
                        json.dump(data, f)
        except Exception as e:
            print('Live GraphQL fetch error, using cache:', e)

    if not data and os.path.exists(cache_file):
        with open(cache_file) as f:
            data = json.load(f)

    return data

def parse_metrics(data):
    coll = data['contributionsCollection']
    cal = coll['contributionCalendar']
    all_days = [d for w in cal['weeks'] for d in w['contributionDays']]

    # 1. 14-Day Velocity Cadence
    last_14 = all_days[-14:]
    max_14 = max([d['contributionCount'] for d in last_14] + [1])
    days_14 = []
    for i, d in enumerate(last_14):
        cnt = d['contributionCount']
        dt = datetime.strptime(d['date'], '%Y-%m-%d')
        days_14.append({
            'date': dt.strftime('%m/%d'),
            'count': cnt,
            'is_peak': (cnt == max_14 and cnt > 0),
            'is_today': (i == 13)
        })
    avg_14 = round(sum(d['count'] for d in days_14) / 14, 1)
    active_14 = sum(1 for d in days_14 if d['count'] > 0)
    consistency_14 = round((active_14 / 14) * 100)

    # 2. Engineering Scope & Work Breakdown (Non-duplicate Metric for Overview)
    priv_c = coll.get('restrictedContributionsCount', 0)
    pub_c = coll.get('totalCommitContributions', 0)
    pr_c = coll.get('totalPullRequestContributions', 0) + coll.get('totalPullRequestReviewContributions', 0)
    total_c = priv_c + pub_c + pr_c or 1

    pct_priv = round((priv_c / total_c) * 100)
    pct_pub = round((pub_c / total_c) * 100)
    pct_pr = max(1, 100 - pct_priv - pct_pub)

    repos = data['repositories']['nodes']
    total_repos = len(repos)
    priv_repos = sum(1 for r in repos if r['isPrivate'])
    pct_priv_repos = round((priv_repos / total_repos) * 100) if total_repos > 0 else 0
    total_prs = data.get('pullRequests', {}).get('totalCount', 0)

    scope_data = {
        'priv_count': priv_c,
        'pub_count': pub_c,
        'pr_count': pr_c,
        'pct_priv': pct_priv,
        'pct_pub': pct_pub,
        'pct_pr': pct_pr,
        'total_repos': total_repos,
        'priv_repos': priv_repos,
        'pct_priv_repos': pct_priv_repos,
        'total_prs': total_prs
    }

    # 3. Language Breakdown across BOTH public and private repositories (NO repo names)
    code_bytes = defaultdict(int)
    for r in repos:
        name = r['name']
        if any(k in name.lower() for k in ['lab', 'alien-shooting', 'data_analysis', 'diabetes']):
            continue
        for edge in r['languages']['edges']:
            lname = edge['node']['name']
            if lname not in ['HTML', 'CSS', 'Shell', 'Just', 'SmPL', 'Meson', 'Dockerfile', 'CMake', 'Go Template', 'Jupyter Notebook']:
                code_bytes[lname] += edge['size']

    total_code = sum(code_bytes.values()) or 1
    sorted_code = sorted(code_bytes.items(), key=lambda x: x[1], reverse=True)

    palette = ['#38BDF8', '#34D399', '#A78BFA', '#FBBF24']
    top_langs = []
    covered = 0
    for idx, (l, b) in enumerate(sorted_code[:3]):
        pct = round((b / total_code) * 100)
        covered += pct
        top_langs.append({'name': truncate_ellipsis(l, 15), 'pct': pct, 'bytes': b, 'color': palette[idx]})
    other_pct = max(0, 100 - covered)
    top_langs.append({'name': 'Python &amp; Other', 'pct': other_pct, 'bytes': 0, 'color': palette[3]})

    # 4. 12-Month Line Chart
    monthly = defaultdict(int)
    for d in all_days:
        m = d['date'][:7]
        monthly[m] += d['contributionCount']

    sorted_m = sorted(monthly.keys())[-12:]
    m_vals = [monthly[m] for m in sorted_m]
    m_labels = [datetime.strptime(m, '%Y-%m').strftime('%b').upper() for m in sorted_m]
    total_annual = cal['totalContributions']
    avg_monthly = round(sum(m_vals) / len(m_vals), 1)

    rolling_avg = []
    for i in range(len(m_vals)):
        win = m_vals[max(0, i-2):i+1]
        rolling_avg.append(round(sum(win) / len(win), 1))

    peak_val = max(m_vals)
    peak_idx = m_vals.index(peak_val)
    peak_month = m_labels[peak_idx]

    scale_max = math.ceil(peak_val / 100) * 100
    if scale_max == 0: scale_max = 100
    y_ticks = [0, int(scale_max * 0.25), int(scale_max * 0.5), int(scale_max * 0.75), scale_max]

    # 5. Weekday Cadence Bar Chart
    weekday_counts = defaultdict(int)
    for d in all_days:
        weekday_counts[d['weekday']] += d['contributionCount']

    weekday_order = [1, 2, 3, 4, 5, 6, 0] # MON .. SUN
    weekday_names = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    w_counts = [weekday_counts[i] for i in weekday_order]
    total_w = sum(w_counts) or 1
    w_pcts = [round((c / total_w) * 100) for c in w_counts]
    peak_w_idx = w_pcts.index(max(w_pcts))
    peak_w_day = weekday_names[peak_w_idx]
    peak_w_pct = w_pcts[peak_w_idx]

    weekday_data = []
    for i, name in enumerate(weekday_names):
        weekday_data.append({
            'name': name,
            'count': w_counts[i],
            'pct': w_pcts[i],
            'is_peak': (i == peak_w_idx)
        })

    return {
        'overview': {
            'days_14': days_14,
            'avg_14': avg_14,
            'consistency_14': consistency_14,
            'scope': scope_data
        },
        'telemetry': {
            'months': m_labels,
            'm_vals': m_vals,
            'rolling_avg': rolling_avg,
            'total_annual': total_annual,
            'avg_monthly': avg_monthly,
            'peak_val': peak_val,
            'peak_month': peak_month,
            'peak_idx': peak_idx,
            'scale_max': scale_max,
            'y_ticks': y_ticks,
            'pie_slices': top_langs,
            'weekdays': weekday_data,
            'peak_w_day': peak_w_day,
            'peak_w_pct': peak_w_pct
        }
    }


# ==========================================
# 1. HERO BANNER WITH ROTATING WORLD GLOBE
# ==========================================

W_GLOBE = 720
H_GLOBE = 290
cx_globe = 860
cy_globe = 135
r_globe = 145

def lonlat_to_xy(lon, lat):
    x = (lon + 180) / 360 * W_GLOBE
    y = (90 - lat) / 180 * H_GLOBE
    return x, y

continents_data = {
    "north_america": [
        (-168, 65), (-140, 70), (-125, 70), (-85, 75), (-75, 60), (-60, 48), 
        (-70, 42), (-80, 25), (-90, 30), (-98, 26), (-105, 20), (-85, 15), 
        (-78, 8), (-82, 9), (-92, 16), (-105, 22), (-115, 32), (-124, 38), 
        (-125, 48), (-135, 58), (-165, 60)
    ],
    "greenland": [
        (-50, 60), (-25, 70), (-20, 80), (-40, 83), (-60, 78), (-55, 68)
    ],
    "south_america": [
        (-78, 8), (-60, 10), (-35, -5), (-38, -18), (-50, -32), (-55, -45),
        (-68, -55), (-75, -50), (-72, -35), (-80, -5), (-80, 5)
    ],
    "europe": [
        (-10, 36), (0, 44), (5, 52), (10, 55), (15, 60), (28, 70), (40, 65),
        (50, 55), (35, 45), (28, 40), (20, 36), (10, 36), (-5, 36)
    ],
    "uk_scandi": [
        (-5, 50), (-5, 58), (2, 58), (2, 50), (12, 56), (18, 60), (28, 70), 
        (15, 65), (5, 60)
    ],
    "africa": [
        (-15, 12), (-17, 22), (-5, 36), (10, 37), (25, 32), (32, 30), (43, 12),
        (50, 10), (40, -5), (35, -25), (25, -34), (18, -34), (12, -15), (8, 4),
        (-5, 5), (-15, 12)
    ],
    "asia": [
        (40, 65), (60, 70), (90, 75), (130, 72), (170, 65), (160, 55), (140, 50),
        (130, 40), (122, 32), (120, 22), (108, 12), (105, 20), (100, 10), (80, 10),
        (72, 22), (60, 25), (55, 30), (45, 30), (35, 40), (45, 55)
    ],
    "india": [
        (70, 24), (80, 26), (88, 22), (80, 10), (76, 8), (73, 15)
    ],
    "southeast_asia": [
        (100, 20), (108, 22), (108, 12), (105, 9), (102, 12), (100, 15)
    ],
    "japan": [
        (130, 32), (135, 35), (142, 42), (140, 36), (132, 30)
    ],
    "australia": [
        (115, -22), (130, -12), (142, -10), (152, -25), (150, -37), (138, -35),
        (130, -32), (116, -35), (114, -26)
    ]
}

def build_continent_svg_paths(offset_x=0):
    paths = []
    for name, points in continents_data.items():
        coords = [lonlat_to_xy(lon, lat) for lon, lat in points]
        d = f"M {coords[0][0] + offset_x:.1f} {coords[0][1]:.1f}"
        for x, y in coords[1:]:
            d += f" L {x + offset_x:.1f} {y:.1f}"
        d += " Z"
        paths.append(d)
    return " ".join(paths)

def build_land_dots(offset_x=0, color="#38BDF8"):
    key_centers = [
        (-100, 45), (-110, 52), (-90, 38), (-80, 35), (-120, 48), (-70, 46),
        (-60, -10), (-50, -20), (-65, -30), (-45, -15),
        (15, 50), (25, 55), (5, 46), (35, 58),
        (20, 10), (15, 25), (25, -15), (30, 0), (10, 0),
        (80, 50), (100, 55), (115, 40), (105, 32), (70, 30), (85, 25), (60, 40),
        (102, 16), (105, 18), (108, 14), (110, -5),
        (135, -25), (125, -28), (145, -22)
    ]
    dots = []
    for lon, lat in key_centers:
        x, y = lonlat_to_xy(lon, lat)
        dots.append(f'<circle cx="{x + offset_x:.1f}" cy="{y:.1f}" r="2" fill="{color}" fill-opacity="0.75"/>')
    return "\n".join(dots)

vn_x, vn_y = lonlat_to_xy(106.63, 10.82)

def generate_hero_banner(is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    grid_color = "#162032" if is_dark else "#E2E8F0"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#64748B"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    badge_bg = "rgba(30, 41, 59, 0.7)" if is_dark else "rgba(241, 245, 249, 0.9)"
    badge_border = "#334155" if is_dark else "#CBD5E1"
    
    continent_fill = "#38BDF8" if is_dark else "#0284C7"
    grid_stroke = "#1E293B" if is_dark else "#E2E8F0"

    all_continents = f'''
    <path d="{build_continent_svg_paths(0)} {build_continent_svg_paths(W_GLOBE)} {build_continent_svg_paths(2*W_GLOBE)}" fill="{continent_fill}" fill-opacity="{'0.28' if is_dark else '0.22'}" stroke="{continent_fill}" stroke-width="1.2" stroke-opacity="{'0.85' if is_dark else '0.7'}"/>
    {build_land_dots(0, continent_fill)}
    {build_land_dots(W_GLOBE, continent_fill)}
    {build_land_dots(2*W_GLOBE, continent_fill)}
    '''

    vn_dots = ""
    for off in [0, W_GLOBE, 2*W_GLOBE]:
        vn_dots += f'''
        <g transform="translate({vn_x + off:.1f}, {vn_y:.1f})">
          <circle cx="0" cy="0" r="3.5" fill="{accent_blue}"/>
          <circle cx="0" cy="0" r="7" fill="none" stroke="{accent_blue}" stroke-width="1.2">
            <animate attributeName="r" values="3.5;14;3.5" dur="2.4s" repeatCount="indefinite"/>
            <animate attributeName="stroke-opacity" values="0.9;0.1;0.9" dur="2.4s" repeatCount="indefinite"/>
          </circle>
          <text x="9" y="-4" font-family="'JetBrains Mono', Consolas, monospace" font-size="8.5" font-weight="700" fill="{accent_blue}" letter-spacing="0.5">VN</text>
        </g>
        '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 320" width="100%" height="100%">
  <defs>
    <pattern id="grid_{'dark' if is_dark else 'light'}" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="{grid_color}" stroke-width="0.75" stroke-opacity="0.6"/>
      <circle cx="32" cy="32" r="1" fill="{grid_color}" fill-opacity="0.8"/>
    </pattern>
    <clipPath id="banner_clip_{'dark' if is_dark else 'light'}">
      <rect width="958" height="318" x="1" y="1" rx="14"/>
    </clipPath>
    <clipPath id="globe_mask_{'dark' if is_dark else 'light'}">
      <circle cx="{cx_globe}" cy="{cy_globe}" r="{r_globe}"/>
    </clipPath>
    <radialGradient id="globe_glow_{'dark' if is_dark else 'light'}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{accent_blue}" stop-opacity="{'0.35' if is_dark else '0.22'}"/>
      <stop offset="65%" stop-color="{accent_blue}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="{accent_blue}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="sphere_shading_{'dark' if is_dark else 'light'}" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="{'#1E293B' if is_dark else '#FFFFFF'}" stop-opacity="0.05"/>
      <stop offset="60%" stop-color="{'#000000' if is_dark else '#CBD5E1'}" stop-opacity="{'0.4' if is_dark else '0.15'}"/>
      <stop offset="100%" stop-color="{'#000000' if is_dark else '#94A3B8'}" stop-opacity="{'0.88' if is_dark else '0.4'}"/>
    </radialGradient>
  </defs>

  <g clip-path="url(#banner_clip_{'dark' if is_dark else 'light'})">
    <rect width="958" height="318" x="1" y="1" fill="{bg_color}"/>
    <rect width="958" height="318" x="1" y="1" fill="url(#grid_{'dark' if is_dark else 'light'})"/>

    <!-- Corner Overflow Rotating 3D World Globe -->
    <circle cx="{cx_globe}" cy="{cy_globe}" r="{r_globe + 40}" fill="url(#globe_glow_{'dark' if is_dark else 'light'})"/>
    <ellipse cx="{cx_globe}" cy="{cy_globe}" rx="{r_globe + 35}" ry="45" fill="none" stroke="{accent_blue}" stroke-width="1.2" stroke-opacity="0.35" stroke-dasharray="5 7" transform="rotate(-20 {cx_globe} {cy_globe})"/>
    <circle cx="{cx_globe}" cy="{cy_globe}" r="{r_globe}" fill="{'#090D14' if is_dark else '#F1F5F9'}" stroke="{accent_blue}" stroke-width="1.8" stroke-opacity="0.85"/>

    <g clip-path="url(#globe_mask_{'dark' if is_dark else 'light'})">
      <g transform="rotate(-15 {cx_globe} {cy_globe})">
        <ellipse cx="{cx_globe}" cy="{cy_globe}" rx="{r_globe}" ry="0" fill="none" stroke="{grid_stroke}" stroke-width="1.2" stroke-opacity="0.7"/>
        <ellipse cx="{cx_globe}" cy="{cy_globe - 45}" rx="137" ry="35" fill="none" stroke="{grid_stroke}" stroke-width="0.9" stroke-opacity="0.55"/>
        <ellipse cx="{cx_globe}" cy="{cy_globe + 45}" rx="137" ry="35" fill="none" stroke="{grid_stroke}" stroke-width="0.9" stroke-opacity="0.55"/>
        <ellipse cx="{cx_globe}" cy="{cy_globe - 90}" rx="113" ry="28" fill="none" stroke="{grid_stroke}" stroke-width="0.8" stroke-opacity="0.45"/>
        <ellipse cx="{cx_globe}" cy="{cy_globe + 90}" rx="113" ry="28" fill="none" stroke="{grid_stroke}" stroke-width="0.8" stroke-opacity="0.45"/>

        <!-- Rotating World Continents & Fixed Beacon Dot -->
        <g transform="translate({cx_globe - W_GLOBE}, {cy_globe - r_globe})">
          <animateTransform attributeName="transform" type="translate" from="{cx_globe}, {cy_globe - r_globe}" to="{cx_globe - W_GLOBE}, {cy_globe - r_globe}" dur="22s" repeatCount="indefinite"/>
          {all_continents}
          {vn_dots}
        </g>
      </g>
      <circle cx="{cx_globe}" cy="{cy_globe}" r="{r_globe}" fill="url(#sphere_shading_{'dark' if is_dark else 'light'})"/>
    </g>
  </g>

  <rect width="958" height="318" x="1" y="1" rx="14" fill="none" stroke="{border_color}" stroke-width="1.5"/>

  <!-- Top System Bar -->
  <g transform="translate(36, 36)">
    <circle cx="4" cy="4" r="4.5" fill="{accent_emerald}"/>
    <circle cx="4" cy="4" r="9" fill="none" stroke="{accent_emerald}" stroke-width="1" stroke-opacity="0.4">
      <animate attributeName="r" values="4.5;10;4.5" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="0.6;0.1;0.6" dur="3s" repeatCount="indefinite"/>
    </circle>
    <text x="24" y="8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', monospace" font-size="11" font-weight="600" fill="{accent_emerald}" letter-spacing="1.5">SYSTEM ACTIVE // ARCHITECTURE &#8226; SYSTEMS &#8226; AI</text>
  </g>

  <line x1="36" y1="58" x2="660" y2="58" stroke="{border_color}" stroke-width="1" stroke-dasharray="4 4"/>

  <!-- Left Main Brand (max-width safe for all screen sizes) -->
  <g transform="translate(36, 118)">
    <text x="0" y="-8" font-family="'JetBrains Mono', Consolas, monospace" font-size="14" font-weight="500" fill="{accent_blue}" letter-spacing="0.5">&gt; whoami --portfolio</text>
    <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="46" font-weight="800" fill="{text_primary}" letter-spacing="-1">mudoker</text>
    <text x="220" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="20" font-weight="400" fill="{text_muted}">/</text>
    <text x="238" y="42" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="20" font-weight="500" fill="{text_secondary}">software &amp; systems engineer</text>

    <text x="0" y="82" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14" font-weight="400" fill="{text_secondary}">
      Engineering resilient backends, keyboard-first TUIs, and practical AI.
    </text>
  </g>

  <!-- Bottom Fast Tags Bar (Responsive Spacing) -->
  <g transform="translate(36, 268)">
    <rect x="0" y="0" width="120" height="28" rx="6" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <circle cx="14" cy="14" r="3" fill="{accent_blue}"/>
    <text x="26" y="18" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="{text_primary}">GO &amp; TUI</text>

    <rect x="132" y="0" width="160" height="28" rx="6" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <circle cx="146" cy="14" r="3" fill="{accent_emerald}"/>
    <text x="158" y="18" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="{text_primary}">BACKEND SYSTEMS</text>

    <rect x="304" y="0" width="154" height="28" rx="6" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <circle cx="318" cy="14" r="3" fill="#A78BFA"/>
    <text x="330" y="18" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="{text_primary}">APPLIED AI LIVE</text>

    <rect x="470" y="0" width="134" height="28" rx="6" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <circle cx="484" cy="14" r="3" fill="#FBBF24"/>
    <text x="496" y="18" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="{text_primary}">LINUX KERNEL</text>
  </g>
</svg>'''
    ET.fromstring(svg)
    return svg


# =========================================================================
# 2. ACTIVITY & OVERVIEW (14-DAY VELOCITY & PRODUCTION SCOPE BREAKDOWN)
# =========================================================================

def generate_overview_activity(metrics, is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    card_bg = "#111827" if is_dark else "#FFFFFF"
    card_border = "#1F2937" if is_dark else "#E5E7EB"
    grid_color = "#1E293B" if is_dark else "#E2E8F0"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    accent_purple = "#A78BFA" if is_dark else "#7C3AED"
    pill_bg = "rgba(30, 41, 59, 0.6)" if is_dark else "rgba(241, 245, 249, 0.8)"
    pill_border = "#334155" if is_dark else "#CBD5E1"

    ov = metrics['overview']
    days = ov['days_14']
    avg_14 = ov['avg_14']
    consistency_14 = ov['consistency_14']
    scope = ov['scope']

    # Left: 14 Days Bar Plot
    max_c = max([d['count'] for d in days] + [1])
    bar_start_x = 22
    bar_slot_w = 31.5
    bar_w = 16
    base_y = 125
    max_h = 58

    chart_bars = ""
    for i, d in enumerate(days):
        bx = bar_start_x + i * bar_slot_w + (bar_slot_w - bar_w) / 2
        bh = (d['count'] / max_c) * max_h if d['count'] > 0 else 3
        by = base_y - bh
        color = accent_blue if d['is_peak'] else (accent_emerald if d['count'] > 0 else ("#334155" if is_dark else "#CBD5E1"))
        tcolor = accent_blue if d['is_peak'] else text_primary

        chart_bars += f'<rect x="{bx:.1f}" y="{base_y - max_h}" width="{bar_w}" height="{max_h}" rx="2.5" fill="{grid_color}" fill-opacity="0.35"/>\n'
        chart_bars += f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w}" height="{bh:.1f}" rx="2.5" fill="{color}"/>\n'
        if d['count'] > 0:
            chart_bars += f'<text x="{bx + bar_w/2:.1f}" y="{by - 4:.1f}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="7.5" font-weight="600" fill="{tcolor}">{d["count"]}</text>\n'
        chart_bars += f'<text x="{bx + bar_w/2:.1f}" y="{base_y + 13}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="7.5" font-weight="500" fill="{text_secondary}">{d["date"]}</text>\n'

    # Right: Work Allocation & Engineering Scope (Non-duplicate Metric)
    total_bar_w = 416
    w_priv = (scope['pct_priv'] / 100) * total_bar_w
    w_pub = (scope['pct_pub'] / 100) * total_bar_w
    w_pr = total_bar_w - w_priv - w_pub

    scope_rects = f'''
    <rect x="0" y="0" width="{w_priv:.1f}" height="10" rx="3" fill="{accent_blue}"/>
    <rect x="{w_priv + 2:.1f}" y="0" width="{max(0, w_pub - 4):.1f}" height="10" rx="3" fill="{accent_emerald}"/>
    <rect x="{w_priv + w_pub:.1f}" y="0" width="{max(0, w_pr):.1f}" height="10" rx="3" fill="{accent_purple}"/>
    '''

    scope_labels = f'''
    <g transform="translate(0, 0)">
      <circle cx="4" cy="4" r="3.5" fill="{accent_blue}"/>
      <text x="12" y="7" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="10.5" font-weight="600" fill="{text_primary}">Private Systems</text>
      <text x="12" y="21" font-family="'JetBrains Mono', monospace" font-size="8.5" fill="{text_secondary}">{scope['priv_count']:,} ({scope['pct_priv']}%)</text>
    </g>
    <g transform="translate(145, 0)">
      <circle cx="4" cy="4" r="3.5" fill="{accent_emerald}"/>
      <text x="12" y="7" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="10.5" font-weight="600" fill="{text_primary}">Open Source</text>
      <text x="12" y="21" font-family="'JetBrains Mono', monospace" font-size="8.5" fill="{text_secondary}">{scope['pub_count']:,} ({scope['pct_pub']}%)</text>
    </g>
    <g transform="translate(285, 0)">
      <circle cx="4" cy="4" r="3.5" fill="{accent_purple}"/>
      <text x="12" y="7" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="10.5" font-weight="600" fill="{text_primary}">Reviews &amp; PRs</text>
      <text x="12" y="21" font-family="'JetBrains Mono', monospace" font-size="8.5" fill="{text_secondary}">{scope['pr_count']} ({scope['pct_pr']}%)</text>
    </g>
    '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 216" width="100%" height="100%">
  <rect width="958" height="214" x="1" y="1" rx="14" fill="{bg_color}" stroke="{border_color}" stroke-width="1.2"/>

  <!-- Top Title -->
  <text x="24" y="25" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="{accent_blue}" letter-spacing="1">ACTIVITY &amp; ENGINEERING SCOPE</text>
  <text x="250" y="25" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" fill="{text_secondary}">// SPRINT VELOCITY &amp; PRODUCTION SCOPE ALLOCATION</text>

  <!-- Left: 14-day velocity chart -->
  <g transform="translate(24, 42)">
    <rect width="450" height="152" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    
    <text x="18" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" font-weight="700" fill="{text_primary}">14-Day Velocity Cadence</text>
    <text x="18" y="36" font-family="'JetBrains Mono', monospace" font-size="8.5" fill="{text_secondary}">RECENT ROLLING COMMITS</text>

    <!-- Badges -->
    <g transform="translate(248, 12)">
      <rect width="86" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <circle cx="10" cy="10" r="2.5" fill="{accent_blue}"/>
      <text x="18" y="13.5" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="{text_primary}">{avg_14} / DAY</text>

      <rect x="92" y="0" width="94" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <circle cx="102" cy="10" r="2.5" fill="{accent_emerald}"/>
      <text x="110" y="13.5" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="{text_primary}">{consistency_14}% CONSISTENT</text>
    </g>

    <!-- 14 Bars -->
    {chart_bars}
  </g>

  <!-- Right: Work Allocation & Scope (Production vs Open Source) -->
  <g transform="translate(492, 42)">
    <rect width="444" height="152" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    
    <text x="18" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" font-weight="700" fill="{text_primary}">Work Allocation &amp; Scope</text>
    <text x="18" y="36" font-family="'JetBrains Mono', monospace" font-size="8.5" fill="{text_secondary}">PRODUCTION ARCHITECTURE VS OPEN SOURCE RATIO</text>

    <!-- Badges -->
    <g transform="translate(268, 12)">
      <rect width="160" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <circle cx="10" cy="10" r="2.5" fill="{accent_blue}"/>
      <text x="18" y="13.5" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="{text_primary}">{scope['total_repos']} REPOS // {scope['pct_priv_repos']}% PRIV</text>
    </g>

    <!-- Stacked Bar -->
    <g transform="translate(14, 52)">
      <rect width="{total_bar_w}" height="10" rx="3" fill="{grid_color}" fill-opacity="0.3"/>
      {scope_rects}
    </g>

    <!-- Scope Labels -->
    <g transform="translate(14, 76)">
      {scope_labels}
    </g>

    <!-- Engineering Chips with Safe Clamped Bounds -->
    <g transform="translate(14, 116)">
      <rect x="0" y="0" width="136" height="22" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="68" y="14" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="{text_secondary}">{scope['pct_priv']}% PRODUCTION FOCUS</text>

      <rect x="144" y="0" width="136" height="22" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="212" y="14" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="{text_secondary}">{scope['total_prs']} PULL REQUESTS</text>

      <rect x="288" y="0" width="128" height="22" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="352" y="14" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="{text_secondary}">REALTIME VERIFIED</text>
    </g>
  </g>
</svg>'''
    ET.fromstring(svg)
    return svg


# =========================================================================
# 3. ENGINEERING TELEMETRY (REAL-TIME DATA-DRIVEN // RESPONSIVE // ELLIPSIS)
# =========================================================================

def generate_telemetry(metrics, is_dark=True):
    bg_color = '#0B0F17' if is_dark else '#F8FAFC'
    border_color = '#1E293B' if is_dark else '#E2E8F0'
    grid_color = '#1E293B' if is_dark else '#E2E8F0'
    card_bg = '#111827' if is_dark else '#FFFFFF'
    card_border = '#1F2937' if is_dark else '#E5E7EB'
    text_primary = '#F1F5F9' if is_dark else '#0F172A'
    text_secondary = '#94A3B8' if is_dark else '#475569'
    text_muted = '#64748B' if is_dark else '#94A3B8'
    accent_blue = '#38BDF8' if is_dark else '#0284C7'
    accent_emerald = '#34D399' if is_dark else '#059669'
    pill_bg = 'rgba(30, 41, 59, 0.6)' if is_dark else 'rgba(241, 245, 249, 0.8)'
    pill_border = '#334155' if is_dark else '#CBD5E1'

    tel = metrics['telemetry']
    months = tel['months']
    m_vals = tel['m_vals']
    rolling_avg = tel['rolling_avg']
    total_annual = tel['total_annual']
    avg_monthly = tel['avg_monthly']
    peak_val = tel['peak_val']
    peak_month = tel['peak_month']
    peak_idx = tel['peak_idx']
    scale_max = tel['scale_max']
    y_ticks = tel['y_ticks']
    pie_slices = tel['pie_slices']
    weekdays = tel['weekdays']
    peak_w_day = tel['peak_w_day']
    peak_w_pct = tel['peak_w_pct']

    # 1. Line Chart Plot
    plot_x = 72
    plot_w = 432
    plot_y = 115
    plot_h = 160
    base_y = 275

    coords = []
    for i, v in enumerate(m_vals):
        x = plot_x + (i / 11) * plot_w
        y = base_y - (v / scale_max) * plot_h
        coords.append((x, y))

    path_line = f'M {coords[0][0]:.1f} {coords[0][1]:.1f}'
    for x, y in coords[1:]:
        path_line += f' L {x:.1f} {y:.1f}'

    path_area = path_line + f' L {coords[-1][0]:.1f} {base_y} L {coords[0][0]:.1f} {base_y} Z'

    avg_coords = []
    for i, v in enumerate(rolling_avg):
        x = plot_x + (i / 11) * plot_w
        y = base_y - (v / scale_max) * plot_h
        avg_coords.append((x, y))
    path_avg = f'M {avg_coords[0][0]:.1f} {avg_coords[0][1]:.1f}'
    for x, y in avg_coords[1:]:
        path_avg += f' L {x:.1f} {y:.1f}'

    px, py = coords[peak_idx]
    badge_x = max(plot_x + 10, min(plot_x + plot_w - 76, px - 38))
    badge_y = max(60, py - 28)

    grid_lines = ''
    for yt in y_ticks:
        gy = base_y - (yt / scale_max) * plot_h
        grid_lines += f'<line x1="{plot_x}" y1="{gy:.1f}" x2="{plot_x + plot_w}" y2="{gy:.1f}" stroke="{grid_color}" stroke-width="0.8" stroke-dasharray="3 3"/>\n'
        grid_lines += f'<text x="{plot_x - 8}" y="{gy + 3.5:.1f}" text-anchor="end" font-family="\'JetBrains Mono\', monospace" font-size="8.5" fill="{text_muted}">{yt}</text>\n'

    x_labels = ''
    for i, m in enumerate(months):
        x = coords[i][0]
        x_labels += f'<text x="{x:.1f}" y="{base_y + 16}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="8" fill="{text_secondary}">{m}</text>\n'

    dots = ''
    for i, (x, y) in enumerate(coords):
        if i == peak_idx:
            dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{accent_blue}" stroke="{card_bg}" stroke-width="2"/>\n'
            dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="none" stroke="{accent_blue}" stroke-width="1.2" stroke-opacity="0.6"/>\n'
        else:
            dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{accent_blue}"/>\n'

    # 2. Pie Chart (Public + Private Codebases // NO REPO NAMES // TRUNCATED WITH ELLIPSIS)
    cx_pie = 618
    cy_pie = 126
    r_pie = 44
    current_angle = 0
    pie_paths = ''
    pie_legend = ''
    legend_y = 92
    sep_color = card_bg

    for sl in pie_slices:
        pct = sl['pct']
        color = sl['color']
        label = sl['name'] # already safely truncated with ellipsis
        deg = pct * 3.6
        if deg > 0:
            start_rad = math.radians(current_angle - 90)
            end_rad = math.radians(current_angle + deg - 90)
            x1 = cx_pie + r_pie * math.cos(start_rad)
            y1 = cy_pie + r_pie * math.sin(start_rad)
            x2 = cx_pie + r_pie * math.cos(end_rad)
            y2 = cy_pie + r_pie * math.sin(end_rad)
            large_arc = 1 if deg > 180 else 0
            d = f'M {cx_pie} {cy_pie} L {x1:.2f} {y1:.2f} A {r_pie} {r_pie} 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z'
            pie_paths += f'<path d="{d}" fill="{color}" stroke="{sep_color}" stroke-width="2"/>\n'

        pie_legend += f'''
        <g transform="translate(684, {legend_y})">
          <rect x="0" y="0" width="8" height="8" rx="2" fill="{color}"/>
          <text x="14" y="8" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="10.5" font-weight="600" fill="{text_primary}">{label}</text>
          <text x="234" y="8" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" fill="{color}">{pct}%</text>
        </g>
        '''
        legend_y += 18
        current_angle += deg

    # 3. Bar Chart (Weekday Distribution)
    bar_start_x = 566
    bar_slot_w = 48.5
    bar_w = 26
    bar_base_y = 330
    bar_max_h = 56
    max_w_pct = max([w['pct'] for w in weekdays] + [1])

    bars_svg = ''
    for i, w in enumerate(weekdays):
        bx = bar_start_x + i * bar_slot_w + (bar_slot_w - bar_w) / 2
        bh = (w['pct'] / max_w_pct) * bar_max_h if w['pct'] > 0 else 3
        by = bar_base_y - bh
        bcolor = accent_blue if w['is_peak'] else ('#334155' if is_dark else '#CBD5E1')
        tcolor = accent_blue if w['is_peak'] else text_primary

        bars_svg += f'<rect x="{bx:.1f}" y="{bar_base_y - bar_max_h}" width="{bar_w}" height="{bar_max_h}" rx="3" fill="{grid_color}" fill-opacity="0.35"/>\n'
        bars_svg += f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w}" height="{bh:.1f}" rx="3" fill="{bcolor}"/>\n'
        bars_svg += f'<text x="{bx + bar_w/2:.1f}" y="{by - 5:.1f}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="8" font-weight="600" fill="{tcolor}">{w["pct"]}%</text>\n'
        bars_svg += f'<text x="{bx + bar_w/2:.1f}" y="{bar_base_y + 14}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="8.5" font-weight="600" fill="{text_secondary}">{w["name"]}</text>\n'

    avg_y = bar_base_y - (14.3 / max_w_pct) * bar_max_h
    bars_svg += f'<line x1="{bar_start_x}" y1="{avg_y:.1f}" x2="{bar_start_x + 7 * bar_slot_w - 5}" y2="{avg_y:.1f}" stroke="{accent_emerald}" stroke-width="1" stroke-dasharray="3 3" stroke-opacity="0.8"/>\n'
    bars_svg += f'<text x="{bar_start_x + 7 * bar_slot_w - 2}" y="{avg_y + 3:.1f}" font-family="\'JetBrains Mono\', monospace" font-size="7.5" font-weight="600" fill="{accent_emerald}">AVG</text>\n'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 380" width="100%" height="100%">
  <defs>
    <linearGradient id="line_area_{'dark' if is_dark else 'light'}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{accent_blue}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="{accent_blue}" stop-opacity="0.0"/>
    </linearGradient>
  </defs>

  <rect width="958" height="378" x="1" y="1" rx="14" fill="{bg_color}" stroke="{border_color}" stroke-width="1.2"/>

  <!-- Top Header -->
  <text x="24" y="25" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="{accent_blue}" letter-spacing="1">ENGINEERING TELEMETRY &amp; METRICS</text>
  <text x="285" y="25" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" fill="{text_secondary}">// THROUGHPUT VELOCITY &amp; STACK COMPOSITION</text>

  <circle cx="934" cy="21" r="3.5" fill="{accent_emerald}"/>
  <text x="924" y="24" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="600" fill="{accent_emerald}">LIVE TELEMETRY</text>

  <!-- Left: Line Chart Panel (Bounded x=24..524) -->
  <rect x="24" y="44" width="500" height="316" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
  <text x="42" y="68" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="13" font-weight="700" fill="{text_primary}">Commit Velocity &amp; Cadence Trajectory</text>
  <text x="42" y="83" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">12-MONTH ACTIVITY // +{total_annual:,} COMMITS // {peak_val} PEAK</text>

  <!-- Line Chart Badge (Safe inside card bounds: 372 + 108 = 480 < 500) -->
  <g transform="translate(372, 54)">
    <rect width="108" height="22" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
    <circle cx="12" cy="11" r="3" fill="{accent_blue}"/>
    <text x="22" y="14.5" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="600" fill="{text_primary}">{avg_monthly} AVG / MO</text>
  </g>

  <!-- Plot Area -->
  {grid_lines}
  <path d="{path_area}" fill="url(#line_area_{'dark' if is_dark else 'light'})"/>
  <path d="{path_avg}" fill="none" stroke="{accent_emerald}" stroke-width="1.2" stroke-dasharray="4 4" stroke-opacity="0.7"/>
  <path d="{path_line}" fill="none" stroke="{accent_blue}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  {dots}
  {x_labels}

  <!-- Peak callout badge (Safely clamped inside plot area) -->
  <g transform="translate({badge_x:.1f}, {badge_y:.1f})">
    <rect width="76" height="20" rx="4" fill="{bg_color}" stroke="{accent_blue}" stroke-width="1"/>
    <text x="38" y="13.5" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" fill="{accent_blue}">{peak_month} PEAK {peak_val}</text>
  </g>

  <!-- Legend bottom -->
  <g transform="translate(44, 336)">
    <line x1="0" y1="6" x2="16" y2="6" stroke="{accent_blue}" stroke-width="2"/>
    <circle cx="8" cy="6" r="2" fill="{accent_blue}"/>
    <text x="22" y="9.5" font-family="'JetBrains Mono', monospace" font-size="8" fill="{text_secondary}">Monthly Volume</text>

    <line x1="130" y1="6" x2="146" y2="6" stroke="{accent_emerald}" stroke-width="1.2" stroke-dasharray="3 3"/>
    <text x="152" y="9.5" font-family="'JetBrains Mono', monospace" font-size="8" fill="{text_secondary}">Rolling Average</text>
  </g>

  <!-- Right: Top - Pie Chart Panel (Bounded x=542..936 // Truncated labels with ellipsis) -->
  <rect x="542" y="44" width="394" height="150" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
  <text x="558" y="68" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12.5" font-weight="700" fill="{text_primary}">Language Composition</text>
  <text x="558" y="82" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">PUBLIC &amp; PRIVATE CODEBASES // REALTIME COMPUTED</text>

  <!-- Pie Chart -->
  {pie_paths}
  {pie_legend}

  <!-- Right: Bottom - Bar Chart Panel (Bounded x=542..936) -->
  <rect x="542" y="210" width="394" height="150" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
  <text x="558" y="234" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12.5" font-weight="700" fill="{text_primary}">Commit Cadence by Weekday</text>
  <text x="558" y="248" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">HISTORICAL CADENCE // PEAK: {peak_w_day}</text>

  <!-- Badge (Safe bounds: 816 + 104 = 920 < 936) -->
  <g transform="translate(816, 222)">
    <rect width="104" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
    <circle cx="10" cy="10" r="2.5" fill="{accent_emerald}"/>
    <text x="18" y="13.5" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="{accent_emerald}">{peak_w_day} PEAK {peak_w_pct}%</text>
  </g>

  <!-- Bar Chart -->
  {bars_svg}
</svg>'''
    ET.fromstring(svg)
    return svg


# ==========================================
# MAIN EXECUTION
# ==========================================

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
generate_icons(base_dir)

# Fetch live real-time GitHub data
live_raw = get_live_github_data(base_dir)
if not live_raw:
    raise RuntimeError("Failed to obtain live GitHub data and no cache found.")

metrics = parse_metrics(live_raw)

# 1. Hero banner
with open(f"{base_dir}/assets/hero-banner-dark.svg", "w") as f:
    f.write(generate_hero_banner(True))
with open(f"{base_dir}/assets/hero-banner-light.svg", "w") as f:
    f.write(generate_hero_banner(False))

# 2. Activity & Overview (Real-time // 14-day velocity + Work Allocation Scope)
with open(f"{base_dir}/assets/overview-activity-dark.svg", "w") as f:
    f.write(generate_overview_activity(metrics, True))
with open(f"{base_dir}/assets/overview-activity-light.svg", "w") as f:
    f.write(generate_overview_activity(metrics, False))

# 3. Engineering Telemetry (Real-time Line, Pie with NO repo names, and Weekday Bar)
with open(f"{base_dir}/assets/telemetry-dark.svg", "w") as f:
    f.write(generate_telemetry(metrics, True))
with open(f"{base_dir}/assets/telemetry-light.svg", "w") as f:
    f.write(generate_telemetry(metrics, False))

print("Successfully generated all responsive, non-overflowing real-time visual assets!")
