import reflex as rx
from cyber_shield_reflex.state import State


def animated_cyber_canvas() -> rx.Component:
    """
    Renders dynamic HTML5 Canvas particle network & animated radar scan line.
    Pure client-side animation running at 60fps with zero external dependencies.
    """
    return rx.html(
        """
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; pointer-events: none; z-index: 1;">
            <canvas id="cyberNetworkCanvas" style="width: 100%; height: 100%; display: block;"></canvas>
            <div class="radar-scanline"></div>
        </div>
        <script>
        (function() {
            function initCanvas() {
                const canvas = document.getElementById('cyberNetworkCanvas');
                if (!canvas) return setTimeout(initCanvas, 100);
                const ctx = canvas.getContext('2d');
                let width = canvas.width = canvas.parentElement.offsetWidth || window.innerWidth;
                let height = canvas.height = canvas.parentElement.offsetHeight || 550;

                window.addEventListener('resize', () => {
                    if (!canvas.parentElement) return;
                    width = canvas.width = canvas.parentElement.offsetWidth || window.innerWidth;
                    height = canvas.height = canvas.parentElement.offsetHeight || 550;
                });

                const particleCount = Math.min(Math.floor(width / 22), 55);
                const particles = [];
                for (let i = 0; i < particleCount; i++) {
                    particles.push({
                        x: Math.random() * width,
                        y: Math.random() * height,
                        vx: (Math.random() - 0.5) * 0.8,
                        vy: (Math.random() - 0.5) * 0.8,
                        radius: Math.random() * 2 + 1,
                        color: Math.random() > 0.4 ? '#38BDF8' : '#1D4ED8'
                    });
                }

                function draw() {
                    ctx.clearRect(0, 0, width, height);

                    // Draw connecting nodes
                    for (let i = 0; i < particles.length; i++) {
                        for (let j = i + 1; j < particles.length; j++) {
                            const dx = particles[i].x - particles[j].x;
                            const dy = particles[i].y - particles[j].y;
                            const dist = Math.sqrt(dx * dx + dy * dy);
                            if (dist < 110) {
                                ctx.strokeStyle = `rgba(56, 189, 248, ${0.25 * (1 - dist / 110)})`;
                                ctx.lineWidth = 0.8;
                                ctx.beginPath();
                                ctx.moveTo(particles[i].x, particles[i].y);
                                ctx.lineTo(particles[j].x, particles[j].y);
                                ctx.stroke();
                            }
                        }
                    }

                    // Draw particles
                    for (let p of particles) {
                        ctx.fillStyle = p.color;
                        ctx.shadowBlur = 8;
                        ctx.shadowColor = '#38BDF8';
                        ctx.beginPath();
                        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.shadowBlur = 0;

                        p.x += p.vx;
                        p.y += p.vy;
                        if (p.x < 0 || p.x > width) p.vx *= -1;
                        if (p.y < 0 || p.y > height) p.vy *= -1;
                    }
                    requestAnimationFrame(draw);
                }
                draw();
            }
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initCanvas);
            } else {
                initCanvas();
            }
        })();
        </script>
        <style>
        @keyframes radarSweep {
            0% { transform: translateY(-100%); opacity: 0.1; }
            50% { opacity: 0.8; }
            100% { transform: translateY(1000%); opacity: 0.1; }
        }
        .radar-scanline {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent 0%, rgba(56, 189, 248, 0.2) 20%, rgba(56, 189, 248, 0.9) 50%, rgba(56, 189, 248, 0.2) 80%, transparent 100%);
            box-shadow: 0 0 16px #38BDF8;
            animation: radarSweep 6s ease-in-out infinite;
        }
        @keyframes floatHero {
            0%, 100% { transform: translateY(0px) scale(1); filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.4)); }
            50% { transform: translateY(-10px) scale(1.02); filter: drop-shadow(0 0 40px rgba(56, 189, 248, 0.7)); }
        }
        @keyframes pulseHalo {
            0%, 100% { transform: scale(1); opacity: 0.3; }
            50% { transform: scale(1.15); opacity: 0.7; }
        }
        @keyframes rotateHolo {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes typingCursor {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        .hero-float-container {
            animation: floatHero 4s ease-in-out infinite;
        }
        .holo-ring {
            animation: rotateHolo 20s linear infinite;
        }
        .holo-ring-reverse {
            animation: rotateHolo 15s linear infinite reverse;
        }
        .pulse-halo-effect {
            animation: pulseHalo 3s ease-in-out infinite;
        }
        .code-pill {
            font-family: 'IBM Plex Mono', monospace;
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11px;
            color: #38BDF8;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        }
        </style>
        """
    )


