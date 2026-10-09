import reflex as rx


def saas_terminal_mockup():
    """
    Signature Next.js SaaS Starter Animated Terminal Element.
    Renders a dark developer-grade terminal with macOS traffic control dots
    and real-time animated command logs.
    """
    return rx.html(
        """
        <div style="width: 100%; max-width: 820px; margin: 32px auto 0 auto; text-align: left;">
            <style>
                @keyframes cursorBlink {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0; }
                }
                .term-cursor {
                    animation: cursorBlink 1s infinite;
                    display: inline-block;
                    width: 8px;
                    height: 14px;
                    background: #38BDF8;
                    vertical-align: middle;
                    margin-left: 4px;
                }
                
                @keyframes lineFade {
                    0% { opacity: 0; transform: translateY(4px); }
                    100% { opacity: 1; transform: translateY(0); }
                }
                .term-line {
                    animation: lineFade 0.4s ease-out forwards;
                }
                
                .terminal-card {
                    background: #0B1726;
                    border: 1px solid rgba(56, 189, 248, 0.2);
                    border-radius: 12px;
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 30px rgba(27, 110, 91, 0.15);
                    overflow: hidden;
                    font-family: 'IBM Plex Mono', monospace;
                }
            </style>

            <div class="terminal-card">
                <!-- Terminal Window Header Bar -->
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; background: #070F1A; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="width: 12px; height: 12px; border-radius: 50%; background: #FF5F56; display: inline-block;"></span>
                        <span style="width: 12px; height: 12px; border-radius: 50%; background: #FFBD2E; display: inline-block;"></span>
                        <span style="width: 12px; height: 12px; border-radius: 50%; background: #27C93F; display: inline-block;"></span>
                    </div>
                    <span style="font-size: 12px; color: rgba(240, 244, 243, 0.6); font-weight: 600;">bash — cyber-shield multi-agent</span>
                    <span style="font-size: 11px; background: rgba(56, 189, 248, 0.15); color: #38BDF8; padding: 2px 8px; border-radius: 4px; font-weight: 600;">v2.4 REALTIME</span>
                </div>

                <!-- Terminal Command Logs Body -->
                <div style="padding: 20px; font-size: 13px; line-height: 1.7; color: #E2E8F0;">
                    <div class="term-line" style="color: #94A3B8;">
                        <span style="color: #38BDF8;">$</span> cyber-shield scan --audio voice_call.wav --target +9198765XXXXX
                    </div>
                    
                    <div class="term-line" style="color: #64748B; margin-top: 6px;">
                        [0.00s] Initializing Multi-Agent Consensus Pipeline...
                    </div>

                    <div class="term-line" style="color: #38BDF8; margin-top: 6px;">
                        <span style="color: #10B981;">✔</span> [SPEECH-AGENT]: Mitran14 Classifier -> <span style="color: #EF4444; font-weight: 700;">99.2% Synthetic Voice Spoof</span>
                    </div>

                    <div class="term-line" style="color: #38BDF8; margin-top: 4px;">
                        <span style="color: #10B981;">✔</span> [TEXT-AGENT]: Llama 3.3 RAG -> <span style="color: #F59E0B; font-weight: 700;">Urgency Tactics Matched (Phishing URL)</span>
                    </div>

                    <div class="term-line" style="color: #38BDF8; margin-top: 4px;">
                        <span style="color: #10B981;">✔</span> [SUSPECT-DB]: SQLite Idempotent Engine -> <span style="color: #EF4444; font-weight: 700;">UPI Flagged (Risk Score: 92/100)</span>
                    </div>

                    <div class="term-line" style="background: rgba(239, 68, 68, 0.12); border-left: 3px solid #EF4444; padding: 8px 12px; margin-top: 10px; border-radius: 4px;">
                        <span style="color: #EF4444; font-weight: 700;">VERDICT: SPOOFED FRAUD CALL DETECTED</span>
                        <span style="color: #94A3B8; font-size: 11px; display: block; margin-top: 2px;">Latency: 1.4s | Multi-Agent Consensus: High Confidence</span>
                    </div>

                    <div style="margin-top: 8px; color: #94A3B8;">
                        <span style="color: #38BDF8;">$</span> <span style="color: #F0F4F3;">ready for next inspection</span><span class="term-cursor"></span>
                    </div>
                </div>
            </div>
        </div>
        """
    )


def hero_defense_hub():
    """Backwards compatibility wrapper returning terminal mockup."""
    return saas_terminal_mockup()


