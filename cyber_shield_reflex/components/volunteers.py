import reflex as rx
from cyber_shield_reflex.state import State


def section_header_pill(step_num: str, title: str, subtitle: str, color_accent: str = "#38BDF8") -> rx.Component:
    """Header pill badge and typography banner for each core volunteer topic."""
    return rx.vstack(
        rx.hstack(
            rx.box(
                rx.text(
                    f"SECTION {step_num}",
                    font_size="11px",
                    font_weight="800",
                    color=color_accent,
                    font_family="'IBM Plex Mono', monospace",
                    letter_spacing="0.1em",
                ),
                padding="4px 12px",
                background=f"{color_accent}15",
                border=f"1px solid {color_accent}40",
                border_radius="20px",
            ),
            rx.box(
                rx.text(
                    "NATIONAL CYBER DEFENSE INITIATIVE",
                    font_size="11px",
                    font_weight="700",
                    color="#64748B",
                    font_family="'IBM Plex Mono', monospace",
                    letter_spacing="0.08em",
                ),
                padding="4px 10px",
            ),
            spacing="2",
            align="center",
            flex_wrap="wrap",
        ),
        rx.heading(
            title,
            font_size={"initial": "24px", "md": "30px"},
            font_weight="800",
            color="#FFFFFF",
            font_family="'Space Grotesk', sans-serif",
            letter_spacing="-0.02em",
            margin_top="10px",
            line_height="1.25",
        ),
        rx.text(
            subtitle,
            font_size={"initial": "14px", "md": "15px"},
            color="#94A3B8",
            font_family="'Outfit', sans-serif",
            line_height="1.6",
            max_width="920px",
            margin_top="4px",
        ),
        spacing="1",
        align="start",
        width="100%",
        margin_bottom="24px",
    )


def concept_card(title: str, role: str, description: str, key_duties: list[str], icon_name: str, color_accent: str) -> rx.Component:
    """Card explaining a specific volunteer classification under the Cyber Crime Volunteers Concept."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(icon_name, size=24, color=color_accent),
                    padding="12px",
                    background=f"{color_accent}15",
                    border=f"1px solid {color_accent}30",
                    border_radius="12px",
                ),
                rx.vstack(
                    rx.text(
                        role,
                        font_size="11px",
                        font_weight="800",
                        color=color_accent,
                        font_family="'IBM Plex Mono', monospace",
                        letter_spacing="0.08em",
                    ),
                    rx.heading(
                        title,
                        font_size="18px",
                        font_weight="700",
                        color="#F8FAFC",
                        font_family="'Space Grotesk', sans-serif",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.text(
                description,
                font_size="13px",
                color="#CBD5E1",
                font_family="'Outfit', sans-serif",
                line_height="1.6",
                margin_top="12px",
            ),
            rx.box(
                rx.text(
                    "PRIMARY RESPONSIBILITIES & CAPABILITIES",
                    font_size="10px",
                    font_weight="800",
                    color="#64748B",
                    font_family="'IBM Plex Mono', monospace",
                    letter_spacing="0.08em",
                    margin_bottom="8px",
                ),
                rx.vstack(
                    *[
                        rx.hstack(
                            rx.icon("check-circle-2", size=15, color=color_accent, style={"flex_shrink": "0"}),
                            rx.text(
                                duty,
                                font_size="12px",
                                color="#94A3B8",
                                font_family="'Outfit', sans-serif",
                                line_height="1.5",
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        )
                        for duty in key_duties
                    ],
                    spacing="2",
                    width="100%",
                ),
                width="100%",
                padding_top="14px",
                border_top="1px solid rgba(255, 255, 255, 0.08)",
                margin_top="14px",
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        padding="24px",
        background="linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(10, 15, 29, 0.9) 100%)",
        border="1px solid rgba(255, 255, 255, 0.08)",
        border_radius="16px",
        box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
        _hover={
            "border_color": color_accent,
            "transform": "translateY(-4px)",
            "box_shadow": f"0 12px 35px {color_accent}25",
        },
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        height="100%",
        width="100%",
    )


def why_needed_card(number: str, title: str, challenge: str, resolution: str, icon_name: str, color_accent: str) -> rx.Component:
    """Deep structural card explaining Why Volunteers Are Critically Needed in cyber defense."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.text(
                            number,
                            font_size="13px",
                            font_weight="800",
                            color="#FFFFFF",
                            font_family="'IBM Plex Mono', monospace",
                        ),
                        padding="6px 12px",
                        background=color_accent,
                        border_radius="8px",
                        box_shadow=f"0 2px 10px {color_accent}40",
                    ),
                    rx.heading(
                        title,
                        font_size="17px",
                        font_weight="700",
                        color="#F8FAFC",
                        font_family="'Space Grotesk', sans-serif",
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.icon(icon_name, size=22, color=color_accent),
                justify="between",
                align="center",
                width="100%",
            ),
            # Core Asymmetry / Challenge
            rx.box(
                rx.hstack(
                    rx.icon("alert-circle", size=15, color="#F87171", style={"flex_shrink": "0"}),
                    rx.text(
                        "The Threat Reality:",
                        font_size="11px",
                        font_weight="800",
                        color="#F87171",
                        font_family="'IBM Plex Mono', monospace",
                        letter_spacing="0.05em",
                    ),
                    spacing="1",
                    align="center",
                ),
                rx.text(
                    challenge,
                    font_size="13px",
                    color="#CBD5E1",
                    font_family="'Outfit', sans-serif",
                    line_height="1.55",
                    margin_top="6px",
                ),
                padding="12px 16px",
                background="rgba(239, 68, 68, 0.06)",
                border_left="3px solid #EF4444",
                border_radius="6px",
                width="100%",
                margin_top="14px",
            ),
            # Volunteer Solution
            rx.box(
                rx.hstack(
                    rx.icon("shield-check", size=15, color="#34D399", style={"flex_shrink": "0"}),
                    rx.text(
                        "Why Grassroots Volunteers Solve This:",
                        font_size="11px",
                        font_weight="800",
                        color="#34D399",
                        font_family="'IBM Plex Mono', monospace",
                        letter_spacing="0.05em",
                    ),
                    spacing="1",
                    align="center",
                ),
                rx.text(
                    resolution,
                    font_size="13px",
                    color="#94A3B8",
                    font_family="'Outfit', sans-serif",
                    line_height="1.55",
                    margin_top="6px",
                ),
                padding="12px 16px",
                background="rgba(16, 185, 129, 0.06)",
                border_left="3px solid #10B981",
                border_radius="6px",
                width="100%",
                margin_top="10px",
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        padding="24px",
        background="linear-gradient(135deg, rgba(15, 23, 42, 0.75) 0%, rgba(10, 15, 29, 0.85) 100%)",
        border="1px solid rgba(255, 255, 255, 0.08)",
        border_radius="16px",
        box_shadow="0 6px 24px rgba(0, 0, 0, 0.3)",
        _hover={
            "border_color": color_accent,
            "transform": "translateY(-4px)",
            "box_shadow": f"0 12px 30px {color_accent}20",
        },
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        height="100%",
        width="100%",
    )


