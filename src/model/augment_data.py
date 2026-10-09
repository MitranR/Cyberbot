"""
Generates diverse synthetic scam + safe examples to augment training data.
This helps the ML model generalize to scam patterns not well-represented
in the original datasets.
"""
import random
import pandas as pd
from pathlib import Path

random.seed(42)

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "training data"

# ---------------------------------------------------------------------------
# Synthetic scam templates (filled with random details to avoid overfitting)
# ---------------------------------------------------------------------------

_COMPANIES_BANK = ["SBI", "HDFC", "ICICI", "Axis", "PNB", "Canara", "BOB", "Yes Bank", "Citibank", "HSBC"]
_COMPANIES_COURIER = ["DHL", "FedEx", "UPS", "Blue Dart", "DTDC", "EMS", "Aramex", "TNT"]
_COMPANIES_TECH = ["Microsoft", "Apple", "Dell", "Lenovo", "HP", "Google", "Amazon Web Services"]
_COMPANIES_UTILITY = ["Tata Power", "Adani Electricity", "BSES", "NTPC", "Power Grid", "MSEB", "CESC"]
_COMPANIES_JOB = ["Amazon", "Google", "Microsoft", "Flipkart", "TCS", "Infosys", "Wipro", "Accenture"]
_PLATFORMS = ["PayPal", "Google Pay", "PhonePe", "Amazon Pay", "Paytm", "Netflix", "Apple ID"]
_CURRENCIES = ["$", "£", "€", "₹"]
_URGENCY_PHRASES = [
    "URGENT", "ACT NOW", "Immediate action required", "Final notice",
    "expires today", "last chance", "24 hours", "respond immediately",
    "time sensitive", "act fast", "limited time"
]
_NAME_PREFIXES = ["Mr.", "Mrs.", "Ms.", "Dr.", "Prof."]
_FIRST_NAMES = ["James", "Sarah", "Michael", "Emma", "David", "Olivia", "John", "Sophia", "Robert", "Isabella"]
_LAST_NAMES = ["Johnson", "Williams", "Brown", "Taylor", "Wilson", "Davis", "Clark", "Lee", "Harris", "Martin"]
_DOMAINS = [
    "secure-verify.net", "account-update.com", "login-confirm.co",
    "verify-identity.org", "claim-prize.net", "track-delivery.info",
    "payment-portal.com", "refund-center.co", "support-help.org"
]
_CITIES = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]
_AMOUNTS_SMALL = ["499", "999", "1499", "1999", "2499", "2999", "350", "500"]
_AMOUNTS_LARGE = ["50000", "100000", "500000", "750000", "1000000", "2000000", "5000000", "25000000"]
_AMOUNTS_USD_LARGE = ["500,000", "1,000,000", "2,500,000", "5,000,000", "10,000,000", "25,000,000"]
_SALARIES = ["25000", "35000", "45000", "55000", "65000", "80000"]


def _phone():
    return f"+91-{random.randint(7000000000, 9999999999)}"


def _email():
    domain = random.choice(_DOMAINS).replace("www.", "")
    return f"{random.choice(['claims', 'support', 'admin', 'verify', 'help', 'info', 'service'])}@{domain}"


def _url():
    return f"https://{random.choice(_DOMAINS)}/{random.choice(['verify', 'claim', 'track', 'pay', 'update', 'confirm', 'login'])}-{random.randint(100,999)}"