def animated_cyberbot_insignia() -> rx.Component:
    """
    Centerpiece SVG Cyberbot animated insignia matching the glowing helmet from the banner.
    Surrounded by rotating holographic HUD rings and glowing neon visors.
    """
    return rx.box(
        rx.html(
            """
            <div style="position: relative; width: 220px; height: 220px; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                <!-- Glowing Halo Background -->
                <div class="pulse-halo-effect" style="position: absolute; width: 190px; height: 190px; border-radius: 50%; background: radial-gradient(circle, rgba(56, 189, 248, 0.4) 0%, rgba(29, 78, 216, 0.2) 60%, transparent 100%); filter: blur(12px);"></div>
                
                <!-- Rotating Hologram Ring 1 -->
                <svg class="holo-ring" width="210" height="210" viewBox="0 0 210 210" fill="none" style="position: absolute;">
                    <circle cx="105" cy="105" r="98" stroke="rgba(56, 189, 248, 0.35)" stroke-width="1.5" stroke-dasharray="14 10" />
                    <circle cx="105" cy="105" r="88" stroke="rgba(29, 78, 216, 0.3)" stroke-width="1" stroke-dasharray="6 14" />
                </svg>

                <!-- Rotating Hologram Ring 2 (Counter) -->
                <svg class="holo-ring-reverse" width="230" height="230" viewBox="0 0 230 230" fill="none" style="position: absolute;">
                    <circle cx="115" cy="115" r="108" stroke="rgba(56, 189, 248, 0.2)" stroke-width="1" stroke-dasharray="24 16" />
                </svg>

                <!-- Floating Cyberbot Mask -->
                <div class="hero-float-container" style="position: relative; z-index: 2;">
                    <svg width="120" height="130" viewBox="0 0 100 110" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <!-- Outer Helmet Armor -->
                        <path d="M50 8C30 8 18 24 18 48C18 68 32 94 50 104C68 94 82 68 82 48C82 24 70 8 50 8Z" 
                              fill="#071226" stroke="#38BDF8" stroke-width="3.5" stroke-linejoin="round"/>
                        
                        <!-- Left Ear Node -->
                        <rect x="10" y="40" width="7" height="24" rx="3.5" fill="#0A1E3F" stroke="#38BDF8" stroke-width="2"/>
                        <!-- Right Ear Node -->
                        <rect x="83" y="40" width="7" height="24" rx="3.5" fill="#0A1E3F" stroke="#38BDF8" stroke-width="2"/>

                        <!-- Helmet Crown Crest -->
                        <path d="M42 12H58V26C58 28 55 30 50 30C45 30 42 28 42 26V12Z" 
                              fill="#1E3A8A" stroke="#38BDF8" stroke-width="2"/>

                        <!-- Slanted Glowing Eyes Visor -->
                        <polygon points="32,46 44,50 42,54 30,50" fill="#38BDF8" filter="drop-shadow(0 0 6px #38BDF8)"/>
                        <polygon points="68,46 56,50 58,54 70,50" fill="#38BDF8" filter="drop-shadow(0 0 6px #38BDF8)"/>

                        <!-- Chin Shield Plate -->
                        <path d="M38 68L50 82L62 68L50 74L38 68Z" fill="#1E40AF" stroke="#38BDF8" stroke-width="2"/>
                        <path d="M50 74V95" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                </div>
            </div>
            """
        ),
        display="flex",
        justify="center",
        align="center",
        width="100%",
    )


