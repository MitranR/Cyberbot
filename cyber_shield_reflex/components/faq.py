import reflex as rx


FAQS_DATA = [
    (
        "What is the purpose of National Cyber Crime Reporting Portal?",
        "The National Cyber Crime Reporting Portal (cybercrime.gov.in) is an initiative of the Ministry of Home Affairs (MHA), Government of India, to facilitate victims/complainants to report cybercrime complaints online, with special focus on cyber crimes against women and children, as well as financial fraud."
    ),
    (
        "What is CSEAM - Child Sexual Exploitative and Abuse Material?",
        "CSEAM refers to Child Sexual Abuse Material or Child Sexual Exploitation and Abuse Material. Reporting CSEAM content allows law enforcement agencies to urgently remove illegal materials and investigate offenders under IT Act Sections 67B and POCSO provisions."
    ),
    (
        "Apart from this portal, are there any alternative ways to remove objectionable content from social media websites?",
        "Yes, complainants can report objectionable content directly through the grievance reporting mechanisms provided on respective social media platforms (Meta, X, YouTube) or contact the Grievance Officer designated by the platform under the Information Technology Rules, 2021."
    ),
    (
        "Which type of cybercrimes I can report on the portal?",
        "You can report all major categories of cybercrimes, including Financial Cyber Fraud (banking scams, OTP fraud, UPI fraud), Cyber Crimes against Women & Children, Identity Theft, Phishing, Ransomware, Social Media Hacking, and Fake Caller ID / Voice Spoofing scams."
    ),
    (
        "What kind of information, should I provide to report complaint?",
        "You should provide accurate incident details including date and time, suspect phone numbers/emails, bank transaction IDs (for financial fraud), screenshots/URL links, audio recording files (for voice scams), and valid identity verification details."
    ),
    (
        "Which State/ UT shall I select while reporting a complaint?",
        "Complainants should select the State/Union Territory where they reside or where the incident took place so the complaint can be automatically routed to the concerned local cyber crime police station for investigation."
    ),
    (
        "How can I file the complaints about other cybercrimes?",
        "On the portal, select 'Report Other Cyber Crime' option, choose the specific incident category (e.g. email phishing, social media account compromise), enter the event log details, upload evidence files, and submit."
    ),
    (
        "What type of information would be considered as evidence while filing my complaint related to cybercrime?",
        "Valid digital evidence includes bank account statements/transaction receipts, SMS messages, WhatsApp chat exports, call recordings/audio files, email headers (.eml or .msg files), website URLs, and server log files."
    ),
    (
        "What action will be taken if complainant reports any false complaint/information?",
        "Providing false or misleading information to law enforcement is a punishable offense under Section 182 / Section 211 of the Indian Penal Code (IPC) / Bharatiya Nyaya Sanhita (BNS) and may lead to legal prosecution."
    ),
    (
        "Can I report a complaint without uploading any information?",
        "Basic mandatory details such as incident description, State/UT, and contact info are required to register an actionable complaint. Supporting digital evidence files can be uploaded during or after initial registration."
    ),
    (
        "What happens once I report a complaint?",
        "Once submitted, your complaint is assigned a unique Acknowledgement Number and automatically dispatched to the designated State/UT Cyber Crime Police Unit for preliminary verification and formal FIR registration."
    ),
    (
        "Will I be informed that my complaint has been submitted successfully?",
        "Yes, an instant SMS alert and email confirmation containing your unique Acknowledgement Number will be dispatched to your registered mobile number and email ID upon successful submission."
    ),
    (
        "Can I check the status of my complaint?",
        "Yes, complainants can track live complaint status anytime by entering their Acknowledgement Number on the portal or helpline dashboard."
    ),
    (
        "Can I withdraw my complaint from the portal?",
        "Once registered and routed to police authorities, complaints cannot be automatically deleted online, but complainants may submit a written withdrawal request directly to the investigating officer at the assigned police station."
    ),
    (
        "What is Hash value and what is its purpose?",
        "A Hash value (e.g. SHA-256 or MD5) is a unique cryptographic digital fingerprint generated from a file. It proves the authenticity and integrity of digital evidence in court by demonstrating that the file was not altered after acquisition."
    ),
    (
        "Can I file a complaint if I am an Indian citizen or non-citizen victimized in cyberspace?",
        "Yes. Indian citizens victimized online by foreign entities, as well as foreign nationals victimized by individuals or companies operating within India, can report complaints on the portal for legal action under Indian cyber laws."
    ),
]


def render_faq_item(q_a: tuple) -> rx.Component:
    """Renders a single FAQ accordion item."""
    question, answer = q_a
    return rx.accordion.item(
        header=rx.text(
            question,
            font_size="15px",
            font_weight="600",
            color="#0F172A",
            font_family="'Outfit', sans-serif",
        ),
        content=rx.text(
            answer,
            font_size="14px",
            color="#475569",
            font_family="'Outfit', sans-serif",
            line_height="1.6",
        ),
    )


def faq() -> rx.Component:
    """
    16 Official Government FAQs Accordion Component.
    Stretches edge-to-edge 100% full width across the screen.
    """
    return rx.box(
        rx.box(
            rx.vstack(
                rx.vstack(
                    rx.text("FREQUENTLY ASKED QUESTIONS", font_size="11px", font_weight="700", color="#0284C7", font_family="'IBM Plex Mono', monospace", letter_spacing="0.1em"),
                    rx.heading("Official Cyber Crime Reporting Guidance & FAQs", font_size="28px", font_weight="800", color="#0F172A", font_family="'Space Grotesk', sans-serif"),
                    rx.text("Authoritative answers to common questions regarding cybercrime reporting, evidence handling, and legal action.", font_size="15px", color="#475569", font_family="'Outfit', sans-serif"),
                    spacing="1",
                    align="center",
                    text_align="center",
                    margin_bottom="24px",
                ),
                
                rx.accordion.root(
                    *[render_faq_item(item) for item in FAQS_DATA],
                    collapsible=True,
                    width="100%",
                    variant="outline",
                ),
                spacing="4",
                align="center",
                padding_y="48px",
                width="100%",
            ),
            width="100%",
            padding_x={"initial": "16px", "md": "48px"},
        ),
        width="100%",
        background="#FFFFFF",
        border_top="1px solid #E2E8F0",
        id="faq-section",
    )
