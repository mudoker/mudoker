import os
import xml.etree.ElementTree as ET

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
    "terminal": '<polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/>'
}

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
        ET.fromstring(svg) # validate
    print("All 12 Lucide icons generated & validated.")

def generate_engineering_focus(base_dir, is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    card_bg = "#111827" if is_dark else "#FFFFFF"
    card_border = "#243248" if is_dark else "#CBD5E1"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#64748B"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    accent_purple = "#A78BFA" if is_dark else "#7C3AED"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 210" width="100%" height="100%">
  <rect width="958" height="208" x="1" y="1" rx="12" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5" />

  <!-- Philosophy One-Liner Header -->
  <g transform="translate(32, 28)">
    <text x="0" y="0" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="700" fill="{accent_blue}" letter-spacing="1.5">ENGINEERING FOCUS</text>
    <text x="180" y="0" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11.5" font-weight="500" fill="{text_secondary}">&#8212; Understand the system. Engineer the architecture. Optimize for impact.</text>
  </g>

  <!-- Card 1: Systems Engineering -->
  <g transform="translate(32, 48)">
    <rect width="280" height="138" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    <g transform="translate(20, 20) scale(0.9)" stroke="{accent_blue}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
      {ICONS["cpu"]}
    </g>
    <text x="50" y="36" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14.5" font-weight="700" fill="{text_primary}">Systems Engineering</text>
    <text x="20" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" font-weight="500" fill="{accent_blue}">Linux &amp; low-level development</text>
    
    <text x="20" y="92" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_secondary}">&#8226; Linux driver &amp; kernel space</text>
    <text x="20" y="110" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_secondary}">&#8226; Hardware defect filtering</text>
    <text x="20" y="128" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_secondary}">&#8226; Low-latency TUI runtimes</text>
  </g>

  <!-- Card 2: Software Architecture -->
  <g transform="translate(340, 48)">
    <rect width="280" height="138" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    <g transform="translate(20, 20) scale(0.9)" stroke="{accent_emerald}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
      {ICONS["layers"]}
    </g>
    <text x="50" y="36" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14.5" font-weight="700" fill="{text_primary}">Software Architecture</text>
    <text x="20" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" font-weight="500" fill="{accent_emerald}">Full-stack &amp; distributed systems</text>
    
    <text x="20" y="92" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_secondary}">&#8226; High-throughput Go services</text>
    <text x="20" y="110" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_secondary}">&#8226; Graph debt minimization</text>
    <text x="20" y="128" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_secondary}">&#8226; Offline-first local sync</text>
  </g>

  <!-- Card 3: Applied Intelligence -->
  <g transform="translate(648, 48)">
    <rect width="280" height="138" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    <g transform="translate(20, 20) scale(0.9)" stroke="{accent_purple}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
      {ICONS["brain-circuit"]}
    </g>
    <text x="50" y="36" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14.5" font-weight="700" fill="{text_primary}">Applied Intelligence</text>
    <text x="20" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" font-weight="500" fill="{accent_purple}">Multimodal &amp; efficient inference</text>
    
    <text x="20" y="92" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_secondary}">&#8226; Real-time voice WebSockets</text>
    <text x="20" y="110" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_secondary}">&#8226; Audio Worklet DSP meters</text>
    <text x="20" y="128" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_secondary}">&#8226; Token &amp; latency reduction</text>
  </g>
</svg>'''
    ET.fromstring(svg) # validate
    return svg

def generate_tech_stack(base_dir, is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    card_bg = "#111827" if is_dark else "#FFFFFF"
    card_border = "#243248" if is_dark else "#CBD5E1"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#64748B"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    accent_purple = "#A78BFA" if is_dark else "#7C3AED"
    accent_amber = "#FBBF24" if is_dark else "#D97706"

    categories = [
        ("LANGUAGES", [("Go", accent_blue), ("TypeScript", accent_purple), ("C", accent_amber), ("Python", accent_emerald), ("Rust", accent_blue), ("SQL", text_secondary)]),
        ("FRONTEND", [("React 19", accent_blue), ("Next.js (App Router)", text_primary), ("Tailwind CSS", accent_blue), ("Web Audio API", accent_purple)]),
        ("BACKEND", [("Go Concurrency", accent_blue), ("Node.js", accent_emerald), ("WebSockets (WSS)", accent_purple), ("OAuth 2.0 / RBAC", accent_amber)]),
        ("SYSTEMS &amp; DATA", [("Linux Drivers / Meson", accent_amber), ("PostgreSQL", accent_blue), ("SQLite (WAL / CTE)", accent_blue), ("Docker", accent_blue)]),
        ("APPLIED AI", [("Gemini Multimodal Live", accent_purple), ("Audio Worklets", accent_blue), ("Inference Optimization", accent_emerald)])
    ]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 220" width="100%" height="100%">
  <rect width="958" height="218" x="1" y="1" rx="12" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5" />

  <g transform="translate(32, 28)">
    <text x="0" y="0" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="700" fill="{accent_blue}" letter-spacing="1.5">TECHNOLOGY ECOSYSTEM</text>
    <text x="210" y="0" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="{text_muted}">// VERIFIED PRODUCTION &amp; PROJECT STACK</text>
  </g>
'''
    y = 48
    row_height = 30
    for cat_name, items in categories:
        svg += f'''
  <g transform="translate(32, {y})">
    <rect width="160" height="24" rx="4" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    <text x="12" y="16" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" fill="{accent_blue}">{cat_name}</text>
'''
        item_x = 176
        for item_name, color in items:
            badge_width = len(item_name) * 7.5 + 20
            svg += f'''
    <rect x="{item_x}" y="0" width="{badge_width}" height="24" rx="4" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    <circle cx="{item_x + 9}" cy="12" r="2.5" fill="{color}"/>
    <text x="{item_x + 18}" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11" font-weight="500" fill="{text_primary}">{item_name}</text>
'''
            item_x += badge_width + 8
        svg += '  </g>'
        y += row_height + 4

    svg += '\n</svg>'
    ET.fromstring(svg) # validate
    return svg

base = '/home/mudoker/mudoker-profile'
generate_icons(base)

with open(f"{base}/assets/engineering-focus-dark.svg", "w") as f:
    f.write(generate_engineering_focus(base, True))
with open(f"{base}/assets/engineering-focus-light.svg", "w") as f:
    f.write(generate_engineering_focus(base, False))

with open(f"{base}/assets/tech-stack-dark.svg", "w") as f:
    f.write(generate_tech_stack(base, True))
with open(f"{base}/assets/tech-stack-light.svg", "w") as f:
    f.write(generate_tech_stack(base, False))

print("Focus and Tech Stack assets generated & validated.")
