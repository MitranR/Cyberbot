import re
from datetime import datetime
from typing import Dict, Any, List


def extract_identifiers(text: str) -> Dict[str, Any]:
    """
    Extracts forensic digital identifiers from call transcripts or SMS messages:
    phone numbers, sender headers, URLs/domains, UPI VPAs, and detected impersonated entity.
    """
    text_lower = (text or "").lower()
    
    # 1. Phone numbers (Indian cellular, toll-free 1800, landlines, or international format)
    raw_phones = re.findall(
        r'(?:\+?91[\s-]?)?[6-9]\d{9}|\b1800[\s-]?\d{3}[\s-]?\d{4}\b|\b\d{3,5}[\s-]?\d{6,8}\b',
        text
    )
    # Deduplicate while preserving order
    phones = []
    for p in raw_phones:
        cleaned_p = re.sub(r'[\s-]', '', p)
        if cleaned_p not in [re.sub(r'[\s-]', '', x) for x in phones]:
            phones.append(p)

    # 2. URLs & Malicious Domains (filter out common media file extensions)
    raw_urls = re.findall(
        r'(?:https?://|www\.)[^\s,]+|\b[a-zA-Z0-9.-]+\.(?:invalid|com|net|org|in|xyz|top|app|info|biz|site|online)(?:/[^\s,]*)?',
        text
    )
    urls = [
        u.rstrip(".,;)") for u in raw_urls 
        if not u.endswith((".wav", ".mp3", ".ogg", ".png", ".jpg", ".jpeg", ".csv", ".json"))
    ]
    urls = list(dict.fromkeys(urls))

    # 3. SMS Sender Headers (TRAI format e.g. AX-HDFCBK, VK-SBIINB, BZ-AIRTEL)
    headers = list(dict.fromkeys(re.findall(r'\b[A-Za-z]{2}-[A-Za-z0-9]{4,}\b', text)))

    # 4. UPI Virtual Private Addresses (VPAs)
    upis = list(dict.fromkeys(re.findall(r'[a-zA-Z0-9.\-_]{2,49}@[a-zA-Z]{2,}', text)))

    # 5. Detected Impersonated Entity / Agency
    impersonated = "Unknown / Deceptive Impersonation"
    if any(w in text_lower for w in ["cbi", "police", "narcotics", "court", "warrant", "arrest", "customs drugs", "trai arrest", "digital arrest"]):
        impersonated = "Law Enforcement / Police / CBI / Judiciary"
    elif any(w in text_lower for w in ["hdfc", "sbi", "icici", "axis", "bank", "kyc", "rbi", "debit card", "credit card", "atm card", "cvv", "branch"]):
        impersonated = "Bank Official / KYC Verification Officer"
    elif any(w in text_lower for w in ["electricity", "power connection", "tneb", "bses", "bescom", "meter", "cutoff", "power line"]):
        impersonated = "State Electricity Distribution Board"
    elif any(w in text_lower for w in ["fedex", "bluedart", "dhl", "courier", "parcel", "customs", "delivery", "shipment"]):
        impersonated = "Courier Service / Customs Clearance Authority"
    elif any(w in text_lower for w in ["airtel", "jio", "vi", "bsnl", "sim", "telecom", "trai", "sim swap", "sim replacement"]):
        impersonated = "Telecom Provider / TRAI Regulatory Body"
    elif any(w in text_lower for w in ["microsoft", "google", "anydesk", "teamviewer", "technician", "cleaner app", "virus warning"]):
        impersonated = "Tech Support / Software Vendor"
    elif any(w in text_lower for w in ["job", "recruiter", "salary", "work from home", "telegram task", "daily income"]):
        impersonated = "Recruitment Firm / Task Scheme Representative"
    elif any(w in text_lower for w in ["lottery", "lucky draw", "prize", "points expire", "reward points"]):
        impersonated = "Prize Dispatcher / Reward Points Desk"
    elif any(w in text_lower for w in ["loan", "micro-credit", "instant cash", "advance fee"]):
        impersonated = "Non-Banking Financial / Instant Loan App"

    return {
        "phones": phones,
        "urls": urls,
        "headers": headers,
        "upis": upis,
        "impersonated": impersonated
    }