def _generate_scams(count: int) -> list:
    """Generate diverse scam messages."""
    scams = []

    for _ in range(count):
        choice = random.randint(1, 10)

        if choice == 1:
            # Bank KYC / account scam
            bank = random.choice(_COMPANIES_BANK)
            company = random.choice(_COMPANIES_BANK)
            msg = random.choice([
                f"Dear Customer, your {bank} account has been temporarily blocked due to KYC non-compliance. Update immediately at {_url()} to restore access.",
                f"{random.choice(_URGENCY_PHRASES)}: Your {company} account has been suspended. Click {_url()} to verify your identity within 24 hours or your account will be permanently closed.",
                f"ALERT: Unauthorized login detected on your {bank} account from {random.choice(_CITIES)}. If this wasn't you, secure your account at {_url()} immediately.",
                f"Your {bank} debit card has been deactivated due to suspicious activity. Please re-activate at {_url()} or call {_phone()}.",
                f"Security alert: {bank} detected a login from an unknown device. Verify now at {_url()} or your account will be locked.",
                f"Your {bank} internet banking has been disabled. Please re-confirm your details at {_url()} to continue using online banking.",
            ])
            scams.append(msg)

        elif choice == 2:
            # Lottery / prize scam
            curr = random.choice(_CURRENCIES)
            amt = random.choice(_AMOUNTS_LARGE)
            msg = random.choice([
                f"CONGRATULATIONS!!! Your mobile number has won {curr}{amt} in the {random.choice(['UK', 'US', 'Canada', 'Australia', 'Spain', 'Dubai'])} {random.choice(['National Lottery', 'Mega Draw', 'Prize Promotion', 'Sweepstakes', 'Lucky Draw', 'Cash Giveaway'])}. To claim, send your personal details and bank info to {_email()}.",
                f"You have been selected as the winner of {curr}{amt} in our quarterly promotion. Call {_phone()} immediately to claim your prize. Reference: {random.randint(10000,99999)}.",
                f"{random.choice(_URGENCY_PHRASES)}: You've won {curr}{amt} in the {random.choice(['International', 'Annual', 'Monthly'])} {random.choice(['Lottery', 'Bonus Draw', 'Prize Award'])}. This is our final attempt to reach you. Contact {_email()} now.",
                f"Congratulations! You are our {random.choice(['1st', '2nd', '3rd'])} prize winner of {curr}{amt}. Funds are ready for transfer. Send your banking details to {_email()} for processing.",
            ])
            scams.append(msg)

        elif choice == 3:
            # Courier / customs / shipping scam
            courier = random.choice(_COMPANIES_COURIER)
            amt = random.choice(_AMOUNTS_SMALL)
            msg = random.choice([
                f"Your {courier} parcel is on hold due to unpaid customs duty of Rs.{amt}. Pay now at {_url()} to release your package. Delivery will be cancelled in 24 hours if unpaid.",
                f"{courier} tracking update: Your package could not be delivered due to incomplete address. Confirm details at {_url()} within 12 hours or item will be returned.",
                f"Customs Clearance Pending: Your international shipment via {courier} requires a clearance fee of {amt}. Make payment at {_url()} to avoid destruction of goods.",
                f"{courier}: Your parcel contains a restricted item and requires verification. Pay {amt} release fee at {_url()} or legal action may be taken.",
                f"Your {courier} shipment #{random.randint(1000000,9999999)} is being held by customs. Immediate payment of Rs.{amt} required at {_url()}.",
            ])
            scams.append(msg)

        elif choice == 4:
            # Tech support scam
            company = random.choice(_COMPANIES_TECH)
            msg = random.choice([
                f"This is {company} Support. We detected a virus on your system. Download AnyDesk or TeamViewer immediately and share your session ID so our technician can fix it remotely. Call {_phone()} now.",
                f"{company} Security Alert: Your computer has been infected with malware that is stealing your passwords. Visit {_url()} for immediate free scan and removal.",
                f"Warning: {company} has detected {random.randint(3,20)} threats on your device. Call our certified technicians at {_phone()} immediately before your data is compromised.",
                f"Your IP address was used in a cyber attack. Click {_url()} to install our security tool and prevent legal action against you.",
            ])
            scams.append(msg)

        elif choice == 5:
            # Job / recruitment scam
            company = random.choice(_COMPANIES_JOB)
            salary = random.choice(_SALARIES)
            msg = random.choice([
                f"We are hiring for remote {random.choice(['data entry', 'customer support', 'content writing', 'virtual assistant', 'transcription', 'proofreading'])} positions. {salary}/month. Pay a small {random.choice(['registration', 'processing', 'training', 'security deposit', 'onboarding'])} fee of Rs.{random.choice(['500', '1000', '1500', '2000', '2500'])} to secure your slot. Contact {_email()}.",
                f"Urgent hiring by {company}. Part-time work from home. Earn up to Rs.{random.choice(['30000', '40000', '50000', '60000'])} per month. Registration fee required. Call {_phone()} to apply now.",
                f"Your resume has been shortlisted by {company}. To proceed with the interview process, please pay a processing fee of {random.choice(['1999', '2499', '2999'])} to activate your offer letter. Reply for details.",
                f"Congratulations! You've been selected for a high-paying remote job. Receive {salary}/month working just {random.randint(2,4)} hours daily. Pay {random.choice(['199', '299', '499'])} for your ID card and training materials.",
            ])
            scams.append(msg)

        elif choice == 6:
            # Utility / bill scam
            company = random.choice(_COMPANIES_UTILITY)
            amt = random.choice(_AMOUNTS_SMALL)
            msg = random.choice([
                f"Your {company} electricity bill of Rs.{amt} has failed to process. Your power supply will be disconnected tonight. To avoid disconnection, make immediate payment at {_url()}.",
                f"FINAL DISCONNECTION NOTICE: {company} has not received your payment of Rs.{amt}. Your electricity will be cut within 24 hours. Pay instantly at {_url()} to restore service.",
                f"Your {company} account is in arrears of Rs.{amt}. Late payment penalty of Rs.{random.choice(['100', '200', '300', '500'])} will be added if not paid by today. Pay at {_url()}.",
                f"Refund Notice: You have an outstanding credit of Rs.{amt} from {company}. Claim your refund at {_url()} before it expires.",
                f"Your {company} bill payment failed. Your service will be disconnected tonight. Pay instantly via {random.choice(['UPI', 'net banking', 'credit card'])} at {_url()} to avoid disconnection.",
                f"Your utility payment of Rs.{amt} could not be processed. Your power connection will be terminated within 24 hours if not paid immediately.",
                f"Urgent: Your electricity supply will be cut off in 12 hours due to non-payment of Rs.{amt}. Avoid disconnection by paying at {_url()} now.",
            ])
            scams.append(msg)

        elif choice == 7:
            # Extended warranty scam
            msg = random.choice([
                f"We've been trying to reach you about your vehicle's extended warranty. Your coverage is about to expire. Respond YES to speak to an agent or call {_phone()} now.",
                f"Final notice: Your car warranty is expiring soon. Don't risk expensive repairs. Extend your coverage today at {_url()} before it's too late.",
                f"Our records show your {random.choice(['vehicle', 'appliance', 'electronic', 'home'])} warranty is expiring. Call {_phone()} immediately to renew and avoid paying full price for future repairs.",
                f"Important: Your extended warranty protection plan ends on {random.choice(['tomorrow', 'this week', 'in 3 days', 'in 7 days'])}. Renew now at {_url()} to stay covered.",
                f"Your vehicle's extended warranty is about to expire. Talk to an agent today to keep your coverage active. Call {_phone()}.",
            ])
            scams.append(msg)

        elif choice == 8:
            # Free gift / prize scam (not lottery, but "you won a free product")
            amt = random.choice(_AMOUNTS_SMALL)
            msg = random.choice([
                f"You've been selected to receive a FREE {random.choice(['iPhone 15', 'Samsung Galaxy S24', 'iPad Pro', 'MacBook Air', 'PlayStation 5', 'Nintendo Switch', 'AirPods Pro', 'Smart TV', 'Gift Card worth 5000'])}! Just pay {amt} shipping and handling. Claim at {_url()} before the offer expires.",
                f"Congratulations! You are our {random.randint(1,99999)}th visitor and have won a free {random.choice(['shopping voucher', 'luxury hamper', 'vacation package', 'smartphone', 'gadget bundle'])}. Verify at {_url()} within the next hour.",
                f"You have {random.randint(100,5000)} loyalty reward points expiring soon! Redeem for a free {random.choice(['gift card', 'smartwatch', 'bluetooth speaker', 'premium membership'])}. Small processing fee applies at {_url()}.",
                f"You've been selected for a free {random.choice(['iPhone 15', 'Samsung Galaxy S24', 'iPad Air', 'MacBook Pro', 'PlayStation 5', 'Nintendo Switch OLED', 'Apple Watch', '50 inch Smart TV', 'Gift Card worth 10000'])}! Just cover {random.choice(['shipping', 'processing', 'handling', 'delivery'])} of ${random.choice(['4.99', '5.99', '6.99', '9.99', '12.99', '14.99'])}. Click here before the offer expires.",
                f"Congratulations! You've been chosen for a complimentary {random.choice(['iPhone', 'tablet', 'laptop', 'smartwatch', 'gaming console', 'TV'])}. Only pay the {random.choice(['shipping fee', 'processing charge', 'handling cost', 'delivery charge'])} of {random.choice(['$4.99', '$5.99', '$9.99', 'Rs.499', 'Rs.999'])}.",
            ])
            scams.append(msg)

        elif choice == 9:
            # Emergency / money request scam (social engineering)
            name = f"{random.choice(_NAME_PREFIXES)} {random.choice(_FIRST_NAMES)} {random.choice(_LAST_NAMES)}"
            msg = random.choice([
                f"This is an emergency! I need {random.choice(['money', 'funds', 'cash', 'financial help'])} urgently. Please send {random.choice(['5000', '10000', '15000', '20000', '30000', '50000'])} via {random.choice(['UPI', 'bank transfer', 'Paytm', 'Google Pay'])} to my account. I'll explain later. This is a matter of life and death.",
                f"Hi, it's me. I lost my wallet and phone. I'm using a friend's phone. I need {random.choice(['5000', '8000', '10000', '15000'])} urgently for an emergency. Please send to this account number. I'll pay you back on Monday.",
                f"I'm stuck in {random.choice(_CITIES)} and need immediate financial assistance. Someone in my family is in the hospital. Please wire {random.choice(['10000', '20000', '25000', '50000'])} to this account. Will return by next week.",
                f"Please help! I'm in trouble and need {random.choice(['5000', '10000', '15000'])} right away. I promise to return it by {random.choice(['Monday', 'Friday', 'next week', 'the weekend'])}. Don't tell anyone about this.",
            ])
            scams.append(msg)

        elif choice == 10:
            # Account / subscription scam (Netflix, PayPal etc.)
            platform = random.choice(_PLATFORMS)
            amt = random.choice(_AMOUNTS_SMALL)
            msg = random.choice([
                f"Your {platform} account has been suspended due to payment failure of {amt}. Update your billing information at {_url()} to restore access immediately.",
                f"{platform} Security: We detected unusual activity on your account. Your account will be permanently suspended unless you verify your identity at {_url()}.",
                f"Billing Error: {platform} charged you {random.choice(['99', '149', '199', '499', '999'])} instead of {amt}. Claim your refund at {_url()} within 24 hours.",
                f"Your {platform} subscription has expired. To avoid losing access to your account, renew now at {_url()} for just {amt}/month.",
            ])
            scams.append(msg)

    return scams