def reduction_strategy_card(
    tag: str,
    title: str,
    how_it_reduces: str,
    action_steps: list[str],
    measurable_impact: str,
    icon_name: str,
    color_accent: str,
) -> rx.Component:
    """In-depth tactical card detailing How Volunteers Actively Reduce Cybercrime."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(icon_name, size=24, color=color_accent),
                    padding="12px",
                    background=f"{color_accent}15",
                    border=f"1px solid {color_accent}30",
                    border_radius="12px",
                ),
                rx.vstack(
                    rx.text(
                        tag,
                        font_size="10px",
                        font_weight="800",
                        color=color_accent,
                        font_family="'IBM Plex Mono', monospace",
                        letter_spacing="0.1em",
                    ),
                    rx.heading(
                        title,
                        font_size="18px",
                        font_weight="700",
                        color="#FFFFFF",
                        font_family="'Space Grotesk', sans-serif",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.text(
                how_it_reduces,
                font_size="13px",
                color="#CBD5E1",
                font_family="'Outfit', sans-serif",
                line_height="1.6",
                margin_top="12px",
            ),
            # Practical Action Steps
            rx.box(
                rx.text(
                    "CONCRETE VOLUNTEER ACTIONS",
                    font_size="10px",
                    font_weight="800",
                    color="#64748B",
                    font_family="'IBM Plex Mono', monospace",
                    letter_spacing="0.08em",
                    margin_bottom="8px",
                ),
                rx.vstack(
                    *[
                        rx.hstack(
                            rx.box(
                                width="5px",
                                height="5px",
                                border_radius="50%",
                                background=color_accent,
                                margin_top="7px",
                                style={"flex_shrink": "0"},
                            ),
                            rx.text(
                                step,
                                font_size="12px",
                                color="#94A3B8",
                                font_family="'Outfit', sans-serif",
                                line_height="1.5",
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        )
                        for step in action_steps
                    ],
                    spacing="2",
                    width="100%",
                ),
                width="100%",
                padding_top="12px",
                border_top="1px solid rgba(255, 255, 255, 0.08)",
                margin_top="12px",
            ),
            # Direct Measurable Impact Box
            rx.box(
                rx.hstack(
                    rx.icon("activity", size=14, color=color_accent, style={"flex_shrink": "0"}),
                    rx.text(
                        "Measurable Crime Reduction Impact:",
                        font_size="11px",
                        font_weight="800",
                        color=color_accent,
                        font_family="'IBM Plex Mono', monospace",
                    ),
                    spacing="1",
                    align="center",
                ),
                rx.text(
                    measurable_impact,
                    font_size="12px",
                    color="#E2E8F0",
                    font_family="'Outfit', sans-serif",
                    line_height="1.5",
                    margin_top="4px",
                ),
                padding="10px 14px",
                background=f"{color_accent}10",
                border=f"1px solid {color_accent}25",
                border_radius="8px",
                width="100%",
                margin_top="14px",
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        padding="24px",
        background="linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(10, 15, 29, 0.9) 100%)",
        border="1px solid rgba(255, 255, 255, 0.08)",
        border_radius="16px",
        box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
        _hover={
            "border_color": color_accent,
            "transform": "translateY(-4px)",
            "box_shadow": f"0 12px 35px {color_accent}25",
        },
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        height="100%",
        width="100%",
    )


def code_of_conduct_card() -> rx.Component:
    """Ethical, legal, and operational principles for Cyber Crime Volunteers."""
    principles = [
        ("Absolute Non-Vigilantism", "Volunteers operate strictly as observers, educators, and incident guides. Under no circumstances are volunteers authorized to hack back, conduct surveillance, or breach digital privacy."),
        ("Evidence Integrity & Immutability", "All digital artifacts (headers, UTR receipts, call recordings) must be handled without modification to maintain chain of custody and forensic court admissibility."),
        ("Official Portal Alignment", "All actionable threat intelligence and victim escalations are routed directly through the National Cyber Crime Reporting Portal (cybercrime.gov.in) and 1930 Helpline."),
        ("Community Empathy & Non-Judgment", "Victims of social engineering and cyber scams often experience severe guilt and panic. Volunteers provide reassuring, compassionate, and non-judgmental guidance."),
    ]
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon("scale", size=24, color="#F59E0B"),
                    padding="12px",
                    background="rgba(245, 158, 11, 0.15)",
                    border="1px solid rgba(245, 158, 11, 0.3)",
                    border_radius="12px",
                ),
                rx.vstack(
                    rx.text(
                        "ETHICAL & STATUTORY MANDATE",
                        font_size="11px",
                        font_weight="800",
                        color="#F59E0B",
                        font_family="'IBM Plex Mono', monospace",
                        letter_spacing="0.08em",
                    ),
                    rx.heading(
                        "Cyber Crime Volunteers Code of Ethics & Legal Framework",
                        font_size="20px",
                        font_weight="700",
                        color="#FFFFFF",
                        font_family="'Space Grotesk', sans-serif",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.text(
                "Operating in accordance with the Information Technology Act, 2000 and national cybersecurity guidelines, cyber volunteers serve the public interest with uncompromised integrity, legal compliance, and community trust.",
                font_size="13px",
                color="#CBD5E1",
                font_family="'Outfit', sans-serif",
                line_height="1.6",
                margin_top="10px",
            ),
            rx.grid(
                *[
                    rx.box(
                        rx.hstack(
                            rx.icon("shield", size=16, color="#F59E0B", style={"flex_shrink": "0"}),
                            rx.text(
                                title,
                                font_size="13px",
                                font_weight="700",
                                color="#FDE68A",
                                font_family="'Space Grotesk', sans-serif",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(
                            desc,
                            font_size="12px",
                            color="#94A3B8",
                            font_family="'Outfit', sans-serif",
                            line_height="1.5",
                            margin_top="6px",
                        ),
                        padding="14px",
                        background="rgba(245, 158, 11, 0.04)",
                        border="1px solid rgba(245, 158, 11, 0.15)",
                        border_radius="10px",
                    )
                    for title, desc in principles
                ],
                columns={"initial": "1", "md": "2"},
                spacing="4",
                width="100%",
                margin_top="16px",
            ),
            spacing="2",
            align="start",
            width="100%",
        ),
        padding="28px",
        background="linear-gradient(135deg, rgba(20, 24, 38, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%)",
        border="1px solid rgba(245, 158, 11, 0.25)",
        border_radius="16px",
        box_shadow="0 10px 30px rgba(0, 0, 0, 0.4)",
        width="100%",
        margin_top="24px",
    )


def volunteers_content() -> rx.Component:
    """
    Complete, In-Depth Cyber Crime Volunteers Component.
    Fully addresses:
    1. Cyber Crime Volunteers Concept in detail.
    2. Why we need volunteers in cybercrime mainly.
    3. How volunteers can actively reduce cybercrime.
    """
    return rx.box(
        rx.vstack(
            # Top Banner & Mission Hero
            rx.vstack(
                rx.hstack(
                    rx.box(
                        width="8px",
                        height="8px",
                        border_radius="50%",
                        background="#10B981",
                        box_shadow="0 0 12px #10B981",
                    ),
                    rx.text(
                        "CITIZEN DEFENSE & GRASSROOTS CYBER VIGILANCE",
                        font_size="12px",
                        font_weight="800",
                        color="#10B981",
                        font_family="'IBM Plex Mono', monospace",
                        letter_spacing="0.1em",
                    ),
                    spacing="2",
                    align="center",
                    padding="6px 14px",
                    background="rgba(16, 185, 129, 0.1)",
                    border="1px solid rgba(16, 185, 129, 0.25)",
                    border_radius="20px",
                ),
                rx.heading(
                    "National Cyber Crime Volunteers Initiative",
                    font_size={"initial": "32px", "md": "44px"},
                    font_weight="800",
                    color="#FFFFFF",
                    font_family="'Space Grotesk', sans-serif",
                    letter_spacing="-0.03em",
                    margin_top="12px",
                    line_height="1.2",
                    text_align="start",
                ),
                rx.text(
                    "A collaborative civil defense framework bridging ordinary citizens, technical researchers, and law enforcement agencies to identify digital threats, safeguard vulnerable populations, and systematically neutralize cyber syndicates across India.",
                    font_size={"initial": "15px", "md": "17px"},
                    color="#94A3B8",
                    font_family="'Outfit', sans-serif",
                    line_height="1.6",
                    max_width="960px",
                    margin_top="8px",
                ),
                # Quick Stat Badges
                rx.grid(
                    rx.box(
                        rx.hstack(
                            rx.icon("phone-call", size=20, color="#38BDF8"),
                            rx.vstack(
                                rx.text("1930 HELPLINE", font_size="11px", font_weight="800", color="#64748B", font_family="'IBM Plex Mono', monospace"),
                                rx.text("Golden Hour Freezing", font_size="13px", font_weight="700", color="#F8FAFC"),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        padding="14px 18px",
                        background="rgba(15, 23, 42, 0.7)",
                        border="1px solid rgba(56, 189, 248, 0.2)",
                        border_radius="10px",
                    ),
                    rx.box(
                        rx.hstack(
                            rx.icon("users", size=20, color="#10B981"),
                            rx.vstack(
                                rx.text("COMMUNITY RADAR", font_size="11px", font_weight="800", color="#64748B", font_family="'IBM Plex Mono', monospace"),
                                rx.text("Grassroots Inoculation", font_size="13px", font_weight="700", color="#F8FAFC"),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        padding="14px 18px",
                        background="rgba(15, 23, 42, 0.7)",
                        border="1px solid rgba(16, 185, 129, 0.2)",
                        border_radius="10px",
                    ),
                    rx.box(
                        rx.hstack(
                            rx.icon("shield-alert", size=20, color="#F59E0B"),
                            rx.vstack(
                                rx.text("THREAT SURVEILLANCE", font_size="11px", font_weight="800", color="#64748B", font_family="'IBM Plex Mono', monospace"),
                                rx.text("Mule & APK Disruption", font_size="13px", font_weight="700", color="#F8FAFC"),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        padding="14px 18px",
                        background="rgba(15, 23, 42, 0.7)",
                        border="1px solid rgba(245, 158, 11, 0.2)",
                        border_radius="10px",
                    ),
                    columns={"initial": "1", "sm": "3"},
                    spacing="4",
                    width="100%",
                    margin_top="20px",
                ),
                align="start",
                width="100%",
                padding_y="32px",
                border_bottom="1px solid rgba(255, 255, 255, 0.08)",
            ),

            # =========================================================================
            # PART 1: CYBER CRIME VOLUNTEERS CONCEPT (IN-DETAIL)
            # =========================================================================
            rx.box(
                section_header_pill(
                    "01",
                    "The Cyber Crime Volunteers Concept & National Architecture",
                    "Understanding the institutional framework initiated by national cyber agencies (such as I4C, Ministry of Home Affairs) to cultivate a participatory civil defense ecosystem against digital adversaries.",
                    color_accent="#38BDF8",
                ),
                # Concept Overview Manifesto Box
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "What is the Cyber Crime Volunteer Concept?",
                            font_size="20px",
                            font_weight="700",
                            color="#FFFFFF",
                            font_family="'Space Grotesk', sans-serif",
                        ),
                        rx.text(
                            "The Cyber Crime Volunteer Concept is an institutionalized civil-state partnership model designed to bring together dedicated citizens, ethical technologists, educators, and social advocates to fortify India's cyberspace. Recognizing that cyberspace is infinite and constantly evolving, the state cannot police every private forum, localized phishing campaign, or social engineering script in isolation. Cyber Volunteers serve as the nation's decentralized digital immune system—actively flagging unlawful digital artifacts, imparting vital cyber hygiene to vulnerable populations, and serving as empathetic first-aid navigators when a crime occurs.",
                            font_size="14px",
                            color="#CBD5E1",
                            font_family="'Outfit', sans-serif",
                            line_height="1.7",
                        ),
                        rx.text(
                            "Volunteers are not enforcement officers or vigilantes; they operate strictly within statutory boundaries, channeling vetted threat telemetry and victim cases directly to the National Cyber Crime Reporting Portal (NCRP) and state cyber police cells.",
                            font_size="14px",
                            color="#94A3B8",
                            font_family="'Outfit', sans-serif",
                            line_height="1.7",
                            font_weight="500",
                        ),
                        spacing="3",
                        align="start",
                    ),
                    padding="26px",
                    background="rgba(56, 189, 248, 0.04)",
                    border="1px solid rgba(56, 189, 248, 0.2)",
                    border_radius="14px",
                    margin_bottom="24px",
                    width="100%",
                ),
                # 3 Core Categories Grid
                rx.grid(
                    concept_card(
                        title="Cyber Awareness Promoters",
                        role="PILLAR 1 // GRASSROOTS EDUCATION",
                        description="Focuses on preventive digital literacy, public outreach, and immunizing non-technical citizens against psychological manipulation before fraud takes place.",
                        key_duties=[
                            "Conducting cyber safety workshops in schools, colleges, and Senior Citizen Welfare forums.",
                            "Demystifying modern scam patterns: Fake parcel seizures, 'Digital Arrest' hoaxes, and fake electricity cutoff SMS.",
                            "Educating small merchants and students never to share OTPs, PINs, or install unverified APK files.",
                            "Translating complex cyber advisories into local languages to bridge the vernacular digital divide.",
                        ],
                        icon_name="book-open",
                        color_accent="#38BDF8",
                    ),
                    concept_card(
                        title="Cyber Threat Observers",
                        role="PILLAR 2 // OPEN-SOURCE INTELLIGENCE",
                        description="Specialized technical observers who proactively survey the open web, public channels, and digital conduits to identify illegal or predatory digital assets.",
                        key_duties=[
                            "Detecting and reporting malicious phishing portals, spoofed banking domains, and fake government welfare sites.",
                            "Monitoring and flagging illegal loan applications, betting apps, and malicious APK files hosted on untrusted platforms.",
                            "Identifying Child Sexual Abuse Material (CSAM) and content promoting violent extremism or communal disharmony.",
                            "Cataloging fake customer support numbers indexed on search engines used by call-center fraudsters.",
                        ],
                        icon_name="search",
                        color_accent="#818CF8",
                    ),
                    concept_card(
                        title="Cyber First-Responders",
                        role="PILLAR 3 // GOLDEN HOUR NAVIGATION",
                        description="Empathetic community navigators who guide victims through the decisive first 1 to 3 hours after a cyber incident occurs to maximize asset recovery.",
                        key_duties=[
                            "Immediately assisting victims to dial the 1930 Financial Fraud Helpline and freeze transiting assets.",
                            "Collating forensic artifacts: UTR numbers, account receipts, email headers, and call recordings.",
                            "Guiding victims step-by-step through registering an official complaint on cybercrime.gov.in.",
                            "Providing psychological reassurance and eliminating the stigma and shame associated with being scammed.",
                        ],
                        icon_name="shield-check",
                        color_accent="#34D399",
                    ),
                    columns={"initial": "1", "md": "3"},
                    spacing="5",
                    width="100%",
                ),
                width="100%",
                padding_y="40px",
                border_bottom="1px solid rgba(255, 255, 255, 0.08)",
            ),

            # =========================================================================
            # PART 2: WHY DO WE NEED VOLUNTEERS IN CYBERCRIME MAINLY? (IN-DETAIL)
            # =========================================================================
            rx.box(
                section_header_pill(
                    "02",
                    "Why Do We Need Volunteers in Cybercrime Mainly?",
                    "Analyzing the structural bottlenecks in cyber defense: the vast asymmetry between automated criminal syndicates and finite institutional enforcement resources.",
                    color_accent="#F59E0B",
                ),
                rx.grid(
                    why_needed_card(
                        number="01",
                        title="Vast Asymmetry in Scale & Criminal Automation",
                        challenge="Transnational and interstate cyber syndicates utilize automated robocall dialers, AI voice cloners, bulk SMS gateways, and disposable server infrastructure to launch millions of attacks every single day. Institutional cyber cells possess finite officers and are severely outmatched by the sheer automated volume of attacks.",
                        resolution="Volunteers act as a massive decentralized surveillance radar. By crowdsourcing threat detection across every district and town, millions of suspicious touchpoints can be identified and neutralized long before police stations receive formal complaints.",
                        icon_name="cpu",
                        color_accent="#F59E0B",
                    ),
                    why_needed_card(
                        number="02",
                        title="The 'Last-Mile' Digital Divide & Rapid FinTech Adoption",
                        challenge="India's digital payment ecosystem (UPI, AePS, mobile banking) expanded at historic speed, bringing hundreds of millions of first-time digital users online. However, digital safety awareness did not grow at the same pace, leaving pensioners, students, and rural merchants uniquely vulnerable to fear-based social engineering.",
                        resolution="Centralized government press releases rarely penetrate grassroots communities in time. Local volunteers bridge this last-mile gap, delivering relatable, in-person education and vernacular advice directly to families and local shopkeepers.",
                        icon_name="users",
                        color_accent="#EC4899",
                    ),
                    why_needed_card(
                        number="03",
                        title="The Critical 'Golden Hour' Financial Freezing Window",
                        challenge="In financial cyber fraud, stolen money is transferred through 4 to 8 cascading 'mule' bank accounts within 60 to 120 minutes. If victims panic, visit the wrong local police station, or delay reporting by even 2 hours, the funds are cashed out at ATMs or converted to crypto, making recovery near impossible.",
                        resolution="Trained community volunteers provide instantaneous emergency triage: instructing the victim to dial 1930 immediately, pinpoint the exact transaction UTRs, and notify bank nodal officers while the money is still in transit.",
                        icon_name="clock",
                        color_accent="#10B981",
                    ),
                    why_needed_card(
                        number="04",
                        title="Hyper-Rapid Mutation of Scam Modus Operandi",
                        challenge="Cyber criminals continually modify their playbooks: shifting from simple OTP phishing to complex 'Digital Arrest' video calls impersonating CBI officers, fake work-from-home Telegram task scams, and malicious utility bill APK links. Official warning circulars often take weeks to formalize.",
                        resolution="Volunteers operating on the ground encounter newly circulating scam scripts and deceptive WhatsApp forwards within hours of launch. They flag novel patterns immediately, enabling AI defense systems and authorities to deploy countermeasures swiftly.",
                        icon_name="zap",
                        color_accent="#818CF8",
                    ),
                    why_needed_card(
                        number="05",
                        title="Overcoming Victim Guilt, Stigma & Chronic Under-Reporting",
                        challenge="Over 80% of cyber fraud victims never report their losses due to overwhelming feelings of shame, fear of family judgment, intimidation by legal procedures, or the erroneous belief that small losses cannot be investigated.",
                        resolution="Community volunteers remove the stigma of victimhood. By providing compassionate, confidential peer support and holding the victim's hand through the portal registration process, volunteers ensure hidden crimes are documented and investigated.",
                        icon_name="shield",
                        color_accent="#06B6D4",
                    ),
                    why_needed_card(
                        number="06",
                        title="Neutralizing Localized Money Mule & SIM Card Pipelines",
                        challenge="Cyber cartels rely on localized networks of college students, unbanked laborers, and gig workers who are coerced or bribed into opening 'mule' bank accounts and providing KYC SIM cards to receive laundered fraud funds.",
                        resolution="Volunteers in colleges, hostels, and residential colonies identify and expose mule recruitment drives before young citizens ruin their futures by participating in organized money laundering syndicates.",
                        icon_name="network",
                        color_accent="#EAB308",
                    ),
                    columns={"initial": "1", "md": "2", "lg": "3"},
                    spacing="5",
                    width="100%",
                ),
                width="100%",
                padding_y="40px",
                border_bottom="1px solid rgba(255, 255, 255, 0.08)",
            ),

            # =========================================================================
            # PART 3: HOW VOLUNTEERS CAN REDUCE CRIME (IN-DETAIL)
            # =========================================================================
            rx.box(
                section_header_pill(
                    "03",
                    "How Volunteers Can Actively Reduce Digital Crime",
                    "A step-by-step examination of concrete, tactical mechanisms through which trained volunteers systematically dismantle fraud networks and protect community assets.",
                    color_accent="#10B981",
                ),
                rx.grid(
                    reduction_strategy_card(
                        tag="STRATEGY 01 // PROACTIVE TAKEDOWN",
                        title="Crowdsourcing Threat Telemetry & Rapid Domain Disruption",
                        how_it_reduces="Fraud syndicates purchase thousands of lookalike domains and distribute malicious APKs every week. When hundreds of trained volunteers systematically crawl, detect, and report these deceptive endpoints, domain registrars, hosting providers, and telecom firewalls can block them before victims click.",
                        action_steps=[
                            "Scouting and logging fraudulent APK links mimicking SBI YONO, PM Kisan, and electricity discom portals.",
                            "Submitting verified phishing URLs directly to CERT-In and the National Cyber Crime Reporting Portal.",
                            "Reporting spoofed customer care numbers on Google Maps and search engine indexing consoles.",
                            "Coordinating with telecom nodal teams to block fraudulent WhatsApp and Telegram business accounts.",
                        ],
                        measurable_impact="Reduces the operational lifespan of phishing domains from days to mere hours, cutting criminal revenue by over 70%.",
                        icon_name="globe",
                        color_accent="#38BDF8",
                    ),
                    reduction_strategy_card(
                        tag="STRATEGY 02 // FINANCIAL FREEZING",
                        title="Executing 'Golden Hour' 1930 Emergency Interventions",
                        how_it_reduces="The Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS) under 1930 enables real-time inter-bank communication. Volunteers ensure victims act within minutes, dramatically raising the recovery rate of stolen money before it exits the banking network.",
                        action_steps=[
                            "Guiding victims through the mandatory call protocol to 1930 without panic.",
                            "Compiling the 12-digit UPI UTR numbers, beneficiary account numbers, and transaction timestamps.",
                            "Facilitating immediate liaison with bank nodal fraud desks to place liens on beneficiary mule accounts.",
                            "Ensuring a formal acknowledgment number is generated on cybercrime.gov.in within 24 hours.",
                        ],
                        measurable_impact="Increases fund recovery success from under 5% to over 65% when reported within the first 120 minutes of transaction.",
                        icon_name="landmark",
                        color_accent="#10B981",
                    ),
                    reduction_strategy_card(
                        tag="STRATEGY 03 // BEHAVIORAL INOCULATION",
                        title="Immunizing Communities Against Psychological Exploitation",
                        how_it_reduces="Cybercrime succeeds primarily by exploiting human emotions: fear (digital arrest, legal notices), greed (lottery, high-yield investment), and urgency (bill cutoff in 1 hour). By educating communities on these exact psychological triggers, volunteers inoculate citizens so scams fail on arrival.",
                        action_steps=[
                            "Demystifying 'Digital Arrest' scams: Emphasizing that Indian police and CBI NEVER interrogate or arrest over video calls.",
                            "Drilling the golden rule: 'Entering a UPI PIN or scanning a QR code is ONLY for sending money, NEVER for receiving money.'",
                            "Teaching seniors and merchants to verify caller claims through official landline numbers, not callback numbers.",
                            "Distributing one-page visual checklists on recognizing fake KYC and reward point SMS.",
                        ],
                        measurable_impact="Dramatically reduces victim susceptibility to social engineering scams across educated and uneducated demographics alike.",
                        icon_name="shield",
                        color_accent="#818CF8",
                    ),
                    reduction_strategy_card(
                        tag="STRATEGY 04 // MULE DISRUPTION",
                        title="Drying Up the Criminal Banking & SIM Card Infrastructure",
                        how_it_reduces="Cyber syndicates cannot steal money without a conduit to receive and cash it out. By exposing campus mule recruitment schemes and educating citizens on the legal perils of account-sharing, volunteers choke the financial infrastructure that criminal networks depend upon.",
                        action_steps=[
                            "Educating university students on Section 420 and PMLA liabilities of lending bank accounts or ATM cards.",
                            "Reporting suspicious Telegram channels advertising 'Earn Rs 5,000 daily by providing your current account.'",
                            "Partnering with local bank branches to spot suspicious bulk account openings by unregistered intermediaries.",
                            "Guiding unwitting mule victims on self-reporting to police before they are formally named as accused co-conspirators.",
                        ],
                        measurable_impact="Starves cyber cartels of disposable Indian bank accounts, forcing them into traceable channels where interception is high.",
                        icon_name="network",
                        color_accent="#F59E0B",
                    ),
                    reduction_strategy_card(
                        tag="STRATEGY 05 // FORENSIC EVIDENCE PRESERVATION",
                        title="Standardizing Court-Admissible Digital Evidence Packages",
                        how_it_reduces="Many cybercrime complaints collapse in court because victims accidentally delete chats, forward screenshots without metadata, or fail to save email headers. Volunteers ensure digital evidence is forensically sound from moment zero.",
                        action_steps=[
                            "Exporting original unedited chat logs, voice recordings, and SMS headers with full timestamps.",
                            "Capturing bank passbook statements highlighting exact debit timestamps and reference numbers.",
                            "Recording APK file hashes, destination IP addresses, or fraudulent payment gateway URLs.",
                            "Organizing all documentation into structured PDF complaint dossiers ready for cyber cell FIR registration.",
                        ],
                        measurable_impact="Speeds up police charge-sheet filing and boosts judicial conviction rates in specialized cyber tribunals.",
                        icon_name="file-text",
                        color_accent="#EC4899",
                    ),
                    reduction_strategy_card(
                        tag="STRATEGY 06 // VERNACULAR & RURAL EMPOWERMENT",
                        title="Extending Cyber Defense Beyond Urban Metros to Rural Districts",
                        how_it_reduces="Organized fraud networks have shifted their focus to Tier-3 cities, rural farming belts, and small business owners who lack English fluency. Volunteers who speak local dialects ensure no Indian citizen is left defenseless.",
                        action_steps=[
                            "Translating critical cyber safety alerts into regional vernacular languages (Hindi, Tamil, Telugu, Bengali, Marathi, etc.).",
                            "Conducting physical village panchayat and Krishi Vigyan Kendra workshops for farmers on PM-Kisan subsidy scams.",
                            "Advising local traders and micro-entrepreneurs on POS terminal safety and QR code tampering risks.",
                            "Operating local drop-in assistance desks on weekly market days for quick fraud verification.",
                        ],
                        measurable_impact="Closes the regional vulnerability gap that fraudsters exploit, ensuring pan-India digital defense resilience.",
                        icon_name="users",
                        color_accent="#06B6D4",
                    ),
                    columns={"initial": "1", "md": "2", "lg": "3"},
                    spacing="5",
                    width="100%",
                ),
                width="100%",
                padding_y="40px",
                border_bottom="1px solid rgba(255, 255, 255, 0.08)",
            ),

            # =========================================================================
            # ETHICS, MANDATE & OFFICIAL VOLUNTEER ENROLLMENT PORTAL
            # =========================================================================
            code_of_conduct_card(),

            # Government Portal Action Box
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("landmark", size=24, color="#38BDF8"),
                        rx.heading(
                            "Register as a Cyber Volunteer on the Official Government Portal",
                            font_size="20px",
                            font_weight="700",
                            color="#FFFFFF",
                            font_family="'Space Grotesk', sans-serif",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    rx.text(
                        "The Ministry of Home Affairs (MHA) under the Indian Cyber Crime Coordination Centre (I4C) invites citizens to formally register as Cyber Crime Volunteers on the National Cyber Crime Reporting Portal. Any Indian citizen can contribute towards digital safety as an Awareness Promoter, Cyber Threat Observer, or Technical Expert.",
                        font_size="14px",
                        color="#CBD5E1",
                        font_family="'Outfit', sans-serif",
                        line_height="1.6",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.text("Visit Official Volunteer Registration Portal", font_size="14px", font_weight="700"),
                                    rx.icon("external-link", size=16),
                                    spacing="2",
                                    align="center",
                                ),
                                background="linear-gradient(90deg, #1D4ED8 0%, #0284C7 100%)",
                                color="#FFFFFF",
                                padding_x="24px",
                                padding_y="12px",
                                border_radius="8px",
                                box_shadow="0 4px 15px rgba(2, 132, 199, 0.4)",
                                cursor="pointer",
                                _hover={"opacity": 0.95, "transform": "translateY(-2px)"},
                            ),
                            href="https://cybercrime.gov.in/Webform/Volunteer_Registration.aspx",
                            is_external=True,
                        ),
                        rx.button(
                            "Emergency Helpline: 1930",
                            variant="surface",
                            color_scheme="sky",
                            font_weight="700",
                            font_size="14px",
                            font_family="'IBM Plex Mono', monospace",
                            padding_x="20px",
                            padding_y="12px",
                            border_radius="8px",
                            on_click=State.toggle_complaint_modal,  # type: ignore
                            cursor="pointer",
                        ),
                        spacing="4",
                        align="center",
                        flex_wrap="wrap",
                        margin_top="12px",
                    ),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                padding="28px",
                background="linear-gradient(135deg, rgba(30, 58, 138, 0.25) 0%, rgba(15, 23, 42, 0.8) 100%)",
                border="1px solid rgba(56, 189, 248, 0.3)",
                border_radius="16px",
                margin_top="32px",
                margin_bottom="40px",
                width="100%",
            ),

            width="100%",
            spacing="0",
            align="start",
        ),
        width="100%",
        max_width="1280px",
        margin_x="auto",
    )