def map_ncrp_category(threat_type: str, text: str) -> tuple[str, str]:
    """
    Maps threat classifications and message text to official National Cyber Crime
    Reporting Portal (NCRP - cybercrime.gov.in) Primary Category and Sub-Category.
    """
    t_combined = (threat_type + " " + (text or "")).lower()

    if any(w in t_combined for w in ["digital arrest", "police", "cbi", "narcotics", "arrest", "warrant", "court"]):
        return ("Other Cyber Crime", "Digital Arrest / Impersonation of Law Enforcement")
    elif any(w in t_combined for w in ["upi", "qr code", "collect request", "refund", "qr"]):
        return ("Online Financial Fraud", "UPI Related Fraud")
    elif any(w in t_combined for w in ["electricity", "power connection", "meter", "cutoff"]):
        return ("Online Financial Fraud", "Utility / Electricity Bill Disconnection Scam")
    elif any(w in t_combined for w in ["parcel", "courier", "fedex", "customs", "bluedart", "dhl"]):
        return ("Online Financial Fraud", "Courier / Customs Parcel Extortion Scam")
    elif any(w in t_combined for w in ["job", "task", "work from home", "salary", "telegram task"]):
        return ("Online Financial Fraud", "Job / Telegram Task / Work-From-Home Scam")
    elif any(w in t_combined for w in ["sim swap", "lost signal", "sim deactivation", "trai", "lost service"]):
        return ("Other Cyber Crime", "SIM Swap / Telecom Fraud")
    elif any(w in t_combined for w in ["lottery", "lucky draw", "prize", "points expire", "reward points"]):
        return ("Online Financial Fraud", "Lottery / Prize / Reward Points Fraud")
    elif any(w in t_combined for w in ["apk", "trojan", "anydesk", "teamviewer", "remote access"]):
        return ("Other Cyber Crime", "Malicious APK / Remote Device Takeover")
    elif any(w in t_combined for w in ["loan", "micro-credit", "loan approved"]):
        return ("Online Financial Fraud", "Instant Loan App / Micro-Credit Fraud")
    elif any(w in t_combined for w in ["crypto", "cryptocurrency", "bitcoin", "investment return", "guaranteed return"]):
        return ("Online Financial Fraud", "Cryptocurrency & Fake Investment Scheme")
    elif any(w in t_combined for w in ["bank", "kyc", "otp", "debit card", "credit card", "cvv", "pin"]):
        return ("Online Financial Fraud", "Internet Banking / KYC Credential Phishing")
    else:
        return ("Online Financial Fraud", "Phishing / Social Engineering Cyber Fraud")


def get_applicable_legal_sections(category: str, subcategory: str, text: str) -> List[str]:
    """
    Returns statutory penal charges under the Information Technology Act, 2000
    and Bharatiya Nyaya Sanhita (BNS) 2023 / Indian Penal Code (IPC).
    """
    t = (text or "").lower()
    sections = [
        "Section 66D, Information Technology Act, 2000 (Cheating by Personation using Computer Resource)",
        "Section 318(4), Bharatiya Nyaya Sanhita, 2023 [IPC Section 420] (Cheating & Dishonestly Inducing Delivery of Property)",
        "Section 319, Bharatiya Nyaya Sanhita, 2023 [IPC Section 419] (Cheating by Personation)"
    ]

    if any(w in t for w in ["otp", "pin", "cvv", "kyc", "password", "identity", "card number"]):
        sections.append("Section 66C, Information Technology Act, 2000 (Identity Theft & Electronic Credential Misuse)")

    if any(w in t for w in ["arrest", "police", "court", "threat", "disconnect", "penalty", "warrant", "cutoff", "jail", "blackmail"]):
        sections.append("Section 351, Bharatiya Nyaya Sanhita, 2023 [IPC Section 506] (Criminal Intimidation & Coercion)")

    if any(w in t for w in ["apk", "anydesk", "teamviewer", "remote access", "trojan", "malware", "virus"]):
        sections.append("Section 43 & Section 66, Information Technology Act, 2000 (Unauthorised Access & Computer Contaminant Injection)")

    if any(w in t for w in ["photo", "photos", "video", "explicit", "blackmail", "leak"]):
        sections.append("Section 67 & Section 67A, Information Technology Act, 2000 (Transmission of Sexually Explicit/Obscene Material)")

    return sections