def _generate_safe(count: int) -> list:
    """Generate diverse legitimate messages to balance the augmented data."""
    safe = []

    for _ in range(count):
        choice = random.randint(1, 15)

        if choice == 1:
            msgs = [f"Hey, are we still on for {random.choice(['lunch', 'dinner', 'coffee', 'drinks'])} tomorrow at {random.choice(['12pm', '1pm', '2pm', '7pm', '8pm'])}?"]
        elif choice == 2:
            msgs = [f"Your {random.choice(['Amazon', 'Flipkart', 'Myntra', 'Ajio'])} order #{random.randint(10000,99999)} has been shipped and will arrive on {random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])}{random.choice(['', '. Track your package on our website'])}."]
        elif choice == 3:
            msgs = [f"Reminder: Your {random.choice(['dentist', 'doctor', 'eye checkup', 'consultation'])} appointment is scheduled for {random.choice(['July', 'August', 'September'])} {random.randint(1,30)} at {random.choice(['9:00', '10:00', '10:30', '11:00', '14:00', '15:00', '16:00'])} {random.choice(['AM', 'PM'])}."]
        elif choice == 4:
            msgs = ["Mom, I'll be home late tonight, don't wait up for dinner."]
        elif choice == 5:
            msgs = [f"Team meeting moved to {random.choice(['2pm', '3pm', '4pm'])} today in {random.choice(['conference room B', 'the main hall', 'Boardroom A', 'Zoom'])}{random.choice(['', '. Please bring your reports'])}."]
        elif choice == 6:
            msgs = [f"Thank you for your payment of ${random.randint(10,200)}.{random.randint(0,99):02d}. Your {random.choice(['subscription', 'membership', 'plan', 'service'])} has been renewed."]
        elif choice == 7:
            msgs = [f"Can you send me the notes from {random.choice(['yesterday', 'today', 'Monday', "yesterday's"])} {random.choice(['lecture', 'class', 'meeting', 'session'])}{random.choice(['', '? I missed it'])}."]
        elif choice == 8:
            msgs = [f"Your OTP for {random.choice(['logging into', 'accessing', 'verifying'])} your {random.choice(['bank', 'email', 'account'])} is {random.randint(100000,999999)}. Do not share this with anyone."]
        elif choice == 9:
            msgs = [f"How was your {random.choice(['weekend', 'trip', 'vacation', 'day'])}? Let's catch up soon!"]
        elif choice == 10:
            msgs = [f"The {random.choice(['report', 'presentation', 'document', 'file'])} you requested is attached. Please review and let me know if you have any questions."]
        elif choice == 11:
            msgs = [f"Your {random.choice(['train', 'flight', 'bus', 'cab'])} is confirmed. {random.choice(['PNR', 'Booking', 'Ticket'])} #{random.randint(100000,999999)}. Departure at {random.randint(6,22)}:{random.choice(['00', '15', '30', '45'])}."]
        elif choice == 12:
            msgs = [f"Happy Birthday! Hope you have a wonderful day filled with joy and laughter!"]
        elif choice == 13:
            msgs = [f"Please find the {random.choice(['Q1', 'Q2', 'Q3', 'Q4', 'annual'])} {random.choice(['report', 'summary', 'results', 'analysis'])} attached for your review. Deadline for feedback is {random.choice(['Friday', 'Monday', 'next week'])}."]
        elif choice == 14:
            msgs = [f"Hi, just confirming our meeting at {random.randint(9,17)}:00. See you at the {random.choice(['office', 'cafe', 'lobby', 'reception'])}."]
        else:
            msgs = [f"Your {random.choice(['courier', 'package', 'parcel'])} has been delivered to your {random.choice(['office', 'home', 'neighbor', 'security desk'])}. Tracking: {random.choice(['', '#'])}{random.randint(1000000,9999999)}"]

        safe.extend(msgs)

    return safe


def generate_augmented_dataset(scam_count=25000, safe_count=25000):
    """
    Generate synthetic dataset and save as CSV for training.
    """
    print(f"Generating {scam_count} synthetic scam examples...")
    scams = _generate_scams(scam_count)
    print(f"  Generated {len(scams)} scam examples")

    print(f"Generating {safe_count} synthetic safe examples...")
    safe = _generate_safe(safe_count)
    print(f"  Generated {len(safe)} safe examples")

    df_scam = pd.DataFrame({"label": 1, "text": scams})
    df_safe = pd.DataFrame({"label": 0, "text": safe})
    df = pd.concat([df_scam, df_safe], ignore_index=True)

    output_path = OUTPUT_DIR / "synthetic_augmented.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} synthetic samples to {output_path}")
    return output_path


if __name__ == "__main__":
    generate_augmented_dataset()
