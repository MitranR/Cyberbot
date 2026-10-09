import reflex as rx
from cyber_shield_reflex.state import State


def complaint_prerequisites_modal() -> rx.Component:
    """
    Dialog box that opens when clicking 'Register a Complaint'.
    Displays mandatory and optional information requirements before filing a complaint.
    Matches the official National Cyber Crime Reporting Portal interface design.
    """
    return rx.dialog.root(
        rx.dialog.content(
            # Top Blue Header Bar
            rx.hstack(
                rx.text(
                    "Please keep this information ready before filing your complaint:",
                    font_size="15px",
                    font_weight="700",
                    color="#FFFFFF",
                    font_family="'Outfit', sans-serif",
                ),
                rx.icon(
                    "x",
                    size=20,
                    color="#FFFFFF",
                    cursor="pointer",
                    on_click=State.toggle_complaint_modal,  # type: ignore
                ),
                justify="between",
                align="center",
                background="linear-gradient(90deg, #0056D2 0%, #0088FF 100%)",
                padding="14px 20px",
                border_top_left_radius="8px",
                border_top_right_radius="8px",
            ),
            
            # Modal Body Content
            rx.vstack(
                # Section 1: Mandatory Information
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.icon("circle-alert", size=18, color="#0056D2"),
                            background="#EBF5FF",
                            border_radius="50%",
                            padding="4px",
                        ),
                        rx.text(
                            "Mandatory Information",
                            font_size="14px",
                            font_weight="700",
                            color="#0056D2",
                            font_family="'Outfit', sans-serif",
                        ),
                        spacing="2",
                        align="center",
                        margin_bottom="10px",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("1. Incident Date and Time.", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                            rx.text('2. Incident details (minimum 200 characters) without any special characters (#$@^*\' "~!).', font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                            rx.text("3. Soft copy of any national Id ( Voter Id, Driving license, Passport, PAN Card, Aadhar Card) of complainant in .jpeg, .jpg, .png format (file size should not be more than 5 MB).", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                            rx.text("4. In case of Financial crime, please keep following information ready:", font_size="12px", font_weight="700", color="#9333EA", font_family="'Outfit', sans-serif"),
                            rx.vstack(
                                rx.text("i) Name of the Bank/ Wallet/Merchant", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                                rx.text("ii) 12-digit Transaction id/UTR No.", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                                rx.text("iii) Date of transaction", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                                rx.text("iv) Fraud amount", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                                spacing="1",
                                padding_left="16px",
                                align="start",
                            ),
                            rx.text("5. Soft copy of all the relevant evidences related to the cyber crime (not more than 10 MB each)", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                            spacing="2",
                            align="start",
                        ),
                        padding="14px",
                        background="#FFFFFF",
                        border="1px solid #E2E8F0",
                        border_radius="6px",
                    ),
                    margin_bottom="16px",
                    width="100%",
                ),
                
                # Section 2: Optional/Desirable Information
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.icon("arrow-up-down", size=18, color="#0056D2"),
                            background="#EBF5FF",
                            border_radius="50%",
                            padding="4px",
                        ),
                        rx.text(
                            "Optional/Desirable Information:",
                            font_size="14px",
                            font_weight="700",
                            color="#0056D2",
                            font_family="'Outfit', sans-serif",
                        ),
                        spacing="2",
                        align="center",
                        margin_bottom="10px",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("1. Suspected website URLs/ Social Media handles (wherever applicable)", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                            rx.text("2. Suspect Details (if available)", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                            rx.vstack(
                                rx.text("i) Mobile No", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                                rx.text("ii) Email id", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                                rx.text("iii) Bank Account No", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                                rx.text("iv) Address", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                                rx.text("v) Soft copy of photograph of suspect in .jpeg, .jpg, .png format (not more than 5 MB)", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                                rx.text("vi) Any other document through which suspect can be identified.", font_size="12px", color="#334155", font_family="'Outfit', sans-serif"),
                                spacing="1",
                                padding_left="16px",
                                align="start",
                            ),
                            spacing="2",
                            align="start",
                        ),
                        padding="14px",
                        background="#FFFFFF",
                        border="1px solid #E2E8F0",
                        border_radius="6px",
                    ),
                    width="100%",
                ),
                
                # Bottom Action Button
                rx.hstack(
                    rx.button(
                        "I Understand",
                        background="#00A3E0",
                        color="#FFFFFF",
                        font_weight="700",
                        font_size="13px",
                        padding_x="20px",
                        padding_y="10px",
                        border_radius="4px",
                        on_click=State.proceed_to_complaint,  # type: ignore
                        cursor="pointer",
                        _hover={"background": "#0088C6"},
                    ),
                    justify="end",
                    width="100%",
                    margin_top="16px",
                ),
                padding="20px",
                width="100%",
            ),
            padding="0",
            max_width="720px",
            border_radius="8px",
            background="#F8FAFC",
            box_shadow="0 10px 25px rgba(0, 0, 0, 0.2)",
            overflow="hidden",
        ),
        open=State.complaint_modal_open,
    )


def disclaimer_modal() -> rx.Component:
    """
    Disclaimer Modal for Cyber Fraud Shield Platform.
    Customized for platform team and research administration.
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.hstack(
                rx.heading("Disclaimer & Terms of Use", font_size="16px", font_weight="700", color="#0A1F2E", font_family="'Space Grotesk', sans-serif"),
                rx.icon("x", size=18, color="#5A6E72", cursor="pointer", on_click=State.toggle_disclaimer_modal),  # type: ignore
                justify="between",
                align="center",
                margin_bottom="14px",
            ),
            rx.vstack(
                rx.text(
                    "This Website is designed, developed, and maintained by the Cyber Fraud Shield AI Engineering & Platform Administration Team. The contents of this website are for information, voice fraud intelligence, and educational cybercrime prevention purposes, enabling the public to have quick access to AI voice analysis tools and suspect reporting features.",
                    font_size="13px",
                    color="#334155",
                    font_family="'Outfit', sans-serif",
                    line_height="1.6",
                ),
                rx.text(
                    "We take every effort to provide accurate, real-time AI threat predictions and updated information. However, details such as model parameters, phone numbers, or threat scores are subject to continuous algorithmic updates. Hence, we do not assume legal liability on the completeness, accuracy, or usefulness of the automated predictions provided on this website.",
                    font_size="13px",
                    color="#334155",
                    font_family="'Outfit', sans-serif",
                    line_height="1.6",
                ),
                rx.text(
                    "The links are provided to external tools and reporting portals. We are not responsible for the accuracy of contents in those external sites, and hyperlinks do not constitute an endorsement of third-party services.",
                    font_size="13px",
                    color="#334155",
                    font_family="'Outfit', sans-serif",
                    line_height="1.6",
                ),
                rx.text(
                    "Despite our best technical efforts, we recommend users maintain updated anti-virus and security protection. We welcome your suggestions to improve our platform and request that any error found may kindly be brought to our notice.",
                    font_size="13px",
                    color="#334155",
                    font_family="'Outfit', sans-serif",
                    line_height="1.6",
                ),
                rx.text("Thanks for visiting our site.", font_size="13px", font_weight="700", color="#1B6E5B"),
                rx.text("Website Administration & AI Engineering Team", font_size="12px", font_weight="600", color="#5A6E72", font_family="'IBM Plex Mono', monospace"),
                spacing="3",
                align="start",
            ),
            rx.hstack(
                rx.button("Close", variant="soft", color_scheme="gray", on_click=State.toggle_disclaimer_modal, cursor="pointer"),  # type: ignore
                justify="end",
                margin_top="16px",
                width="100%",
            ),
            padding="24px",
            max_width="560px",
            border_radius="10px",
            background="#FFFFFF",
        ),
        open=State.disclaimer_modal_open,
    )
