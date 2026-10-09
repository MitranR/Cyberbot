from src.agents.text_agent import TextScamDetectorAgent

agent = TextScamDetectorAgent()

MESSAGES = {
    "Safe": "Looks fine, nothing to worry about.",
    "Caution": "Bit suspicious — don't click anything or share your info until you're sure who this is from.",
    "High Alert": "Pretty sure this is a scam. Don't reply, don't tap any links. Check with the real company directly if you're unsure.",
    "Critical Threat": "This is definitely a scam. Block them now. If you already entered any details, call your bank immediately."
}

while True:
    text = input("\nEnter SMS text (or 'quit'): ")
    if text.lower() == 'quit':
        break
    r = agent.analyze(text)
    verdict = MESSAGES.get(r["threat_level"], "Unable to analyze.")
    print(f"\n[{r['threat_level']}] {r['scam_type']} ({r['risk_score']}/100)")
    print(verdict)