def live_animated_waveform():
    """Backwards compatibility wrapper returning terminal mockup."""
    return saas_terminal_mockup()


def hero() -> rx.Component:
    """
    Next.js SaaS Starter Inspired Hero Section Component.
    Features Next.js SaaS layout, animated developer terminal, pill badge, and clean action CTAs.
    """
    return rx.box(
        rx.box(
            rx.vstack(
                # Next.js SaaS Starter Announcement Pill Badge
                rx.hstack(
                    rx.box(
                        "✨",
                        font_size="13px",
                    ),
                    rx.text(
                        "Multi-Agent AI Fraud Shield 2.0 Released",
                        font_size="13px",
                        font_weight="600",
                        color="#0A1F2E",
                        font_family="'Outfit', sans-serif",
                    ),
                    rx.icon("arrow-right", size=14, color="#1B6E5B"),
                    spacing="2",
                    align="center",
                    padding_x="14px",
                    padding_y="6px",
                    background="#FFFFFF",
                    border="1px solid #CBD5E1",
                    border_radius="20px",
                    box_shadow="0 2px 8px rgba(0,0,0,0.04)",
                    cursor="pointer",
                    _hover={"border_color": "#1B6E5B", "transform": "translateY(-1px)"},
                    transition="all 0.2s ease",
                ),
                
                # Next.js SaaS Starter Bold Headline & Subtitle
                rx.heading(
                    "Institutional Multi-Agent AI Platform Against Cyber Fraud",
                    font_size={"initial": "32px", "sm": "46px", "md": "58px"},
                    font_weight="800",
                    color="#0A1F2E",
                    font_family="'Space Grotesk', sans-serif",
                    text_align="center",
                    line_height="1.1",
                    max_width="960px",
                    margin_top="18px",
                    user_select="none",
                ),
                rx.text(
                    "Protecting citizens and institutions with real-time cloned voice detection, Llama 3.3 SMS phishing dissection, and suspect registry risk scoring.",
                    font_size={"initial": "16px", "sm": "18px", "md": "20px"},
                    color="#475569",
                    font_family="'Outfit', sans-serif",
                    text_align="center",
                    max_width="780px",
                    margin_top="12px",
                    user_select="none",
                ),
                
                # Call to Action Buttons (Next.js SaaS starter button layout)
                rx.hstack(
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon("shield-alert", size=18),
                                rx.text("Analyze a Call / Text"),
                                rx.icon("arrow-right", size=16),
                                spacing="2",
                            ),
                            size="3",
                            background="#0A1F2E",
                            color="#FFFFFF",
                            font_weight="700",
                            font_family="'Space Grotesk', sans-serif",
                            padding_x="28px",
                            padding_y="24px",
                            border_radius="10px",
                            cursor="pointer",
                            box_shadow="0 4px 16px rgba(10, 31, 46, 0.25)",
                            _hover={"background": "#1B6E5B", "transform": "translateY(-2px)"},
                            transition="all 0.2s ease",
                        ),
                        href="/scan",
                        text_decoration="none",
                    ),
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon("search", size=18),
                                rx.text("Search Suspect DB"),
                                spacing="2",
                            ),
                            size="3",
                            variant="outline",
                            color="#0A1F2E",
                            border="1px solid #CBD5E1",
                            font_weight="700",
                            font_family="'Space Grotesk', sans-serif",
                            padding_x="24px",
                            padding_y="24px",
                            border_radius="10px",
                            cursor="pointer",
                            background="#FFFFFF",
                            _hover={"background": "#F8FAFC", "border_color": "#0A1F2E"},
                            transition="all 0.2s ease",
                        ),
                        href="/suspect-intelligence",
                        text_decoration="none",
                    ),
                    spacing="3",
                    align="center",
                    justify="center",
                    wrap="wrap",
                    margin_top="24px",
                ),

                # Next.js SaaS Animated Terminal Mockup Visual
                saas_terminal_mockup(),

                spacing="4",
                align="center",
                padding_y={"initial": "40px", "sm": "60px", "md": "70px"},
            ),
            max_width="1200px",
            padding_x={"initial": "16px", "md": "32px"},
            margin_x="auto",
        ),
        background="linear-gradient(180deg, #F8FAFC 0%, #EDF2F7 100%)",
        border_bottom="1px solid #E2E8F0",
        position="relative",
        overflow="hidden",
        width="100%",
    )