def animated_hero() -> rx.Component:
    """
    High-impact animated cybersecurity motion hero section for Cyber Fraud Shield (Cyberbot).
    Features live canvas nodes, pulsing neon helmet insignia, cyber telemetry pills, and dynamic actions.
    """
    return rx.box(
        # Background Canvas & Radar
        animated_cyber_canvas(),
        
        # Grid overlay texture
        rx.box(
            position="absolute",
            top="0",
            left="0",
            width="100%",
            height="100%",
            background_image="radial-gradient(rgba(56, 189, 248, 0.12) 1px, transparent 1px)",
            background_size="32px 32px",
            opacity="0.65",
            pointer_events="none",
            z_index="2",
        ),
        
        # Hero Foreground Content
        rx.box(
            rx.vstack(
                # Top Status Pill
                rx.hstack(
                    rx.box(
                        width="8px",
                        height="8px",
                        border_radius="50%",
                        background="#38BDF8",
                        box_shadow="0 0 10px #38BDF8",
                    ),
                    rx.text(
                        "AI FRAUD DEFENSE SYSTEM ACTIVE • REAL-TIME PROTECTION",
                        font_size="12px",
                        font_weight="700",
                        letter_spacing="0.1em",
                        color="#38BDF8",
                        font_family="'IBM Plex Mono', monospace",
                    ),
                    padding_x="14px",
                    padding_y="6px",
                    background="rgba(15, 23, 42, 0.8)",
                    border="1px solid rgba(56, 189, 248, 0.35)",
                    border_radius="20px",
                    backdrop_filter="blur(10px)",
                    box_shadow="0 4px 16px rgba(0, 0, 0, 0.5)",
                    align="center",
                    spacing="2",
                    margin_bottom="12px",
                ),

                # Animated Glowing Insignia
                animated_cyberbot_insignia(),

                # Cyber Title with Glowing Gradient
                rx.vstack(
                    rx.heading(
                        "CYBERBOT",
                        font_size={"initial": "36px", "sm": "48px", "md": "56px"},
                        font_weight="900",
                        letter_spacing="0.08em",
                        font_family="'Space Grotesk', sans-serif",
                        background="linear-gradient(180deg, #FFFFFF 0%, #38BDF8 60%, #1D4ED8 100%)",
                        background_clip="text",
                        color="transparent",
                        text_shadow="0 0 30px rgba(56, 189, 248, 0.4)",
                        line_height="1.05",
                        margin_top="10px",
                    ),
                    rx.text(
                        "AI-POWERED CYBERSECURITY ASSISTANT & FRAUD DEFENSE ENGINE",
                        font_size={"initial": "12px", "sm": "14px", "md": "15px"},
                        font_weight="700",
                        letter_spacing="0.12em",
                        color="#E2E8F0",
                        font_family="'IBM Plex Mono', monospace",
                        text_align="center",
                    ),
                    rx.text(
                        "Next-generation defense safeguarding citizens against synthetic deepfake voice clones, phishing SMS, and extortion threats.",
                        font_size={"initial": "14px", "sm": "16px"},
                        color="#94A3B8",
                        font_family="'Outfit', sans-serif",
                        max_width="680px",
                        text_align="center",
                        margin_top="6px",
                    ),
                    spacing="2",
                    align="center",
                    width="100%",
                ),

                # Interactive Call-to-Action Buttons
                rx.hstack(
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon("mic", size=18, color="#FFFFFF"),
                                rx.text("Scan Voice & Call Audio", font_weight="700"),
                                spacing="2",
                                align="center",
                            ),
                            background="linear-gradient(90deg, #1D4ED8 0%, #0284C7 100%)",
                            color="#FFFFFF",
                            font_size="15px",
                            padding_x="24px",
                            padding_y="14px",
                            border_radius="10px",
                            box_shadow="0 6px 24px rgba(2, 132, 199, 0.45)",
                            cursor="pointer",
                            _hover={"transform": "translateY(-2px)", "box_shadow": "0 8px 30px rgba(56, 189, 248, 0.6)"},
                            transition="all 0.2s ease-in-out",
                        ),
                        href="/scan",
                        text_decoration="none",
                    ),
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon("shield-alert", size=18, color="#38BDF8"),
                                rx.text("Suspect Intelligence", font_weight="700"),
                                spacing="2",
                                align="center",
                            ),
                            background="rgba(15, 23, 42, 0.8)",
                            border="1px solid rgba(56, 189, 248, 0.4)",
                            color="#FFFFFF",
                            font_size="15px",
                            padding_x="24px",
                            padding_y="14px",
                            border_radius="10px",
                            backdrop_filter="blur(10px)",
                            cursor="pointer",
                            _hover={"background": "rgba(30, 41, 59, 0.9)", "border_color": "#38BDF8", "transform": "translateY(-2px)"},
                            transition="all 0.2s ease-in-out",
                        ),
                        href="/suspect-intelligence",
                        text_decoration="none",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("bot", size=18, color="#FFFFFF"),
                            rx.text("Ask Cyberbot AI", font_weight="700"),
                            spacing="2",
                            align="center",
                        ),
                        background="#0B132B",
                        border="1px solid #1E3A8A",
                        color="#38BDF8",
                        font_size="15px",
                        padding_x="22px",
                        padding_y="14px",
                        border_radius="10px",
                        cursor="pointer",
                        on_click=State.toggle_bot,  # type: ignore
                        _hover={"background": "#1E293B", "color": "#FFFFFF", "transform": "translateY(-2px)"},
                        transition="all 0.2s ease-in-out",
                    ),
                    wrap="wrap",
                    justify="center",
                    spacing="3",
                    margin_top="18px",
                ),

                # Live Security Telemetry Cards
                rx.grid(
                    rx.box(
                        rx.hstack(
                            rx.icon("audio_waveform", size=20, color="#38BDF8"),
                            rx.vstack(
                                rx.text("Acoustic Spoof Detection", font_size="12px", font_weight="700", color="#FFFFFF"),
                                rx.text("98.4% Synthetic Voice Accuracy", font_size="11px", color="#94A3B8"),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        padding="14px 18px",
                        background="rgba(15, 23, 42, 0.75)",
                        border="1px solid rgba(56, 189, 248, 0.2)",
                        border_radius="10px",
                        backdrop_filter="blur(8px)",
                    ),
                    rx.box(
                        rx.hstack(
                            rx.icon("file-search", size=20, color="#38BDF8"),
                            rx.vstack(
                                rx.text("Llama 3.3 Threat Engine", font_size="12px", font_weight="700", color="#FFFFFF"),
                                rx.text("TF-IDF + Zero-Shot Reasoning", font_size="11px", color="#94A3B8"),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        padding="14px 18px",
                        background="rgba(15, 23, 42, 0.75)",
                        border="1px solid rgba(56, 189, 248, 0.2)",
                        border_radius="10px",
                        backdrop_filter="blur(8px)",
                    ),
                    rx.box(
                        rx.hstack(
                            rx.icon("phone-call", size=20, color="#38BDF8"),
                            rx.vstack(
                                rx.text("National Cyber Helpline", font_size="12px", font_weight="700", color="#FFFFFF"),
                                rx.text("Toll-Free 1930 Direct Guidance", font_size="11px", color="#94A3B8"),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        padding="14px 18px",
                        background="rgba(15, 23, 42, 0.75)",
                        border="1px solid rgba(56, 189, 248, 0.2)",
                        border_radius="10px",
                        backdrop_filter="blur(8px)",
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", md="3"),
                    spacing="4",
                    width="100%",
                    max_width="880px",
                    margin_top="32px",
                ),
                align="center",
                width="100%",
                padding_y={"initial": "40px", "md": "60px"},
            ),
            position="relative",
            z_index="5",
            width="100%",
            max_width="1200px",
            margin_x="auto",
            padding_x={"initial": "16px", "md": "32px"},
        ),
        position="relative",
        overflow="hidden",
        width="100%",
        min_height={"initial": "520px", "md": "620px"},
        background="radial-gradient(circle at 50% 25%, #0B1E38 0%, #050B17 60%, #030712 100%)",
        border_bottom="1px solid #1E293B",
        box_shadow="0 10px 40px rgba(0, 0, 0, 0.8)",
    )
