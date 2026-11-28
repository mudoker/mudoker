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
    token = os.environ.get('GH_PAT') or os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not token:
        try:
            token = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True).stdout.strip()
        except Exception:
            token = None

    cache_file = os.path.join(base_dir, 'data', 'telemetry_cache.json')
    os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)

    cached_data = None
    if os.path.exists(cache_file):
        try:
            with open(cache_file) as f:
                cached_data = json.load(f)
        except Exception as e:
            print("Warning reading cache:", e)

    data = None
    if token:
        # 1. viewer query (returns full profile + private repos if PAT / personal token)
        # 2. user("mudoker") query (works with standard GITHUB_TOKEN in GitHub Actions)
        queries = [
            ('viewer', '''query {
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
    prs_merged: pullRequests(states: MERGED) { totalCount }
    prs_open: pullRequests(states: OPEN) { totalCount }
    prs_closed: pullRequests(states: CLOSED) { totalCount }
    issues_closed: issues(states: CLOSED) { totalCount }
    issues_open: issues(states: OPEN) { totalCount }
    repositories(ownerAffiliations: OWNER, first: 100, isFork: false) {
      nodes {
        name
        isPrivate
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}'''),
            ('user', '''query {
  user(login: "mudoker") {
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
    prs_merged: pullRequests(states: MERGED) { totalCount }
    prs_open: pullRequests(states: OPEN) { totalCount }
    prs_closed: pullRequests(states: CLOSED) { totalCount }
    issues_closed: issues(states: CLOSED) { totalCount }
    issues_open: issues(states: OPEN) { totalCount }
    repositories(ownerAffiliations: OWNER, first: 100, isFork: false) {
      nodes {
        name
        isPrivate
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}''')
        ]

        for q_type, query in queries:
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
                    if 'data' in raw_json and raw_json['data'] and raw_json['data'].get(q_type):
                        res_obj = raw_json['data'][q_type]
                        if res_obj.get('login') == 'mudoker':
                            data = res_obj
                            print(f"Successfully fetched live data via '{q_type}' query.")
                            break
                    if 'errors' in raw_json:
                        print(f"GraphQL {q_type} notices:", [err.get('message') for err in raw_json['errors']])
            except Exception as e:
                print(f"Live GraphQL {q_type} fetch error:", e)

    if data:
        # If private repos are not visible in this query (e.g. running via bot GITHUB_TOKEN) but exist in cache, preserve them
        if cached_data:
            live_repos = data.get('repositories', {}).get('nodes', [])
            has_private = any(r.get('isPrivate') for r in live_repos)
            if not has_private:
                cached_repos = cached_data.get('repositories', {}).get('nodes', [])
                cached_private = [r for r in cached_repos if r.get('isPrivate')]
                if cached_private:
                    live_names = {r['name'] for r in live_repos}
                    for pr in cached_private:
                        if pr['name'] not in live_names:
                            live_repos.append(pr)
                    data['repositories']['nodes'] = live_repos

        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
    elif cached_data:
        print("Using cached data fallback.")
        data = cached_data

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

    # Real-time Pull Request Delivery & Issue Lifecycle (Meaningful, Non-Commit Metrics)
    prs_merged = data.get('prs_merged', {}).get('totalCount', 271)
    prs_open = data.get('prs_open', {}).get('totalCount', 4)
    prs_closed = data.get('prs_closed', {}).get('totalCount', 43)
    total_prs = prs_merged + prs_open + prs_closed or 318
    pr_merge_rate = round((prs_merged / total_prs) * 100, 1)

    issues_closed = data.get('issues_closed', {}).get('totalCount', 37)
    issues_open = data.get('issues_open', {}).get('totalCount', 33)
    total_issues = issues_closed + issues_open or 70
    issue_res_rate = round((issues_closed / total_issues) * 100, 1)
    total_deliveries = prs_merged + issues_closed

    delivery_data = {
        'prs_merged': prs_merged,
        'prs_open': prs_open,
        'prs_closed': prs_closed,
        'total_prs': total_prs,
        'pr_merge_rate': pr_merge_rate,
        'issues_closed': issues_closed,
        'issues_open': issues_open,
        'total_issues': total_issues,
        'issue_res_rate': issue_res_rate,
        'total_deliveries': total_deliveries
    }

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

    # 3. Language Breakdown across BOTH public and private repositories (Recognizing Rust and core languages)
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

    featured = []
    featured_names = set()
    for l, b in sorted_code:
        if len(featured) < 4:
            featured.append((l, b))
            featured_names.add(l)

    # Recognize Rust and common languages explicitly
    if 'Rust' in code_bytes and 'Rust' not in featured_names:
        featured.append(('Rust', code_bytes['Rust']))
        featured_names.add('Rust')
    else:
        for l, b in sorted_code:
            if l not in featured_names and len(featured) < 5:
                featured.append((l, b))
                featured_names.add(l)

    palette_map = {
        'C': '#38BDF8',
        'TypeScript': '#34D399',
        'Go': '#A78BFA',
        'Python': '#FBBF24',
        'Rust': '#FB923C',
        'C++': '#60A5FA',
        'JavaScript': '#FCD34D',
        'Other': '#94A3B8'
    }

    top_langs = []
    covered = 0
    for l, b in featured:
        pct = round((b / total_code) * 100)
        if b > 0 and pct == 0:
            pct = 1  # Ensure active recognized language is visually represented
        covered += pct
        top_langs.append({'name': truncate_ellipsis(l, 14), 'pct': pct, 'bytes': b, 'color': palette_map.get(l, '#38BDF8')})

    other_pct = max(0, 100 - covered)
    top_langs.append({'name': 'Other', 'pct': other_pct, 'bytes': 0, 'color': palette_map['Other']})

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
            'delivery': delivery_data,
            'scope': scope_data
        },
        'telemetry': {
            'days_14': days_14,
            'avg_14': avg_14,
            'consistency_14': consistency_14,
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

W_GLOBE = 800
H_GLOBE = 340
cx_globe = 875
cy_globe = 130
r_globe = 175

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

def point_in_poly(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# ==========================================
# 1. HERO BANNER WITH ROTATING 3D DOTTED GLOBE
# ==========================================

cx_globe = 875
cy_globe = 130
r_globe = 175
tilt_rad = math.radians(15)

# Sample dense land points (step 3.0 lat, 4.0 lon) -> ~1,200 points
land_matrix_points = []
for lat in range(-56, 75, 3):
    for lon in range(-180, 180, 4):
        for name, poly in continents_data.items():
            if point_in_poly(lon, lat, poly):
                land_matrix_points.append((lon, lat))
                break

# Sparse ocean/sphere grid matrix points (step 15 lat, 15 lon)
ocean_grid_points = []
for lat in range(-75, 80, 15):
    for lon in range(-180, 180, 15):
        ocean_grid_points.append((lon, lat))

# Precompute 12 keyframes for 3D orthographic projection around 360 rotation
NUM_GLOBE_KF = 12
d_land_keyframes = []
d_grid_keyframes = []
vn_cx_kf = []
vn_cy_kf = []
vn_op_kf = []

vn_phi = math.radians(10.82)
vn_lon = 106.63

for k in range(NUM_GLOBE_KF):
    rot = -2 * math.pi * k / NUM_GLOBE_KF

    # 1. Land Dotted Matrix
    l_cmds = []
    for lon, lat in land_matrix_points:
        phi = math.radians(lat)
        lam = math.radians(lon - vn_lon) + rot
        x3 = r_globe * math.cos(phi) * math.sin(lam)
        y3 = -r_globe * math.sin(phi)
        z3 = r_globe * math.cos(phi) * math.cos(lam)

        x = cx_globe + x3
        y = cy_globe + y3 * math.cos(tilt_rad) - z3 * math.sin(tilt_rad)
        z = y3 * math.sin(tilt_rad) + z3 * math.cos(tilt_rad)

        r = round((1.1 + 1.3 * (z / r_globe)), 1) if z > 0 else 0.01
        l_cmds.append(f'M{x:.0f} {y:.0f}m-{r} 0a{r} {r} 0 1 0 {2*r:.1f} 0a{r} {r} 0 1 0 -{2*r:.1f} 0')
    d_land_keyframes.append(''.join(l_cmds))

    # 2. Ocean/Surface Grid Matrix
    g_cmds = []
    for lon, lat in ocean_grid_points:
        phi = math.radians(lat)
        lam = math.radians(lon - vn_lon) + rot
        x3 = r_globe * math.cos(phi) * math.sin(lam)
        y3 = -r_globe * math.sin(phi)
        z3 = r_globe * math.cos(phi) * math.cos(lam)

        x = cx_globe + x3
        y = cy_globe + y3 * math.cos(tilt_rad) - z3 * math.sin(tilt_rad)
        z = y3 * math.sin(tilt_rad) + z3 * math.cos(tilt_rad)

        r = round((0.7 + 0.6 * (z / r_globe)), 1) if z > 0 else 0.01
        g_cmds.append(f'M{x:.0f} {y:.0f}m-{r} 0a{r} {r} 0 1 0 {2*r:.1f} 0a{r} {r} 0 1 0 -{2*r:.1f} 0')
    d_grid_keyframes.append(''.join(g_cmds))

    # 3. Vietnam Location Beacon
    vx3 = r_globe * math.cos(vn_phi) * math.sin(rot)
    vy3 = -r_globe * math.sin(vn_phi)
    vz3 = r_globe * math.cos(vn_phi) * math.cos(rot)
    vx = cx_globe + vx3
    vy = cy_globe + vy3 * math.cos(tilt_rad) - vz3 * math.sin(tilt_rad)
    vz = vy3 * math.sin(tilt_rad) + vz3 * math.cos(tilt_rad)
    vn_cx_kf.append(f'{vx:.1f}')
    vn_cy_kf.append(f'{vy:.1f}')
    vn_op_kf.append('1.0' if vz > 10 else ('0.4' if vz > 0 else '0.0'))

# Loop keyframes
d_land_keyframes.append(d_land_keyframes[0])
d_grid_keyframes.append(d_grid_keyframes[0])
vn_cx_kf.append(vn_cx_kf[0])
vn_cy_kf.append(vn_cy_kf[0])
vn_op_kf.append(vn_op_kf[0])

all_land_d = ';'.join(d_land_keyframes)
all_grid_d = ';'.join(d_grid_keyframes)
all_vn_cx = ';'.join(vn_cx_kf)
all_vn_cy = ';'.join(vn_cy_kf)
all_vn_op = ';'.join(vn_op_kf)
all_vn_tx = ';'.join([f'{float(x)+11:.1f}' for x in vn_cx_kf])
all_vn_ty = ';'.join([f'{float(y)-5:.1f}' for y in vn_cy_kf])

def generate_hero_banner(is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    grid_color = "#162032" if is_dark else "#E2E8F0"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#64748B"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    accent_red = "#EF4444" # Vibrant Red Beacon
    dot_land_color = "#38BDF8" if is_dark else "#0284C7"
    dot_grid_color = "#1E3A5F" if is_dark else "#93C5FD"
    sphere_bg = "#090D14" if is_dark else "#F1F5F9"
    badge_bg = "rgba(30, 41, 59, 0.7)" if is_dark else "rgba(241, 245, 249, 0.9)"
    badge_border = "#334155" if is_dark else "#CBD5E1"
    grid_stroke = "#1E293B" if is_dark else "#E2E8F0"

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
      <stop offset="0%" stop-color="{'#1E293B' if is_dark else '#FFFFFF'}" stop-opacity="0.0"/>
      <stop offset="60%" stop-color="{'#000000' if is_dark else '#CBD5E1'}" stop-opacity="{'0.35' if is_dark else '0.12'}"/>
      <stop offset="100%" stop-color="{'#000000' if is_dark else '#94A3B8'}" stop-opacity="{'0.85' if is_dark else '0.38'}"/>
    </radialGradient>
  </defs>

  <g clip-path="url(#banner_clip_{'dark' if is_dark else 'light'})">
    <rect width="958" height="318" x="1" y="1" fill="{bg_color}"/>
    <rect width="958" height="318" x="1" y="1" fill="url(#grid_{'dark' if is_dark else 'light'})"/>

    <!-- Corner Overflow Rotating 3D Dotted World Globe (Bigger: r=175 at cx=875, cy=130) -->
    <circle cx="{cx_globe}" cy="{cy_globe}" r="{r_globe + 45}" fill="url(#globe_glow_{'dark' if is_dark else 'light'})"/>
    <ellipse cx="{cx_globe}" cy="{cy_globe}" rx="{r_globe + 40}" ry="50" fill="none" stroke="{accent_blue}" stroke-width="1.2" stroke-opacity="0.35" stroke-dasharray="5 7" transform="rotate(-20 {cx_globe} {cy_globe})"/>
    <circle cx="{cx_globe}" cy="{cy_globe}" r="{r_globe + 6}" fill="none" stroke="{accent_blue}" stroke-width="1.5" stroke-opacity="0.25"/>
    <circle cx="{cx_globe}" cy="{cy_globe}" r="{r_globe}" fill="{sphere_bg}" stroke="{accent_blue}" stroke-width="1.8" stroke-opacity="0.85"/>

    <g clip-path="url(#globe_mask_{'dark' if is_dark else 'light'})">
      <!-- 1. Rotating 3D Ocean / Spherical Grid Matrix -->
      <path fill="{dot_grid_color}" fill-opacity="0.45" d="{d_grid_keyframes[0]}">
        <animate attributeName="d" dur="12s" repeatCount="indefinite" values="{all_grid_d}"/>
      </path>

      <!-- 2. Rotating 3D Dotted Landmasses (NO POLYGON OUTLINES, PURE DOTTED MESH) -->
      <path fill="{dot_land_color}" d="{d_land_keyframes[0]}">
        <animate attributeName="d" dur="12s" repeatCount="indefinite" values="{all_land_d}"/>
      </path>

      <!-- 3. Spherical 3D Shading for volumetric realism -->
      <circle cx="{cx_globe}" cy="{cy_globe}" r="{r_globe}" fill="url(#sphere_shading_{'dark' if is_dark else 'light'})"/>

      <!-- 4. Vibrant Red Beacon (Vietnam) - Pulsing Radar Ring & Location Marker in 3D -->
      <g>
        <circle cx="{vn_cx_kf[0]}" cy="{vn_cy_kf[0]}" r="4.5" fill="{accent_red}">
          <animate attributeName="cx" dur="12s" repeatCount="indefinite" values="{all_vn_cx}"/>
          <animate attributeName="cy" dur="12s" repeatCount="indefinite" values="{all_vn_cy}"/>
          <animate attributeName="opacity" dur="12s" repeatCount="indefinite" values="{all_vn_op}"/>
        </circle>
        <circle cx="{vn_cx_kf[0]}" cy="{vn_cy_kf[0]}" r="9" fill="none" stroke="{accent_red}" stroke-width="1.6">
          <animate attributeName="cx" dur="12s" repeatCount="indefinite" values="{all_vn_cx}"/>
          <animate attributeName="cy" dur="12s" repeatCount="indefinite" values="{all_vn_cy}"/>
          <animate attributeName="opacity" dur="12s" repeatCount="indefinite" values="{all_vn_op}"/>
          <animate attributeName="r" values="4.5;16;4.5" dur="1.6s" repeatCount="indefinite"/>
          <animate attributeName="stroke-opacity" values="1;0;1" dur="1.6s" repeatCount="indefinite"/>
        </circle>
        <text x="{float(vn_cx_kf[0]) + 11:.1f}" y="{float(vn_cy_kf[0]) - 5:.1f}" font-family="'JetBrains Mono', Consolas, monospace" font-size="9.5" font-weight="700" fill="{accent_red}" letter-spacing="0.5">VN
          <animate attributeName="x" dur="12s" repeatCount="indefinite" values="{all_vn_tx}"/>
          <animate attributeName="y" dur="12s" repeatCount="indefinite" values="{all_vn_ty}"/>
          <animate attributeName="opacity" dur="12s" repeatCount="indefinite" values="{all_vn_op}"/>
        </text>
      </g>
    </g>

    <text x="{cx_globe}" y="292" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="{accent_blue}" letter-spacing="1">10.82°N, 106.63°E • VN</text>
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
# 2. ACTIVITY & OVERVIEW (PR LIFECYCLE THROUGHPUT & WORK ALLOCATION SCOPE)
# =========================================================================

def generate_overview_activity(metrics, is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    card_bg = "#111827" if is_dark else "#FFFFFF"
    card_border = "#1F2937" if is_dark else "#E5E7EB"
    grid_color = "#1E293B" if is_dark else "#E2E8F0"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#94A3B8"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    accent_purple = "#A78BFA" if is_dark else "#7C3AED"
    pill_bg = "rgba(30, 41, 59, 0.6)" if is_dark else "rgba(241, 245, 249, 0.8)"
    pill_border = "#334155" if is_dark else "#CBD5E1"
    node_bg = "rgba(15, 23, 42, 0.65)" if is_dark else "rgba(241, 245, 249, 0.9)"
    node_border = "#334155" if is_dark else "#CBD5E1"

    ov = metrics['overview']
    scope = ov['scope']

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
  <defs>
    <radialGradient id="lens_glow_{'dark' if is_dark else 'light'}" cx="60%" cy="50%" r="60%">
      <stop offset="0%" stop-color="{accent_blue}" stop-opacity="{'0.75' if is_dark else '0.45'}"/>
      <stop offset="45%" stop-color="{accent_blue}" stop-opacity="{'0.3' if is_dark else '0.15'}"/>
      <stop offset="100%" stop-color="{accent_blue}" stop-opacity="0.0"/>
    </radialGradient>
    <clipPath id="lens_clip_{'dark' if is_dark else 'light'}">
      <circle cx="76" cy="90" r="32"/>
    </clipPath>
  </defs>

  <rect width="958" height="214" x="1" y="1" rx="14" fill="{bg_color}" stroke="{border_color}" stroke-width="1.2"/>

  <!-- Top Title -->
  <text x="24" y="25" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="{accent_blue}" letter-spacing="1">ENGINEERING DOMAINS &amp; SCOPE</text>
  <text x="250" y="25" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" fill="{text_secondary}">// CORE PRINCIPLES &amp; PRODUCTION ALLOCATION</text>

  <!-- Left: Engineering Principles & Domains (Geometric Synthesis Inspired by Design Reference) -->
  <g transform="translate(24, 42)">
    <rect width="450" height="152" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    
    <!-- Header -->
    <text x="18" y="21" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" font-weight="700" fill="{text_primary}">Engineering Principles &amp; Domains</text>
    <text x="18" y="34" font-family="'JetBrains Mono', monospace" font-size="8" fill="{text_secondary}">CONVERGENT ARCHITECTURES // CORE SPECIALIZATIONS</text>

    <!-- Top-Right Status -->
    <g transform="translate(304, 12)">
      <rect width="128" height="18" rx="3.5" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <circle cx="10" cy="9" r="2.5" fill="{accent_blue}"/>
      <text x="18" y="12.5" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="600" fill="{text_primary}">3 CORE PRINCIPLES</text>
    </g>

    <!-- LEFT: Geometric Overlapping Lens / Synthesis Geometry (Inspired by Reference) -->
    <g transform="translate(0, 0)">
      <!-- Crosshairs & Grid Guideliness -->
      <line x1="20" y1="90" x2="136" y2="90" stroke="{text_muted}" stroke-width="0.6" stroke-dasharray="3 3" stroke-opacity="0.35"/>
      <line x1="76" y1="44" x2="76" y2="136" stroke="{text_muted}" stroke-width="0.6" stroke-dasharray="3 3" stroke-opacity="0.35"/>

      <!-- Overlapping Circles (Radius 26) -->
      <!-- Systems Circle (Top-Left) -->
      <circle cx="65" cy="78" r="26" fill="none" stroke="{accent_blue}" stroke-width="0.9" stroke-opacity="0.45"/>
      
      <!-- Architecture Circle (Top-Right) -->
      <circle cx="87" cy="78" r="26" fill="none" stroke="{accent_emerald}" stroke-width="0.9" stroke-opacity="0.45"/>
      
      <!-- AI Circle (Bottom) with Glowing Lens Fill -->
      <circle cx="76" cy="100" r="26" fill="none" stroke="{accent_purple}" stroke-width="0.9" stroke-opacity="0.45"/>

      <!-- Ethereal Glowing Lens on Right Half -->
      <g clip-path="url(#lens_clip_{'dark' if is_dark else 'light'})">
        <ellipse cx="76" cy="90" rx="22" ry="32" fill="url(#lens_glow_{'dark' if is_dark else 'light'})"/>
      </g>

      <!-- Center Convergence Core Dot -->
      <circle cx="76" cy="85" r="3" fill="{text_primary}"/>
      <circle cx="76" cy="85" r="6" fill="none" stroke="{accent_blue}" stroke-width="0.8" stroke-opacity="0.8"/>

      <!-- Domain Tiny Pips -->
      <text x="50" y="66" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="600" fill="{accent_blue}">SYS</text>
      <text x="102" y="66" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="600" fill="{accent_emerald}">ARCH</text>
      <text x="76" y="130" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="600" fill="{accent_purple}">AI</text>
    </g>

    <!-- RIGHT: 3 Domain Cards -->
    <!-- 01 Systems -->
    <g transform="translate(144, 44)">
      <rect width="288" height="28" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <circle cx="12" cy="14" r="3" fill="{accent_blue}"/>
      <text x="22" y="13" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="9" font-weight="700" fill="{text_primary}">Systems Engineering</text>
      <text x="22" y="23" font-family="'JetBrains Mono', monospace" font-size="7" fill="{text_secondary}">Linux &#8226; C &#8226; Go &#8226; Performance</text>
      <text x="278" y="18" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" fill="{accent_blue}">01</text>
    </g>

    <!-- 02 Architecture -->
    <g transform="translate(144, 77)">
      <rect width="288" height="28" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <circle cx="12" cy="14" r="3" fill="{accent_emerald}"/>
      <text x="22" y="13" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="9" font-weight="700" fill="{text_primary}">Software Architecture</text>
      <text x="22" y="23" font-family="'JetBrains Mono', monospace" font-size="7" fill="{text_secondary}">Backend &#8226; Full-Stack &#8226; Distributed Systems</text>
      <text x="278" y="18" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" fill="{accent_emerald}">02</text>
    </g>

    <!-- 03 Applied AI -->
    <g transform="translate(144, 110)">
      <rect width="288" height="28" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <circle cx="12" cy="14" r="3" fill="{accent_purple}"/>
      <text x="22" y="13" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="9" font-weight="700" fill="{text_primary}">Applied Intelligence</text>
      <text x="22" y="23" font-family="'JetBrains Mono', monospace" font-size="7" fill="{text_secondary}">Multimodal &#8226; Inference &#8226; Machine Learning</text>
      <text x="278" y="18" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" fill="{accent_purple}">03</text>
    </g>
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
      <text x="212" y="14" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="{text_secondary}">{scope['total_repos']} MONITORED SYSTEMS</text>

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

    # 2. Pie Chart (Public + Private Codebases // NO REPO NAMES // 2-COLUMN LEGEND WITH SPACED LAYOUT)
    cx_pie = 604
    cy_pie = 135
    r_pie = 38
    current_angle = 0
    pie_paths = ''
    sep_color = card_bg

    for sl in pie_slices:
        pct = sl['pct']
        color = sl['color']
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
        current_angle += deg

    # 2-column balanced legend: up to 3 rows with clear breathing room
    pie_legend = ''
    col1_x = 662
    col2_x = 794
    y_starts = [110, 131, 152]

    for idx, sl in enumerate(pie_slices):
        col_x = col1_x if idx < 3 else col2_x
        row_y = y_starts[idx % 3]
        color = sl['color']
        label = sl['name']
        pct = sl['pct']
        pie_legend += f'''
        <g transform="translate({col_x}, {row_y})">
          <rect x="0" y="0" width="7" height="7" rx="2" fill="{color}"/>
          <text x="13" y="7.5" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="9.5" font-weight="600" fill="{text_primary}">{label}</text>
          <text x="115" y="7.5" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="9.5" font-weight="700" fill="{color}">{pct}%</text>
        </g>
        '''

    # 3. 14-Day Velocity Cadence Bar Chart (Bounded x=542..936, PERFECT SYMMETRIC MARGINS, ZERO OVERFLOW)
    days_14 = tel['days_14']
    avg_14 = tel['avg_14']
    consistency_14 = tel['consistency_14']
    max_c = max([d['count'] for d in days_14] + [1])

    # Card is x=542, width=394 -> right edge=936
    # 18px symmetric inner padding: x=560 to 918 -> 358px total
    bar_start_x = 560
    bar_slot_w = 358.0 / 14.0 # 25.5714px
    bar_w = 14
    bar_offset = (bar_slot_w - bar_w) / 2 # 5.7857px
    base_y = 330
    max_h = 52

    chart_bars = ""
    for i, d in enumerate(days_14):
        bx = bar_start_x + i * bar_slot_w + bar_offset
        bh = (d['count'] / max_c) * max_h if d['count'] > 0 else 3
        by = base_y - bh
        color = accent_blue if d['is_peak'] else (accent_emerald if d['count'] > 0 else ("#334155" if is_dark else "#CBD5E1"))
        tcolor = accent_blue if d['is_peak'] else text_primary

        chart_bars += f'<rect x="{bx:.1f}" y="{base_y - max_h}" width="{bar_w}" height="{max_h}" rx="2.5" fill="{grid_color}" fill-opacity="0.35"/>\n'
        chart_bars += f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w}" height="{bh:.1f}" rx="2.5" fill="{color}"/>\n'
        if d['count'] > 0:
            chart_bars += f'<text x="{bx + bar_w/2:.1f}" y="{by - 4:.1f}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="7.5" font-weight="600" fill="{tcolor}">{d["count"]}</text>\n'
        chart_bars += f'<text x="{bx + bar_w/2:.1f}" y="{base_y + 13}" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="7.5" font-weight="500" fill="{text_secondary}">{d["date"]}</text>\n'

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
  <text x="558" y="66" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12.5" font-weight="700" fill="{text_primary}">Language Composition</text>
  <text x="558" y="78" font-family="'JetBrains Mono', monospace" font-size="8.5" fill="{text_secondary}">PUBLIC &amp; PRIVATE CODEBASES // REALTIME COMPUTED</text>

  <!-- Pie Chart -->
  {pie_paths}
  {pie_legend}

  <!-- Right: Bottom - 14-Day Velocity Cadence Panel (Bounded x=542..936 // SYMMETRIC MARGINS // ZERO OVERFLOW) -->
  <rect x="542" y="210" width="394" height="150" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
  <text x="558" y="234" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12.5" font-weight="700" fill="{text_primary}">14-Day Velocity Cadence</text>
  <text x="558" y="248" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">DAILY SPRINT OUTPUT // RECENT VELOCITY</text>

  <!-- Badge (Safe bounds: 772 + 152 = 924 < 936) -->
  <g transform="translate(772, 222)">
    <rect width="72" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
    <circle cx="10" cy="10" r="2.5" fill="{accent_blue}"/>
    <text x="18" y="13.5" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="{text_primary}">{avg_14} / DAY</text>

    <rect x="78" y="0" width="74" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
    <circle cx="88" cy="10" r="2.5" fill="{accent_emerald}"/>
    <text x="96" y="13.5" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="{text_primary}">{consistency_14}% ACTIVE</text>
  </g>

  <!-- 14-Day Velocity Bars -->
  {chart_bars}
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
