import os

def create_banner(is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    grid_color = "#162032" if is_dark else "#E2E8F0"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#64748B"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    accent_purple = "#A78BFA" if is_dark else "#7C3AED"
    badge_bg = "rgba(30, 41, 59, 0.7)" if is_dark else "rgba(241, 245, 249, 0.9)"
    badge_border = "#334155" if is_dark else "#CBD5E1"
    radar_circle = "#1E293B" if is_dark else "#E2E8F0"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 320" width="100%" height="100%">
  <defs>
    <pattern id="grid_{"dark" if is_dark else "light"}" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="{grid_color}" stroke-width="0.75" stroke-opacity="0.6"/>
      <circle cx="32" cy="32" r="1" fill="{grid_color}" fill-opacity="0.8"/>
    </pattern>
    <linearGradient id="blue_glow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{accent_blue}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="{accent_blue}" stop-opacity="0"/>
    </linearGradient>
    <filter id="subtle_shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="{"0.35" if is_dark else "0.08"}"/>
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect width="958" height="318" x="1" y="1" rx="14" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5" filter="url(#subtle_shadow)"/>
  <rect width="956" height="316" x="2" y="2" rx="13" fill="url(#grid_{"dark" if is_dark else "light"})" />

  <!-- Ambient Glow -->
  <circle cx="820" cy="90" r="160" fill="url(#blue_glow)" />

  <!-- Top System Bar -->
  <g transform="translate(36, 36)">
    <!-- Terminal indicator / status -->
    <circle cx="4" cy="4" r="4.5" fill="{accent_emerald}" />
    <circle cx="4" cy="4" r="9" fill="none" stroke="{accent_emerald}" stroke-width="1" stroke-opacity="0.4">
      <animate attributeName="r" values="4.5;10;4.5" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="0.6;0.1;0.6" dur="3s" repeatCount="indefinite"/>
    </circle>
    <text x="24" y="8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Roboto, monospace" font-size="11" font-weight="600" fill="{accent_emerald}" letter-spacing="1.5">SYSTEM ACTIVE // ARCHITECTURE • SYSTEMS • AI</text>
    
    <text x="888" y="8" text-anchor="end" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="{text_muted}" letter-spacing="1">10.82°N, 106.63°E</text>
  </g>

  <!-- Top Divider Line -->
  <line x1="36" y1="58" x2="924" y2="58" stroke="{border_color}" stroke-width="1" stroke-dasharray="4 4" />

  <!-- Main Hero Brand Section -->
  <g transform="translate(36, 120)">
    <!-- Monospace Prompt Prefix -->
    <text x="0" y="-8" font-family="'JetBrains Mono', Consolas, monospace" font-size="14" font-weight="500" fill="{accent_blue}" letter-spacing="0.5">&gt; whoami --verbose</text>
    
    <!-- User / Profile Name -->
    <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="46" font-weight="800" fill="{text_primary}" letter-spacing="-1">mudoker</text>
    <text x="220" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="20" font-weight="400" fill="{text_muted}">/</text>
    <text x="238" y="42" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="20" font-weight="500" fill="{text_secondary}">software &amp; systems engineer</text>

    <!-- Bio / Philosophy snippet -->
    <text x="0" y="80" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="14.5" font-weight="400" fill="{text_secondary}" letter-spacing="-0.1">
      Designing resilient backend architectures, hardware-adjacent Linux systems, and real-time intelligent agents.
    </text>
    <text x="0" y="104" font-family="-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif" font-size="13.5" font-style="italic" fill="{text_muted}">
      &#8220;If a thing is humanly possible, consider it to be within your reach.&#8221; &#8212; Marcus Aurelius
    </text>
  </g>

  <!-- Right Geometric Radar & Specs Graphic -->
  <g transform="translate(730, 95)">
    <!-- Circuit Crosshairs & Coordinates -->
    <circle cx="100" cy="70" r="60" fill="none" stroke="{radar_circle}" stroke-width="1.2" />
    <circle cx="100" cy="70" r="40" fill="none" stroke="{radar_circle}" stroke-width="1" stroke-dasharray="3 3" />
    <circle cx="100" cy="70" r="20" fill="none" stroke="{radar_circle}" stroke-width="0.8" />
    <circle cx="100" cy="70" r="3" fill="{accent_blue}" />
    
    <!-- Target Crosshairs -->
    <line x1="25" y1="70" x2="175" y2="70" stroke="{radar_circle}" stroke-width="0.8" />
    <line x1="100" y1="-5" x2="100" y2="145" stroke="{radar_circle}" stroke-width="0.8" />
    
    <!-- Coordinate ticks -->
    <path d="M 92 10 L 100 10 M 108 10 L 100 10 M 92 130 L 100 130 M 108 130 L 100 130" stroke="{accent_blue}" stroke-width="1" />
    <path d="M 40 62 L 40 70 M 40 78 L 40 70 M 160 62 L 160 70 M 160 78 L 160 70" stroke="{accent_blue}" stroke-width="1" />

    <!-- Technical Labels -->
    <text x="100" y="156" text-anchor="middle" font-family="'JetBrains Mono', Consolas, monospace" font-size="9" fill="{accent_blue}" letter-spacing="1">SYS_KERNEL_OK</text>
  </g>

  <!-- Bottom Badges / Capabilities Bar -->
  <g transform="translate(36, 268)">
    <!-- Pillar 1: Systems -->
    <rect x="0" y="0" width="170" height="28" rx="6" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <circle cx="14" cy="14" r="3" fill="{accent_blue}"/>
    <text x="26" y="18" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="{text_primary}">SYSTEMS &amp; DRIVERS</text>

    <!-- Pillar 2: Software Engineering -->
    <rect x="182" y="0" width="180" height="28" rx="6" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <circle cx="196" cy="14" r="3" fill="{accent_emerald}"/>
    <text x="208" y="18" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="{text_primary}">BACKEND ARCHITECTURE</text>

    <!-- Pillar 3: Applied AI -->
    <rect x="374" y="0" width="176" height="28" rx="6" fill="{badge_bg}" stroke="{badge_border}" stroke-width="1"/>
    <circle cx="388" cy="14" r="3" fill="{accent_purple}"/>
    <text x="400" y="18" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="{text_primary}">MULTIMODAL STREAMING</text>

    <!-- Core Languages Snippet -->
    <text x="888" y="18" text-anchor="end" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="{text_muted}">[ Go • C • TypeScript • Linux • Python ]</text>
  </g>
</svg>'''
    return svg

def create_pillars(is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    card_bg = "#111827" if is_dark else "#FFFFFF"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    card_border = "#243248" if is_dark else "#CBD5E1"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#64748B"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    accent_purple = "#A78BFA" if is_dark else "#7C3AED"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 210" width="100%" height="100%">
  <defs>
    <filter id="card_shadow" x="-3%" y="-5%" width="106%" height="115%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="{"0.25" if is_dark else "0.05"}"/>
    </filter>
  </defs>

  <rect width="958" height="208" x="1" y="1" rx="12" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5" />

  <!-- Section Title -->
  <g transform="translate(32, 28)">
    <text x="0" y="0" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="{accent_blue}" letter-spacing="1.5">CORE ENGINEERING TRIAD</text>
    <text x="210" y="0" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="{text_muted}">// BALANCED TECHNICAL FOUNDATION</text>
  </g>

  <!-- Card 1: Systems & Architecture -->
  <g transform="translate(32, 48)" filter="url(#card_shadow)">
    <rect width="280" height="138" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    <circle cx="20" cy="22" r="4" fill="{accent_blue}"/>
    <text x="32" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14" font-weight="700" fill="{text_primary}">Systems &amp; OS</text>
    <text x="20" y="52" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="600" fill="{accent_blue}">Low-Level &amp; Kernel Interfaces</text>
    
    <text x="20" y="76" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" fill="{text_secondary}">• Linux driver development (C, Meson)</text>
    <text x="20" y="96" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" fill="{text_secondary}">• Hardware defect filtering &amp; biometrics</text>
    <text x="20" y="116" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" fill="{text_secondary}">• Terminal TUI engines &amp; SQLite WAL</text>
  </g>

  <!-- Card 2: Software Engineering -->
  <g transform="translate(340, 48)" filter="url(#card_shadow)">
    <rect width="280" height="138" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    <circle cx="20" cy="22" r="4" fill="{accent_emerald}"/>
    <text x="32" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14" font-weight="700" fill="{text_primary}">Software Architecture</text>
    <text x="20" y="52" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="600" fill="{accent_emerald}">Full-Stack &amp; Enterprise Systems</text>
    
    <text x="20" y="76" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" fill="{text_secondary}">• High-throughput Go &amp; TypeScript backends</text>
    <text x="20" y="96" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" fill="{text_secondary}">• Graph debt minimization algorithms</text>
    <text x="20" y="116" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" fill="{text_secondary}">• Offline-first synchronization &amp; PWAs</text>
  </g>

  <!-- Card 3: Applied AI -->
  <g transform="translate(648, 48)" filter="url(#card_shadow)">
    <rect width="280" height="138" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>
    <circle cx="20" cy="22" r="4" fill="{accent_purple}"/>
    <text x="32" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="14" font-weight="700" fill="{text_primary}">Applied Intelligence</text>
    <text x="20" y="52" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="600" fill="{accent_purple}">Multimodal &amp; Efficient Inference</text>
    
    <text x="20" y="76" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" fill="{text_secondary}">• Bidirectional voice streaming via WebSockets</text>
    <text x="20" y="96" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" fill="{text_secondary}">• Google Gemini Multimodal Live API</text>
    <text x="20" y="116" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="12" fill="{text_secondary}">• Efficient inference &amp; cost optimization</text>
  </g>
</svg>'''
    return svg

os.makedirs('/home/mudoker/mudoker-profile/assets', exist_ok=True)
with open('/home/mudoker/mudoker-profile/assets/hero-banner-dark.svg', 'w') as f:
    f.write(create_banner(True))
with open('/home/mudoker/mudoker-profile/assets/hero-banner-light.svg', 'w') as f:
    f.write(create_banner(False))

with open('/home/mudoker/mudoker-profile/assets/pillars-dark.svg', 'w') as f:
    f.write(create_pillars(True))
with open('/home/mudoker/mudoker-profile/assets/pillars-light.svg', 'w') as f:
    f.write(create_pillars(False))

print("Assets successfully generated.")

def create_libfprint_pipeline(is_dark=True):
    bg_color = "#0B0F17" if is_dark else "#F8FAFC"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    card_bg = "#111827" if is_dark else "#FFFFFF"
    card_border = "#243248" if is_dark else "#CBD5E1"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    accent_blue = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#34D399" if is_dark else "#059669"
    arrow_color = "#64748B" if is_dark else "#94A3B8"

    nodes = [
        ("Raw Sensor Die", "64×80 Static Capture", accent_blue),
        ("Defect Averaging", "Interpolate 7 DC offsets", accent_emerald),
        ("5-Frame Temporal", "ADC noise cancellation", accent_blue),
        ("2×2 Bilinear Scale", "128×160 for NIST", accent_emerald),
        ("Contrast Squashing", "Active interior [4:76, 3:60]", accent_blue),
        ("NBIS Bozorth-3", "FAR: 0.0% (bz3=12)", accent_emerald),
    ]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 120" width="100%" height="100%">
  <defs>
    <marker id="arrow_{"dark" if is_dark else "light"}" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="{arrow_color}"/>
    </marker>
  </defs>

  <rect width="878" height="118" x="1" y="1" rx="10" fill="{bg_color}" stroke="{border_color}" stroke-width="1.2"/>

  <text x="24" y="22" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="{accent_blue}" letter-spacing="1">SIGNAL &amp; MINUTIAE PROCESSING PIPELINE</text>
  <text x="320" y="22" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" fill="{text_secondary}">// HARDWARE CORRECTION &amp; ZERO-FAR MATCHING</text>
'''
    x_start = 24
    card_width = 118
    gap = 26
    for i, (title, sub, color) in enumerate(nodes):
        x = x_start + i * (card_width + gap)
        svg += f'''
  <g transform="translate({x}, 38)">
    <rect width="{card_width}" height="64" rx="6" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    <circle cx="12" cy="16" r="3" fill="{color}"/>
    <text x="22" y="19" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11" font-weight="700" fill="{text_primary}">{title}</text>
    <text x="12" y="42" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">{sub.split(' ')[0]}</text>
    <text x="12" y="54" font-family="'JetBrains Mono', monospace" font-size="8.5" fill="{text_secondary}">{' '.join(sub.split(' ')[1:])}</text>
  </g>'''
        if i < len(nodes) - 1:
            arrow_x = x + card_width + 4
            svg += f'''
  <line x1="{arrow_x}" y1="70" x2="{arrow_x + gap - 8}" y2="70" stroke="{arrow_color}" stroke-width="1.5" marker-end="url(#arrow_{"dark" if is_dark else "light"})"/>'''

    svg += '\n</svg>'
    return svg

with open('/home/mudoker/mudoker-profile/assets/pipeline-libfprint-dark.svg', 'w') as f:
    f.write(create_libfprint_pipeline(True))
with open('/home/mudoker/mudoker-profile/assets/pipeline-libfprint-light.svg', 'w') as f:
    f.write(create_libfprint_pipeline(False))

print("Pipeline assets generated.")

def create_dodo_pipeline(is_dark=True):
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
        ("Microphone Input", "PCM 16-bit 16kHz", accent_blue),
        ("Audio Worklet", "Real-time VU meter", accent_purple),
        ("WebSocket Client", "wss:// streaming", accent_blue),
        ("Gemini 2.0 Live", "Multimodal Low-Latency", accent_purple),
        ("Audio Synthesis", "Charon voice via Web Audio", accent_blue),
        ("Suspicion FSM", "Dynamic state &amp; alibis", accent_purple),
    ]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 120" width="100%" height="100%">
  <defs>
    <marker id="arrow_dodo_{"dark" if is_dark else "light"}" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="{arrow_color}"/>
    </marker>
  </defs>

  <rect width="878" height="118" x="1" y="1" rx="10" fill="{bg_color}" stroke="{border_color}" stroke-width="1.2"/>

  <text x="24" y="22" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="600" fill="{accent_purple}" letter-spacing="1">REAL-TIME MULTIMODAL AUDIO PIPELINE</text>
  <text x="320" y="22" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" fill="{text_secondary}">// BIDIRECTIONAL WEBSOCKET STREAMING &amp; STATE ENGINE</text>
'''
    x_start = 24
    card_width = 118
    gap = 26
    for i, (title, sub, color) in enumerate(nodes):
        x = x_start + i * (card_width + gap)
        svg += f'''
  <g transform="translate({x}, 38)">
    <rect width="{card_width}" height="64" rx="6" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    <circle cx="12" cy="16" r="3" fill="{color}"/>
    <text x="22" y="19" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11" font-weight="700" fill="{text_primary}">{title}</text>
    <text x="12" y="42" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_secondary}">{sub.split(' ')[0]}</text>
    <text x="12" y="54" font-family="'JetBrains Mono', monospace" font-size="8.5" fill="{text_secondary}">{' '.join(sub.split(' ')[1:])}</text>
  </g>'''
        if i < len(nodes) - 1:
            arrow_x = x + card_width + 4
            svg += f'''
  <line x1="{arrow_x}" y1="70" x2="{arrow_x + gap - 8}" y2="70" stroke="{arrow_color}" stroke-width="1.5" marker-end="url(#arrow_dodo_{"dark" if is_dark else "light"})"/>'''

    svg += '\n</svg>'
    return svg

def create_metrics_card(is_dark=True):
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

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 180" width="100%" height="100%">
  <rect width="878" height="178" x="1" y="1" rx="10" fill="{bg_color}" stroke="{border_color}" stroke-width="1.2"/>

  <!-- Header -->
  <g transform="translate(24, 26)">
    <text x="0" y="0" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" font-weight="700" fill="{accent_blue}" letter-spacing="1.5">TECHNICAL SIGNAL OVERVIEW</text>
    <text x="210" y="0" font-family="'JetBrains Mono', Consolas, monospace" font-size="10" fill="{text_muted}">// ACTIVE REPOSITORIES &amp; LANGUAGE DISTRIBUTION</text>
  </g>

  <!-- Left: Language Breakdown -->
  <g transform="translate(24, 46)">
    <rect width="400" height="110" rx="6" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    
    <!-- Language Bar -->
    <g transform="translate(16, 18)">
      <rect x="0" y="0" width="368" height="10" rx="4" fill="#334155"/>
      <rect x="0" y="0" width="130" height="10" rx="4" fill="{accent_blue}"/>
      <rect x="132" y="0" width="115" height="10" rx="0" fill="{accent_purple}"/>
      <rect x="249" y="0" width="65" height="10" rx="0" fill="{accent_amber}"/>
      <rect x="316" y="0" width="40" height="10" rx="0" fill="{accent_emerald}"/>
    </g>

    <!-- Language Labels -->
    <g transform="translate(16, 48)">
      <!-- Go -->
      <circle cx="4" cy="4" r="4" fill="{accent_blue}"/>
      <text x="14" y="8" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_primary}">Go</text>
      <text x="14" y="22" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_muted}">35% (stream, memoir)</text>

      <!-- TypeScript -->
      <circle cx="104" cy="4" r="4" fill="{accent_purple}"/>
      <text x="114" y="8" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_primary}">TypeScript</text>
      <text x="114" y="22" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_muted}">31% (ledger, dodo)</text>

      <!-- C / Linux -->
      <circle cx="214" cy="4" r="4" fill="{accent_amber}"/>
      <text x="224" y="8" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_primary}">C / Linux</text>
      <text x="224" y="22" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_muted}">18% (libfprint-521d)</text>

      <!-- Python / SQL -->
      <circle cx="314" cy="4" r="4" fill="{accent_emerald}"/>
      <text x="324" y="8" font-family="'JetBrains Mono', monospace" font-size="11" fill="{text_primary}">Python/SQL</text>
      <text x="324" y="22" font-family="'JetBrains Mono', monospace" font-size="9" fill="{text_muted}">16% (infra, scripts)</text>
    </g>
  </g>

  <!-- Right: Architecture Metrics -->
  <g transform="translate(444, 46)">
    <rect width="412" height="110" rx="6" fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>
    
    <g transform="translate(18, 22)">
      <text x="0" y="0" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="700" fill="{text_primary}">Engineering Tenets</text>
      
      <g transform="translate(0, 16)">
        <text x="0" y="10" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11" fill="{text_secondary}">• Zero-tolerance for False Accepts in Biometrics (0.0% FAR verified)</text>
        <text x="0" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11" fill="{text_secondary}">• Pure home-row keyboard ergonomics with Vim-style modal states</text>
        <text x="0" y="46" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11" fill="{text_secondary}">• Sub-100ms real-time multimodal audio streaming over WebSockets</text>
        <text x="0" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif" font-size="11" fill="{text_secondary}">• Offline-first local data structures with optimistic synchronization</text>
      </g>
    </g>
  </g>
</svg>'''
    return svg

with open('/home/mudoker/mudoker-profile/assets/pipeline-dodo-dark.svg', 'w') as f:
    f.write(create_dodo_pipeline(True))
with open('/home/mudoker/mudoker-profile/assets/pipeline-dodo-light.svg', 'w') as f:
    f.write(create_dodo_pipeline(False))

with open('/home/mudoker/mudoker-profile/assets/metrics-dark.svg', 'w') as f:
    f.write(create_metrics_card(True))
with open('/home/mudoker/mudoker-profile/assets/metrics-light.svg', 'w') as f:
    f.write(create_metrics_card(False))

print("All diagrams and metrics generated.")