def generate_gov_complaint_packet(
    content_text: str,
    channel: str = "voice",
    threat_type: str = "",
    risk_score: int = 0,
    threat_probability: int = 0,
    warning_signs: List[str] = None,
    filename: str = ""
) -> Dict[str, Any]:
    """
    Compiles an official, end-to-end cybercrime complaint packet structured
    specifically for direct submission on https://cybercrime.gov.in and Helpline 1930.
    """
    warning_signs = warning_signs or []
    identifiers = extract_identifiers(content_text)
    category, subcategory = map_ncrp_category(threat_type, content_text)
    sections = get_applicable_legal_sections(category, subcategory, content_text)

    channel_name = "Voice Call (VoIP / Cellular Audio)" if channel == "voice" else "SMS (Short Message Service)"
    phones = identifiers["phones"]
    urls = identifiers["urls"]
    headers = identifiers["headers"]
    upis = identifiers["upis"]
    impersonated = identifiers["impersonated"]

    phone_str = ", ".join(phones) if phones else ("Caller CLI Spoofed / Hidden VoIP Number" if channel == "voice" else "Direct Cellular Sender")
    header_str = ", ".join(headers) if headers else ("Not Applicable (Audio Stream)" if channel == "voice" else "Standard Header")
    url_str = ", ".join(urls) if urls else "None detected"
    upi_str = ", ".join(upis) if upis else "None detected"

    now_str = datetime.now().strftime("%d-%b-%Y %I:%M %p IST")
    if channel == "voice":
        evidence_list = [
            f"Original Call Audio Recording file ('{filename or 'call_recording.wav'}')",
            "Certified Audio-to-Text Transcript (Section 65B Indian Evidence Act compliant)",
            "Call Detail Record (CDR) / Mobile screenshot showing timestamp and caller number",
            "Bank transaction UTR / Debit SMS alerts (if any money was transferred)"
        ]
    else:
        evidence_list = [
            "Screenshot of original SMS / Message showing sender header and timestamp",
            "Full verbatim text content of the fraudulent message with exact links/codes",
            "Telecom operator sender detail screenshot",
            "Bank statement with UTR reference (if any unauthorized debit occurred)"
        ]

    # Pre-drafted complaint narrative ready for direct pasting into cybercrime.gov.in complaint box
    draft_lines = [
        "================================================================================",
        "FORMAL COMPLAINT UNDER SECTION 66D IT ACT & BNS FOR NATIONAL CYBER CRIME PORTAL",
        "Official Filing Reference: https://cybercrime.gov.in | Helpline 1930",
        "================================================================================",
        "",
        "TO: The Officer-in-Charge / Cyber Crime Investigation Cell",
        f"SUBJECT: Formal Complaint regarding Cyber Crime incident ({category} - {subcategory})",
        "",
        "1. INCIDENT & PORTAL CLASSIFICATION DETAILS:",
        f"• Primary Crime Category   : {category}",
        f"• Crime Sub-Category       : {subcategory}",
        f"• Medium / Channel         : {channel_name}",
        f"• Approximate Date & Time  : {now_str}",
        f"• Suspect Contact / CLI    : {phone_str}",
        f"• Suspect SMS Header       : {header_str}",
        f"• Suspect Phishing URL(s)  : {url_str}",
        f"• Suspect UPI / Account    : {upi_str}",
        f"• Impersonated Identity    : {impersonated}",
        "",
        "2. BRIEF FACTS OF THE COMPLAINT (MODUS OPERANDI):",
        f"I am submitting this formal complaint regarding a targeted cyber fraud / extortion attempt. "
        f"The suspect contacted me via {channel_name.lower()}, falsely posing as {impersonated}. "
        f"During this communication, the suspect made the following fraudulent statements and demands:\n"
        f'"{content_text.strip()}"\n\n'
        f"The suspect used deceptive social engineering, synthetic pressure, and urgent coercion to induce me into "
        f"revealing sensitive credentials, clicking phishing links, or transferring funds under false pretenses. "
        f"The caller/sender had no lawful authorization to demand such actions.",
        "",
        "3. FORENSIC AI VERIFICATION & THREAT EVALUATION:",
        f"• Forensic Risk Score      : {risk_score} / 100",
        f"• Threat Probability       : {threat_probability}%",
        f"• Forensic Classification  : {threat_type or subcategory}",
        f"• Key Threat Indicators    : {'; '.join(warning_signs[:3]) if warning_signs else 'High-pressure inducement and credential harvesting detected.'}",
        "",
        "4. APPLICABLE LEGAL PROVISIONS (IT ACT 2000 & BNS 2023):",
    ]
    for sec in sections:
        draft_lines.append(f"• {sec}")

    draft_lines.extend([
        "",
        "5. PRAYER / RELIEF SOUGHT FROM AUTHORITIES:",
        "It is respectfully requested that the Cyber Crime Police / National Cyber Crime Reporting Portal:",
        "a) Register this complaint and generate an official NCRP Acknowledgement Number / FIR.",
        "b) Coordinate with the Citizen Financial Cyber Fraud Reporting System (Helpline 1930) to freeze recipient mule accounts if any financial transaction took place.",
        "c) Direct telecom service providers and cybersecurity nodal officers to block and blacklist the suspect phone numbers, headers, and malicious domain endpoints.",
        "d) Take strict penal action against the perpetrators under Section 66D IT Act and relevant provisions of the Bharatiya Nyaya Sanhita.",
        "",
        "Complainant Evidence Pack Attached:",
    ])
    for ev in evidence_list:
        draft_lines.append(f"• [ATTACHMENT] {ev}")

    draft_text = "\n".join(draft_lines)

    return {
        "category": category,
        "subcategory": subcategory,
        "suspect_channel": channel_name,
        "suspect_phone": phone_str,
        "suspect_header": header_str,
        "suspect_urls": url_str,
        "suspect_upis": upi_str,
        "impersonated_entity": impersonated,
        "applicable_sections": sections,
        "evidence_checklist": evidence_list,
        "portal_draft_text": draft_text
    }
