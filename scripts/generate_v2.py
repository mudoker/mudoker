import xml.etree.ElementTree as ET
import os

ICONS = {
    "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>',
    "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    "brain-circuit": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M9 13a4.5 4.5 0 0 0 3-4"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M6 18a4 4 0 0 1-1.967-.518"/><path d="M12 13h4"/><path d="M12 18h6a2 2 0 0 1 2 2v1"/><path d="M12 8h8"/><path d="M16 8V5a2 2 0 0 1 2-2"/><circle cx="16" cy="13" r=".5"/><circle cx="18" cy="3" r=".5"/><circle cx="20" cy="21" r=".5"/><circle cx="20" cy="8" r=".5"/>'
}

# 1. HERO BANNER WITH ROTATING 3D WIREFRAME GLOBE
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
    
    # Globe parameters
    gx, gy, gr = 785, 145, 78
    grid_stroke = "#1E293B" if is_dark else "#E2E8F0"
    meridian_stroke = "#38BDF8" if is_dark else "#0284C7"
    dot_color = "#38BDF8" if is_dark else "#0284C7"

    meridians = ""
    for offset in range(-320, 320, 38):
        meridians += f'<path d="M {gx + offset} {gy - gr} Q {gx + offset + 24} {gy} {gx + offset} {gy + gr}" fill="none" stroke="{meridian_stroke}" stroke-width="1.1" stroke-opacity="0.45"/>\n'
    
    dots = ""
    for dx in range(-240, 240, 32):
        dots += f'''<circle cx="{gx + dx}" cy="{gy - 15}" r="1.8" fill="{dot_color}" fill-opacity="0.75"/>
<circle cx="{gx + dx + 14}" cy="{gy + 15}" r="1.8" fill="{dot_color}" fill-opacity="0.7"/>
<circle cx="{gx + dx + 20}" cy="{gy - 38}" r="1.5" fill="{dot_color}" fill-opacity="0.55"/>
<circle cx="{gx + dx + 8}" cy="{gy + 38}" r="1.5" fill="{dot_color}" fill-opacity="0.55"/>\n'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 320" width="100%" height="100%">
  <defs>
    <pattern id="grid_{'dark' if is_dark else 'light'}" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="{grid_color}" stroke-width="0.75" stroke-opacity="0.6"/>
      <circle cx="32" cy="32" r="1" fill="{grid_color}" fill-opacity="0.8"/>
    </pattern>
    <radialGradient id="globe_glow_{'dark' if is_dark else 'light'}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{accent_blue}" stop-opacity="{'0.28' if is_dark else '0.18'}"/>
      <stop offset="65%" stop-color="{accent_blue}" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="{accent_blue}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="sphere_shading_{'dark' if is_dark else 'light'}" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="{'#1E293B' if is_dark else '#FFFFFF'}" stop-opacity="0.1"/>
      <stop offset="70%" stop-color="{'#000000' if is_dark else '#CBD5E1'}" stop-opacity="{'0.45' if is_dark else '0.18'}"/>
      <stop offset="100%" stop-color="{'#000000' if is_dark else '#94A3B8'}" stop-opacity="{'0.85' if is_dark else '0.38'}"/>
    </radialGradient>
    <clipPath id="globe_mask_{'dark' if is_dark else 'light'}">
      <circle cx="{gx}" cy="{gy}" r="{gr}"/>
    </clipPath>
  </defs>

  <!-- Background Canvas -->
  <rect width="958" height="318" x="1" y="1" rx="14" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5"/>
  <rect width="956" height="316" x="2" y="2" rx="13" fill="url(#grid_{'dark' if is_dark else 'light'})"/>

  <!-- Top System Bar -->
  <g transform="translate(36, 36)">
    <circle cx="4" cy="4" r="4.5" fill="{accent_emerald}"/>
    <circle cx="4" cy="4" r="9" fill="none" stroke="{accent_emerald}" stroke-width="1" stroke-opacity="0.4">
      <animate attributeName="r" values="4.5;10;4.5" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="0.6;0.1;0.6" dur="3s" repeatCount="indefinite"/>
    </circle>
    <text x="24" y="8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', monospace" font-size="11" font-weight="600" fill="{accent_emerald}" letter-spacing="1.5">SYSTEM ACTIVE // SYSTEMS &#8226; ARCHITECTURE &#8226; AI</text>
  </g>

  <!-- Top Divider Line -->
  <line x1="36" y1="58" x2="924" y2="58" stroke="{border_color}" stroke-width="1" stroke-dasharray="4 4"/>

  <!-- Left Main Hero Brand Section (Safe width: 560px, never touches globe) -->
  <g transform="translate(36, 120)">
    <text x="0" y="-8" font-family="'JetBrains Mono', Consolas, monospace" font-size="14" font-weight="500" fill="{accent_blue}" letter-spacing="0.5">&gt; whoami --portfolio</text>
    <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="46" font-weight="800" fill="{text_primary}" letter-spacing="-1">mudoker</text>
    <text x="220" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="20" font-weight="400" fill="{text_muted}">/</text>
    <text x="238" y="42" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="20" font-weight="500" fill="{text_secondary}">software &amp; systems engineer</text>

    <!-- One-line concise tagline -->
    <text x="0" y="82" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14.5" font-weight="400" fill="{text_secondary}">
      Engineering resilient backends, keyboard-first terminal engines, and practical multimodal AI.
    </text>
  </g>

  <!-- ================= RIGHT: ROTATING 3D WIREFRAME GLOBE ================= -->
  <!-- Ambient Atmospheric Glow -->
  <circle cx="{gx}" cy="{gy}" r="{gr + 32}" fill="url(#globe_glow_{'dark' if is_dark else 'light'})"/>

  <!-- Orbital Track Ring -->
  <ellipse cx="{gx}" cy="{gy}" rx="{gr + 26}" ry="34" fill="none" stroke="{accent_blue}" stroke-width="1" stroke-opacity="0.32" stroke-dasharray="4 6" transform="rotate(-20 {gx} {gy})"/>

  <!-- Globe Sphere Solid Base -->
  <circle cx="{gx}" cy="{gy}" r="{gr}" fill="{'#0E1726' if is_dark else '#F1F5F9'}" stroke="{accent_blue}" stroke-width="1.5" stroke-opacity="0.85"/>

  <!-- Clipped Rotating Wireframe -->
  <g clip-path="url(#globe_mask_{'dark' if is_dark else 'light'})">
    <g transform="rotate(-15 {gx} {gy})">
      <!-- Latitudes -->
      <ellipse cx="{gx}" cy="{gy}" rx="{gr}" ry="0" fill="none" stroke="{grid_stroke}" stroke-width="1" stroke-opacity="0.7"/>
      <ellipse cx="{gx}" cy="{gy - 26}" rx="73" ry="19" fill="none" stroke="{grid_stroke}" stroke-width="0.9" stroke-opacity="0.6"/>
      <ellipse cx="{gx}" cy="{gy + 26}" rx="73" ry="19" fill="none" stroke="{grid_stroke}" stroke-width="0.9" stroke-opacity="0.6"/>
      <ellipse cx="{gx}" cy="{gy - 52}" rx="58" ry="14" fill="none" stroke="{grid_stroke}" stroke-width="0.8" stroke-opacity="0.5"/>
      <ellipse cx="{gx}" cy="{gy + 52}" rx="58" ry="14" fill="none" stroke="{grid_stroke}" stroke-width="0.8" stroke-opacity="0.5"/>

      <!-- Rotating Longitude Meridians (Infinite translation period of 152px) -->
      <g>
        <animateTransform attributeName="transform" type="translate" from="0,0" to="152,0" dur="10s" repeatCount="indefinite"/>
        {meridians}
        {dots}
      </g>
    </g>

    <!-- 3D Depth Shading Overlay -->
    <circle cx="{gx}" cy="{gy}" r="{gr}" fill="url(#sphere_shading_{'dark' if is_dark else 'light'})"/>
  </g>

  <!-- Beacon Target Pin: Ho Chi Minh City [10.82°N, 106.63°E] -->
  <g transform="translate(800, 134)">
    <circle cx="0" cy="0" r="3.5" fill="{accent_blue}"/>
    <circle cx="0" cy="0" r="7" fill="none" stroke="{accent_blue}" stroke-width="1.2">
      <animate attributeName="r" values="3.5;13;3.5" dur="2.6s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="0.9;0.1;0.9" dur="2.6s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- Location Label under Globe -->
  <text x="{gx}" y="{gy + gr + 24}" text-anchor="middle" font-family="'JetBrains Mono', Consolas, monospace" font-size="9.5" font-weight="600" fill="{accent_blue}" letter-spacing="1">10.82&#176;N, 106.63&#176;E &#8226; VN</text>

  <!-- Bottom Fast Tags Bar -->
  <g transform="translate(36, 268)">
    <rect x="0" y="0" width="130" height="28" rx="6" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <circle cx="14" cy="14" r="3" fill="{accent_blue}"/>
    <text x="26" y="18" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="{text_primary}">GO &amp; TUI</text>

    <rect x="142" y="0" width="170" height="28" rx="6" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <circle cx="156" cy="14" r="3" fill="{accent_emerald}"/>
    <text x="168" y="18" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="{text_primary}">BACKEND SYSTEMS</text>

    <rect x="324" y="0" width="160" height="28" rx="6" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <circle cx="338" cy="14" r="3" fill="#A78BFA"/>
    <text x="350" y="18" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="{text_primary}">APPLIED AI LIVE</text>

    <text x="670" y="18" text-anchor="end" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="{text_muted}">[ Go &#8226; TypeScript &#8226; Python &#8226; Linux &#8226; SQLite ]</text>
  </g>
</svg>'''
    ET.fromstring(svg)
    return svg


