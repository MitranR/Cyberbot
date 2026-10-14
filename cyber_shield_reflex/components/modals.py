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
                
                # Section 3: Step-by-Step Guide to Register Complaint on Government Portal
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.icon("clipboard-check", size=18, color="#0056D2"),
                            background="#EBF5FF",
                            border_radius="50%",
                            padding="4px",
                        ),
                        rx.text(
                            "Steps to Successfully Register Complaint on Government Portal:",
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
                            rx.box(
                                rx.text("Step 1: Access Portal & Accept Terms", font_size="13px", font_weight="700", color="#0F172A", font_family="'Outfit', sans-serif"),
                                rx.text("Visit the official portal at cybercrime.gov.in and click on 'File a Complaint' or 'Report Cyber Crime'. Read the advisory disclaimer and click 'I Accept' to proceed.", font_size="12px", color="#475569", font_family="'Outfit', sans-serif"),
                                margin_bottom="6px",
                            ),
                            rx.box(
                                rx.text("Step 2: Citizen Login & OTP Verification", font_size="13px", font_weight="700", color="#0F172A", font_family="'Outfit', sans-serif"),
                                rx.text("Select 'Citizen Login', choose your State / Union Territory, enter your Name and Mobile Number, then enter the OTP received on your mobile phone to authenticate.", font_size="12px", color="#475569", font_family="'Outfit', sans-serif"),
                                margin_bottom="6px",
                            ),
                            rx.box(
                                rx.text("Step 3: Select Fraud Category", font_size="13px", font_weight="700", color="#0F172A", font_family="'Outfit', sans-serif"),
                                rx.text("Select 'Financial Cyber Fraud' (for UPI/banking/OTP money loss) or 'Report Other Cyber Crime' (for identity theft, phishing, voice scams, social media hacking).", font_size="12px", color="#475569", font_family="'Outfit', sans-serif"),
                                margin_bottom="6px",
                            ),
                            rx.box(
                                rx.text("Step 4: Enter Incident & Suspect Information", font_size="13px", font_weight="700", color="#0F172A", font_family="'Outfit', sans-serif"),
                                rx.text("Enter incident date and time, a detailed narrative description (min 200 characters), bank account/UTR details, transaction amount, and suspect mobile numbers, URLs, or accounts.", font_size="12px", color="#475569", font_family="'Outfit', sans-serif"),
                                margin_bottom="6px",
                            ),
                            rx.box(
                                rx.text("Step 5: Upload Supporting Digital Evidence", font_size="13px", font_weight="700", color="#0F172A", font_family="'Outfit', sans-serif"),
                                rx.text("Upload a soft copy of your National ID (Aadhaar/PAN/Voter ID) and digital evidence (transaction receipts, screenshots, bank statements, or audio recordings ≤ 10 MB each).", font_size="12px", color="#475569", font_family="'Outfit', sans-serif"),
                                margin_bottom="6px",
                            ),
                            rx.box(
                                rx.text("Step 6: Submit & Save Acknowledgement Number", font_size="13px", font_weight="700", color="#0F172A", font_family="'Outfit', sans-serif"),
                                rx.text("Review your summary, submit the complaint, and note down the unique Acknowledgement Number sent via SMS and Email to track police action and report to your bank.", font_size="12px", color="#475569", font_family="'Outfit', sans-serif"),
                            ),
                            spacing="2",
                            align="start",
                        ),
                        padding="14px",
                        background="#FFFFFF",
                        border="1px solid #E2E8F0",
                        border_radius="6px",
                    ),
                    margin_top="16px",
                    width="100%",
                ),

                # Section 4: Official Government Complaint Registration Link
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.icon("external-link", size=18, color="#0056D2"),
                            background="#EBF5FF",
                            border_radius="50%",
                            padding="4px",
                        ),
                        rx.text(
                            "Official Government Complaint Registration Link:",
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
                            rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        "National Cyber Crime Reporting Portal (NCCRP)",
                                        font_size="14px",
                                        font_weight="700",
                                        color="#0F172A",
                                        font_family="'Space Grotesk', sans-serif",
                                    ),
                                    rx.text(
                                        "Ministry of Home Affairs (MHA), Government of India",
                                        font_size="12px",
                                        color="#64748B",
                                        font_family="'Outfit', sans-serif",
                                    ),
                                    rx.hstack(
                                        rx.icon("phone-call", size=14, color="#16A34A"),
                                        rx.text(
                                            "National Cyber Helpline: 1930 (Toll-Free 24x7)",
                                            font_size="12px",
                                            font_weight="700",
                                            color="#16A34A",
                                            font_family="'IBM Plex Mono', monospace",
                                        ),
                                        spacing="1",
                                        align="center",
                                    ),
                                    spacing="1",
                                    align="start",
                                ),
                                rx.spacer(),
                                rx.link(
                                    rx.button(
                                        rx.hstack(
                                            rx.text("Open Official Portal", font_weight="700", font_size="13px"),
                                            rx.icon("arrow-up-right", size=15),
                                            spacing="1",
                                            align="center",
                                        ),
                                        background="#0056D2",
                                        color="#FFFFFF",
                                        padding_x="18px",
                                        padding_y="10px",
                                        border_radius="6px",
                                        cursor="pointer",
                                        _hover={"background": "#0040A8"},
                                    ),
                                    href="https://cybercrime.gov.in/",
                                    is_external=True,
                                ),
                                width="100%",
                                align="center",
                                wrap="wrap",
                                spacing="3",
                            ),
                            rx.box(
                                rx.hstack(
                                    rx.text(
                                        "Official Portal Link: ",
                                        font_size="12px",
                                        font_weight="600",
                                        color="#475569",
                                    ),
                                    rx.link(
                                        "https://cybercrime.gov.in/",
                                        href="https://cybercrime.gov.in/",
                                        is_external=True,
                                        color="#0056D2",
                                        font_weight="700",
                                        font_size="12px",
                                        text_decoration="underline",
                                    ),
                                    spacing="1",
                                    align="center",
                                ),
                                padding_top="8px",
                                border_top="1px dashed #CBD5E1",
                                width="100%",
                                margin_top="8px",
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        padding="16px",
                        background="#F0F7FF",
                        border="1px solid #BFDBFE",
                        border_radius="8px",
                        width="100%",
                    ),
                    margin_top="16px",
                    width="100%",
                ),
                
                # Bottom Action Buttons
                rx.hstack(
                    rx.button(
                        "I Understand / Close",
                        variant="surface",
                        color_scheme="gray",
                        size="2",
                        on_click=State.toggle_complaint_modal,  # type: ignore
                        cursor="pointer",
                    ),
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon("shield-alert", size=15),
                                rx.text("Proceed to Official Complaint Portal", font_weight="700", font_size="13px"),
                                rx.icon("arrow-up-right", size=14),
                                spacing="2",
                                align="center",
                            ),
                            background="linear-gradient(90deg, #0056D2 0%, #0088FF 100%)",
                            color="#FFFFFF",
                            padding_x="22px",
                            padding_y="10px",
                            border_radius="6px",
                            cursor="pointer",
                            _hover={"opacity": 0.95, "transform": "translateY(-1px)"},
                        ),
                        href="https://cybercrime.gov.in/",
                        is_external=True,
                    ),
                    justify="between",
                    width="100%",
                    margin_top="20px",
                    padding_top="14px",
                    border_top="1px solid #E2E8F0",
                ),
                padding="20px",
                width="100%",
                max_height="78vh",
                overflow_y="auto",
            ),
            padding="0",
            max_width="760px",
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
                    "This Website is designed, developed, and maintained by the Cyber Fraud Shield AI Engineering & Platform Administration Team. The contents of this website are for information, voice fraud intelligence, and educational cybercrime prevention purposes, enabling the public to have quick access to AI voice analysis tools and cyber fraud reporting features.",
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