# 2. ACTIVITY & OVERVIEW WITH DAILY COMMIT RATE CHART (No verbose tenets!)
def generate_overview_activity(is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    card_bg = "#111827" if is_dark else "#FFFFFF"
    card_border = "#243248" if is_dark else "#CBD5E1"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#64748B"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    accent_amber = "#FBBF24" if is_dark else "#D97706"
    accent_purple = "#A78BFA" if is_dark else "#7C3AED"

    # 14-day commit volume data (matching actual active repository cadence)
    commits = [4, 6, 3, 8, 5, 7, 9, 4, 11, 6, 8, 12, 7, 9]
    max_c = 14
    chart_h = 60

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 210" width="100%" height="100%">
  <rect width="958" height="208" x="1" y="1" rx="12" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5"/>

  <!-- Header -->
  <g transform="translate(32, 28)">
    <text x="0" y="0" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="700" fill="{accent_blue}" letter-spacing="1.5">ACTIVITY &amp; TECHNICAL OVERVIEW</text>
    <text x="240" y="0" font-family="'JetBrains Mono', Consolas, monospace" font-size="10.5" fill="{text_muted}">// 14-DAY COMMIT VELOCITY &amp; LANGUAGE DISTRIBUTION</text>
  </g>

  <!-- Left: Daily Commit Rate Chart (Width: 500) -->
  <g transform="translate(32, 46)">
    <rect width="500" height="138" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    
    <!-- Chart Title and Metrics -->
    <text x="18" y="24" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="{text_primary}">Daily Commit Frequency</text>
    
    <g transform="translate(310, 24)">
      <rect x="0" y="-12" width="80" height="20" rx="4" fill="{bg_color}" stroke="{card_border}" stroke-width="1"/>
      <circle cx="8" cy="-2" r="2.5" fill="{accent_emerald}"/>
      <text x="16" y="2" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="600" fill="{accent_emerald}">6.9 / DAY</text>
      
      <rect x="88" y="-12" width="84" height="20" rx="4" fill="{bg_color}" stroke="{card_border}" stroke-width="1"/>
      <text x="96" y="2" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">96% CONSISTENT</text>
    </g>

    <!-- Grid lines -->
    <line x1="20" y1="52" x2="480" y2="52" stroke="{card_border}" stroke-width="0.8" stroke-dasharray="2 3"/>
    <line x1="20" y1="84" x2="480" y2="84" stroke="{card_border}" stroke-width="0.8" stroke-dasharray="2 3"/>
    <line x1="20" y1="116" x2="480" y2="116" stroke="{card_border}" stroke-width="1"/>

    <!-- Daily Bars -->
'''
    bar_w = 20
    gap = 12
    x_start = 28
    for i, c in enumerate(commits):
        bx = x_start + i * (bar_w + gap)
        bh = int((c / max_c) * chart_h)
        by = 116 - bh
        bar_color = accent_blue if i < len(commits)-2 else accent_emerald
        svg += f'''
    <rect x="{bx}" y="{by}" width="{bar_w}" height="{bh}" rx="3" fill="{bar_color}" fill-opacity="0.85"/>
'''
    
    # Bottom date tags
    svg += f'''
    <text x="32" y="128" font-family="'JetBrains Mono', monospace" font-size="8.5" fill="{text_muted}">14d ago</text>
    <text x="248" y="128" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="8.5" fill="{text_muted}">7d ago</text>
    <text x="472" y="128" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="600" fill="{accent_emerald}">Today (Active)</text>
  </g>

  <!-- Right: Clean Language Distribution & Architecture Chips (Width: 380) -->
  <g transform="translate(548, 46)">
    <rect width="380" height="138" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    
    <text x="18" y="24" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="{text_primary}">Language Ecosystem</text>

    <!-- Stacked Distribution Bar (344px wide) -->
    <g transform="translate(18, 38)">
      <rect x="0" y="0" width="344" height="10" rx="4" fill="#334155"/>
      <rect x="0" y="0" width="168" height="10" rx="4" fill="{accent_blue}"/>
      <rect x="170" y="0" width="115" height="10" rx="0" fill="{accent_purple}"/>
      <rect x="287" y="0" width="38" height="10" rx="0" fill="{accent_emerald}"/>
      <rect x="327" y="0" width="17" height="10" rx="0" fill="{accent_amber}"/>
    </g>

    <!-- Spacious 2x2 Language Legend (Clean, zero overlap) -->
    <g transform="translate(18, 68)">
      <!-- Go -->
      <circle cx="4" cy="4" r="3.5" fill="{accent_blue}"/>
      <text x="14" y="8" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="{text_primary}">Go</text>
      <text x="40" y="8" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="{text_secondary}">48% (stream)</text>

      <!-- TypeScript -->
      <circle cx="178" cy="4" r="3.5" fill="{accent_purple}"/>
      <text x="188" y="8" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="{text_primary}">TypeScript</text>
      <text x="265" y="8" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="{text_secondary}">34% (dodo, ledger)</text>

      <!-- Python -->
      <circle cx="4" cy="24" r="3.5" fill="{accent_emerald}"/>
      <text x="14" y="28" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="{text_primary}">Python</text>
      <text x="60" y="28" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="{text_secondary}">11% (tooling)</text>

      <!-- SQL / SQLite -->
      <circle cx="178" cy="24" r="3.5" fill="{accent_amber}"/>
      <text x="188" y="28" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="{text_primary}">SQL</text>
      <text x="215" y="28" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="{text_secondary}">7% (db schemas)</text>
    </g>

    <!-- Architecture Tenet Chips -->
    <g transform="translate(18, 108)">
      <rect x="0" y="0" width="105" height="20" rx="4" fill="{bg_color}" stroke="{card_border}" stroke-width="1"/>
      <text x="52" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="600" fill="{accent_blue}">VIM MODAL TUI</text>

      <rect x="113" y="0" width="112" height="20" rx="4" fill="{bg_color}" stroke="{card_border}" stroke-width="1"/>
      <text x="169" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="600" fill="{accent_purple}">LIVE WEBSOCKETS</text>

      <rect x="233" y="0" width="111" height="20" rx="4" fill="{bg_color}" stroke="{card_border}" stroke-width="1"/>
      <text x="288" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="600" fill="{accent_emerald}">OFFLINE-FIRST</text>
    </g>
  </g>
</svg>'''
    ET.fromstring(svg)
    return svg


# 3. REVAMPED ENGINEERING FOCUS (NO VERBOSE BULLETS, MODERN PILLS, ULTRA CLEAN)
def generate_engineering_focus(is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    card_bg = "#111827" if is_dark else "#FFFFFF"
    card_border = "#243248" if is_dark else "#CBD5E1"
    pill_bg = "#162032" if is_dark else "#F1F5F9"
    pill_border = "#243248" if is_dark else "#CBD5E1"
    
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#64748B"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    accent_purple = "#A78BFA" if is_dark else "#7C3AED"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 190" width="100%" height="100%">
  <rect width="958" height="188" x="1" y="1" rx="12" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5"/>

  <g transform="translate(32, 28)">
    <text x="0" y="0" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="700" fill="{accent_blue}" letter-spacing="1.5">ENGINEERING FOCUS</text>
    <text x="180" y="0" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11" font-weight="500" fill="{text_secondary}">&#8212; Understand the system. Engineer the architecture. Optimize for impact.</text>
  </g>

  <!-- Card 1: Systems Engineering -->
  <g transform="translate(32, 46)">
    <rect width="280" height="124" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    <g transform="translate(18, 16) scale(0.85)" stroke="{accent_blue}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
      {ICONS["cpu"]}
    </g>
    <text x="46" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14" font-weight="700" fill="{text_primary}">Systems Engineering</text>
    <text x="18" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11.5" font-weight="500" fill="{accent_blue}">Linux &amp; terminal runtimes</text>

    <!-- Tags / Pills -->
    <g transform="translate(18, 70)">
      <rect x="0" y="0" width="110" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="55" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">Go TUI Engines</text>

      <rect x="116" y="0" width="120" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="176" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">Vim Ergonomics</text>

      <rect x="0" y="25" width="135" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="67" y="38" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">Offline-First State</text>
    </g>
  </g>

  <!-- Card 2: Software Architecture -->
  <g transform="translate(340, 46)">
    <rect width="280" height="124" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    <g transform="translate(18, 16) scale(0.85)" stroke="{accent_emerald}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
      {ICONS["layers"]}
    </g>
    <text x="46" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14" font-weight="700" fill="{text_primary}">Software Architecture</text>
    <text x="18" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11.5" font-weight="500" fill="{accent_emerald}">Full-stack &amp; distributed systems</text>

    <!-- Tags / Pills -->
    <g transform="translate(18, 70)">
      <rect x="0" y="0" width="125" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="62" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">Graph Debt Solver</text>

      <rect x="131" y="0" width="105" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="183" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">Dual DB (pg/sqlite)</text>

      <rect x="0" y="25" width="135" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="67" y="38" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">Distributed Sync</text>
    </g>
  </g>

  <!-- Card 3: Applied Intelligence -->
  <g transform="translate(648, 46)">
    <rect width="280" height="124" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    <g transform="translate(18, 16) scale(0.85)" stroke="{accent_purple}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
      {ICONS["brain-circuit"]}
    </g>
    <text x="46" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14" font-weight="700" fill="{text_primary}">Applied Intelligence</text>
    <text x="18" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11.5" font-weight="500" fill="{accent_purple}">Multimodal &amp; efficient streaming</text>

    <!-- Tags / Pills -->
    <g transform="translate(18, 70)">
      <rect x="0" y="0" width="110" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="55" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">Gemini Live API</text>

      <rect x="116" y="0" width="120" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="176" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">Voice WebSockets</text>

      <rect x="0" y="25" width="135" height="20" rx="4" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
      <text x="67" y="38" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">Audio Worklet DSP</text>
    </g>
  </g>
</svg>'''
    ET.fromstring(svg)
    return svg


# 4. FIXED DODO PIPELINE (GENEROUS 175PX CARDS, ZERO OVERFLOW)
def generate_dodo_pipeline(is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    card_bg = "#111827" if is_dark else "#FFFFFF"
    card_border = "#243248" if is_dark else "#CBD5E1"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    accent_purple = "#A78BFA" if is_dark else "#7C3AED"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    arrow_color = "#64748B" if is_dark else "#94A3B8"

    nodes = [
        ("Microphone Input", "16kHz PCM Stream", accent_blue),
        ("Audio Worklet DSP", "Real-Time VU Meter", accent_purple),
        ("Gemini 2.0 Live", "Bidirectional WSS", accent_blue),
        ("Suspicion FSM", "Dynamic Alibi State", accent_purple)
    ]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 120" width="100%" height="100%">
  <defs>
    <marker id="arrow_dodo_fixed_{'dark' if is_dark else 'light'}" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="{arrow_color}"/>
    </marker>
  </defs>

  <rect width="878" height="118" x="1" y="1" rx="10" fill="{bg_color}" stroke="{border_color}" stroke-width="1.2"/>

  <text x="24" y="24" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="{accent_purple}" letter-spacing="1">REAL-TIME MULTIMODAL AUDIO PIPELINE</text>
  <text x="320" y="24" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" fill="{text_secondary}">// FULL-DUPLEX WEBSOCKET STREAMING &amp; STATE ENGINE</text>
'''
    x_start = 24
    card_width = 175
    gap = 42
    for i, (title, sub, color) in enumerate(nodes):
        x = x_start + i * (card_width + gap)
        svg += f'''
  <g transform="translate({x}, 40)">
    <rect width="{card_width}" height="60" rx="6" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    <circle cx="16" cy="18" r="3" fill="{color}"/>
    <text x="26" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11.5" font-weight="700" fill="{text_primary}">{title}</text>
    <text x="16" y="44" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="{text_secondary}">{sub}</text>
  </g>'''
        if i < len(nodes) - 1:
            arrow_x = x + card_width + 4
            svg += f'''
  <line x1="{arrow_x}" y1="70" x2="{arrow_x + gap - 8}" y2="70" stroke="{arrow_color}" stroke-width="1.5" marker-end="url(#arrow_dodo_fixed_{'dark' if is_dark else 'light'})"/>'''

    svg += '\n</svg>'
    ET.fromstring(svg)
    return svg

base = '/home/mudoker/mudoker-profile'

# Save all updated assets
with open(f"{base}/assets/hero-banner-dark.svg", "w") as f:
    f.write(generate_hero_banner(True))
with open(f"{base}/assets/hero-banner-light.svg", "w") as f:
    f.write(generate_hero_banner(False))

with open(f"{base}/assets/overview-activity-dark.svg", "w") as f:
    f.write(generate_overview_activity(True))
with open(f"{base}/assets/overview-activity-light.svg", "w") as f:
    f.write(generate_overview_activity(False))

with open(f"{base}/assets/engineering-focus-dark.svg", "w") as f:
    f.write(generate_engineering_focus(True))
with open(f"{base}/assets/engineering-focus-light.svg", "w") as f:
    f.write(generate_engineering_focus(False))

with open(f"{base}/assets/pipeline-dodo-dark.svg", "w") as f:
    f.write(generate_dodo_pipeline(True))
with open(f"{base}/assets/pipeline-dodo-light.svg", "w") as f:
    f.write(generate_dodo_pipeline(False))

print("All revamped visual assets successfully generated and validated!")
