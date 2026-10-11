"""
Comprehensive Multilingual Cybercrime Scenarios & Recovery Playbooks Knowledge Base.
Supports English, Tamil (தமிழ்), German (Deutsch), and Japanese (日本語).
Provides immediate first-response emergency checklists, technical remediation,
and prevention guidelines for all modern cyber fraud vectors.
"""

from typing import Dict, Optional


CYBER_SCENARIOS: Dict[str, Dict[str, str]] = {
    # 1. DIGITAL ARREST / POLICE IMPERSONATION
    "digital_arrest": {
        "Tamil": """🚨 **டிஜிட்டல் அரெஸ்ட் (Digital Arrest) அவசர பாதுகாப்பு வழிகாட்டி**

**எச்சரிக்கை:** இந்தியாவில் எந்தவொரு உண்மையான காவல் துறை, CBI, ED அல்லது சுங்கத்துறை (Customs) அதிகாரிகள் வீடியோ அழைப்பு மூலமாக எவரையும் கைது செய்யவோ அல்லது "டிஜிட்டல் விசாரணை" நடத்தவோ மாட்டார்கள்!

**உடனடி நடவடிக்கைகள்:**
1. **உடனடியாக அழைப்பை துண்டிக்கவும்:** ஸ்கைப், வாட்ஸ்அப் அல்லது வீடியோ அழைப்பை உடனடியாக கட் செய்யுங்கள். அவர்கள் காட்டும் போலி அடையாள அட்டை, கைது ஆணை (Arrest Warrant PDF) அனைத்தும் போலியானவை.
2. **ஒருபோதும் பணம் அனுப்பாதீர்கள்:** "வழக்கிலிருந்து விடுவிக்க வைப்புத்தொகை (Clearance Deposit) அனுப்புங்கள்" என்று கூறினால் அது 100% மோசடி.
3. **அச்சப்பட வேண்டாம்:** அவர்கள் உங்களை சிறையில் அடைப்பதாக பயமுறுத்தினாலும் தொடர்பை துண்டியுங்கள்.
4. **புகார் அளியுங்கள்:** உடனடியாக தேசிய சைபர் உதவி எண் **1930** அழைக்கவும் அல்லது **https://cybercrime.gov.in** இணையதளத்தில் புகார் பதிவு செய்யவும்.""",

        "German": """🚨 **Digital Arrest & Falsche Behördenanrufe Notfall-Leitfaden**

**Wichtiger Hinweis:** Echte Strafverfolgungsbehörden (Polizei, Interpol, Zoll, Justizbehörden) verhaften niemals Personen per Skype-, WhatsApp- oder Telefon-Videoanruf und fordern niemals Sicherheitsleistungen per Banküberweisung!

**Sofortmaßnahmen:**
1. **Verbindung sofort trennen:** Brechen Sie den Video- oder Sprachanruf umgehend ab. Gezeigte Dienstausweise und Haftbefehle sind Fälschungen.
2. **Keine Zahlungen leisten:** Überweisen Sie unter keinen Umständen angebliche "Kautionsbeträge" oder "Prüfkonten-Einzahlungen".
3. **Beweise sichern:** Erstellen Sie Screenshots der Anrufernummern und Dokumente.
4. **Vorfall melden:** Erstatten Sie sofort Anzeige bei der örtlichen Polizeidienststelle und melden Sie den Betrug unter Notruf 1930.""",

        "Japanese": """🚨 **警察・検察なりすまし（デジタル逮捕詐欺）緊急対処ガイド**

**重要事実:** 警察署、検察庁、裁判所がLINEやSkypeなどのビデオ通話で「逮捕状」を提示したり、資金の移動を命じることは100%あり得ません！

**直ちに行うべき3つの行動:**
1. **今すぐ通話を切断:** 脅迫的なビデオ通話や着信は即座に切ってください。画面内の警察手帳や令状はすべて画像加工された偽物です。
2. **絶対に送金しない:** 「身の潔白を証明するための預託金」や「保釈保証金」はすべて詐欺です。
3. **警察相談専用窓口に通報:** 直ちに警察相談ダイヤル（#9110 / 1930）または最寄りの警察署・交番に直接ご相談ください。""",

        "English": """🚨 **"Digital Arrest" Extortion Scam Emergency Playbook**

**Crucial Truth:** No authentic law enforcement agency (Police, CBI, ED, Narcotics Bureau, FBI, Interpol) has the legal authority to arrest, interrogate, or conduct "virtual court hearings" over Skype, WhatsApp, or video calls!

**Immediate Action Checklist:**
1. **Hang Up Immediately:** Terminate the video call. The badges, uniforms, court backgrounds, and arrest warrant PDFs are forged props.
2. **Never Transfer Funds:** Demands to move money to "government verification accounts" or "RBI security pools" are guaranteed theft.
3. **Preserve Evidence:** Take screenshots of the caller's phone numbers, chat messages, and fake letters.
4. **Emergency Escalation:** Dial National Cyber Crime Helpline **1930** immediately and register an official complaint at `https://cybercrime.gov.in`."""
    },

    # 2. AI VOICE CLONING / DEEPFAKE CALLS
    "voice_clone": {
        "Tamil": """🎙️ **AI குரல் குளோனிங் (Voice Cloning Scam) பாதுகாப்பு வழிகாட்டி**

**மோசடி முறை:** சைபர் குற்றவாளிகள் சமூக ஊடகங்களில் உள்ள சில வினாடிகள் ஆடியோவை பயன்படுத்தி உங்கள் மகன், மகள், பெற்றோர் அல்லது உறவினரின் குரலை அச்சு அசல் போல நகலெடுத்து அவசர பணம் கேட்கிறார்கள்.

**பாதுகாப்பு வழிமுறைகள்:**
1. **மாற்று வழியில் தொடர்பு கொள்ளுங்கள்:** அழைப்பை துண்டித்துவிட்டு, அந்த குடும்ப உறுப்பினரின் உண்மையான எண்ணுக்கு நீங்களே நேரடியாக அழைத்து சரிபார்க்கவும்.
2. **குடும்ப ரகசிய குறியீடு (Family Safe Word):** நெருங்கிய குடும்பத்தினருக்குள் ஒரு ரகசிய சொல்லை முன்கூட்டியே முடிவு செய்து வைத்துக்கொள்ளுங்கள்.
3. **அவசரப்படாதீர்கள்:** விபத்து அல்லது கைது என்று பயமுறுத்தினாலும் உணர்ச்சிவசப்பட்டு உடனே பணம் அனுப்பாதீர்கள்.
4. **குரல் அசாதாரணங்களை கவனியுங்கள்:** ரோபோ போன்ற சீரான சுருதி (pitch), செயற்கையான மூச்சு இடைவெளிகள் குரல் குளோனிங்கின் அறிகுறிகளாகும்.""",

        "German": """🎙️ **KI-Stimmenklonen & Enkeltrick 2.0 Schutzleitfaden**

**Modus Operandi:** Betrüger kopieren anhand weniger Sekunden Audiomaterial aus sozialen Medien die Stimmen von Angehörigen und täuschen angebliche Notlagen (Unfall, Verhaftung) vor.

**Schutz- und Sofortmaßnahmen:**
1. **Auflegen und Gegenanruf starten:** Beenden Sie das Telefonat und rufen Sie den Angehörigen selbst unter der gewohnten Handynummer an.
2. **Familien-Codewort nutzen:** Vereinbaren Sie ein geheimes Kennwort innerhalb der Familie für echte Notfälle.
3. **Keine Spontanüberweisungen:** Lassen Sie sich nicht unter emotionalen Druck setzen.
4. **Sprachmerkmale analysieren:** Achten Sie auf unnatürliche Pausen, monotone Tonhöhen oder Hintergrundrauschen.""",

        "Japanese": """🎙️ **AI音声合成・オレオレ詐欺2.0対策ガイド**

**手口の特徴:** SNS動画等から抽出したわずか数秒の音声データを基にAIで実子の声を模倣し、「事故を起こした」「至急示談金が必要」と現金を要求します。

**身を守る重要ルール:**
1. **一旦切って本人へ直接電話:** 指示された番号ではなく、必ず手元の電話帳に登録されている正規の番号に折り返してください。
2. **「家族の合言葉」の確認:** 緊急時には家族間でのみ共有している秘密の合言葉を確認してください。
3. **冷静さを保つ:** パニックを誘う演出に惑わされず、まずは送金を思いとどまってください。
4. **通報:** 不審な電話は直ちに警察相談専用電話（#9110 / 1930）へ相談してください。""",

        "English": """🎙️ **AI Voice Cloning & Deepfake Distress Call Defense**

**How It Works:** Scammers clone family members' voices using 3–5 seconds of public social media audio, staging panicked emergencies (kidnappings, car crashes, police custody) demanding urgent ransom or bail.

**Immediate Defense Protocol:**
1. **Hang Up & Call Back Directly:** Disconnect and dial your relative's known, saved phone number directly.
2. **Demand the Family Safe Word:** Use a pre-agreed passphrase known only to your immediate household.
3. **Ask an Idiosyncratic Question:** Ask about a private shared memory (e.g., "What was the name of our childhood pet?").
4. **Spot Acoustic Artifacts:** Listen for uncanny pitch flatness, robotic breath pacing, or metallic speech edges."""
    },

    # 3. BANK OTP, KYC & ELECTRICITY DISCONNECTION SCAMS
    "bank_otp": {
        "Tamil": """💳 **வங்கி OTP, KYC & மின்கட்டண மோசடி அவசர வழிகாட்டி**

**முக்கிய விதி:** வங்கி ஊழியர்கள் அல்லது மின்சார வாரிய அதிகாரிகள் எப்போதுமே OTP, PIN, அல்லது கடவுச்சொல்லை தொலைபேசி மூலம் கேட்க மாட்டார்கள்!

**உடனடி மீட்பு நடவடிக்கைகள்:**
1. **கார்டுகளை முடக்குங்கள் (Freeze Cards):** வங்கி மொபைல் ஆப் மூலம் கார்டுகளை OFF செய்யவும் அல்லது வங்கியின் 24x7 அவசர எண்ணை அழைத்து நெட் பேங்கிங், UPI முடக்கவும்.
2. **கடவுச்சொற்களை மாற்றவும்:** இணைய வங்கி மற்றும் UPI பின்னை உடனடியாக புதியதாக மாற்றவும்.
3. **கோல்டன் ஹவர் (Golden Hour 1930):** பண இழப்பு ஏற்பட்டால் முதல் 2 மணி நேரத்திற்குள் **1930** எண்ணை அழையுங்கள். இதனால் பணம் குற்றவாளியின் கணக்கிற்கு செல்லும் முன்பே முடக்கப்படும்.
4. **SMS/இணைப்புகளை புறக்கணிக்கவும்:** "இன்றிரவு மின்சாரம் துண்டிக்கப்படும்", "KYC புதுப்பிக்க இங்கே கிளிக் செய்க" என்ற SMS-களை ஒருபோதும் நம்பாதீர்கள்.""",

        "German": """💳 **Bankbetrug, TAN-Diebstahl & Phishing-SMS Notfallprotokoll**

**Grundsatz:** Keine Bank und kein Energieversorger verlangt jemals TANs, Passwörter oder PINs über SMS, E-Mail oder Telefonanrufe!

**Sofortmaßnahmen bei Kompromittierung:**
1. **Karten und Online-Banking sperren:** Rufen Sie unverzüglich den Sperr-Notruf (116 116 oder Ihre Hausbank) an.
2. **Zugangsdaten sofort ändern:** Ändern Sie Online-Banking-PINs von einem separaten, sicheren Endgerät aus.
3. **Transaktionen anfechten:** Melden Sie unautorisierte Abbuchungen binnen kürzester Frist zur Einleitung eines Chargebacks.
4. **Notruf 1930 / Polizei:** Erstatten Sie umgehend Anzeige wegen Cyberbetrugs.""",

        "Japanese": """💳 **銀行詐欺・不正送金・フィッシングSMS緊急対応マニュアル**

**鉄則:** 銀行や電力会社、公的機関が電話やSMSでワンタイムパスワード（OTP）や暗証番号の入力を求めることは絶対にありません！

**被害発生時の即時対応ステップ:**
1. **口座・クレジットカードの即時利用停止:** 銀行の紛失・盗難受付窓口へ電話し、ネットバンキングとカードの即時凍結を依頼してください。
2. **暗証番号・ログインパスワードの変更:** 感染していない別の安全な端末からログイン情報を変更してください。
3. **迅速な被害届:** 不正送金された資金を保全するため、直ちに全国共通サイバー相談窓口（1930 / 警察）へ通報してください。""",

        "English": """💳 **Banking Fraud, OTP Theft & Utility Disconnection Scams**

**Ironclad Rule:** No genuine bank, credit card company, or electricity board will ever solicit OTPs, CVVs, ATM PINs, or urgent app installations via call or SMS.

**First 60-Minute Recovery Protocol:**
1. **Kill Netbanking & Lock Cards:** Open your banking app to toggle card usage OFF, or dial your bank's 24x7 emergency hotline to freeze customer IDs and UPI handles.
2. **The Golden Hour (Call 1930):** Dial National Cyber Crime Helpline **1930** within 2–3 hours. The Citizen Financial Cyber Fraud Reporting system can freeze money in the fraudster's mule bank before cashout.
3. **Collect Transaction Evidence:** Gather the Bank UTR number, debit reference, recipient account/UPI ID, and debit SMS timestamp.
4. **File Complaint:** Submit full details at `https://cybercrime.gov.in` and present the acknowledgement slip to your branch manager."""
    },

    # 4. TELEGRAM PREPAID TASK & PART-TIME JOB FRAUD
    "telegram_job": {
        "Tamil": """💼 **டெலிகிராம் பார்ட் டைம் வேலை & டாஸ்க் மோசடி (Task Scam)**

**மோசடி உத்தி:** "வீட்டிலிருந்தே தினமும் ரூ.3000 சம்பாதிக்கலாம்", "யூடியூப் வீடியோக்களை லைக் செய்யுங்கள் அல்லது ஹோட்டல்களுக்கு ரேட்டிங் கொடுங்கள்" என்று கூறி தொடங்குவார்கள். ஆரம்பத்தில் ரூ.150–ரூ.500 தருவார்கள், பின்னர் "பிரீபெய்ட் விஐபி டாஸ்க்" என்று கூறி லட்சக்கணக்கில் பணத்தை பறிப்பார்கள்.

**பாதுகாப்பு வழிமுறைகள்:**
1. **கூடுதல் பணம் அனுப்பாதீர்கள்:** "உங்கள் லாபத்தை எடுக்க மேலும் 30% வரி செலுத்துங்கள்" என்று அவர்கள் கூறுவது முற்றிலும் பொய். எந்த தொகையையும் அனுப்ப வேண்டாம்.
2. **டெலிகிராம் குழுவிலிருந்து வெளியேறுங்கள்:** குழுவில் உள்ள மற்ற நபர்களும் மோசடி கும்பலை சேர்ந்த போலி கணக்குகளே.
3. **பரிவர்த்தனை விவரங்களை சேகரியுங்கள்:** பணம் அனுப்பிய UPI ஐடி, வங்கி கணக்கு எண்களை ஸ்கிரீன்ஷாட் எடுங்கள்.
4. **1930-ல் உடனே புகார் அளியுங்கள்:** உடனடியாக 1930 அல்லது cybercrime.gov.in-ல் நிதி மோசடி பிரிவில் புகார் பதிவு செய்யுங்கள்.""",

        "German": """💼 **Telegram-Nebenjob & Task-Scam Warnleitfaden**

**Masche:** Kriminelle versprechen hohe Tagesverdienste für einfache Aufgaben (YouTube-Videos liken, Hotelbewertungen abgeben). Nach anfänglichen Kleinstauszahlungen verlangen sie "Prepaid-Investitionen", deren Auszahlung anschließend gesperrt wird.

**Schutz- und Handlungsschritte:**
1. **Kein weiteres Geld einzahlen:** Zahlen Sie keinesfalls angebliche "Freischaltgebühren" oder "Steuern", um Ihr Guthaben zu retten.
2. **Kommunikation abbrechen:** Blockieren Sie die Telegram-Kontakte und sichern Sie den gesamten Chatverlauf als Beweismittel.
3. **Bank kontaktieren:** Informieren Sie Ihre Bank über die getätigten Überweisungen auf die Empfängerkonten.
4. **Cybercrime-Meldung:** Erstatten Sie umgehend Strafanzeige und rufen Sie die Cyber-Helpline 1930 an.""",

        "Japanese": """💼 **副業・「タスク型」Telegram投資詐欺対策**

**典型的な手口:** 「動画にいいねを押すだけ」「ホテルを評価するだけで日給数万円」と誘い、少額の報酬を支払って信用させた後、高額な「前払いタスク」や暗号資産投資に誘導して資金を持ち逃げします。

**直ちに対処すべき事項:**
1. **追加の入金を一切停止:** 「出金手数料」や「税金」を払えば出金できると言われても、絶対に振り込まないでください。
2. **証拠の保全:** やり取りしたチャット履歴、振込先口座番号、送金明細のスクリーンショットをすべて保存してください。
3. **サイバー相談窓口（1930 / 警察）へ届出:** 迅速に通報し、振込先口座の凍結要請を行ってください。""",

        "English": """💼 **Work-From-Home Telegram Task & "Like Video" Job Scam**

**The Anatomy of the Trap:** Scammers recruit via WhatsApp/Telegram offering ₹2,000–₹5,000/day for liking YouTube clips or reviewing hotels. They credit small payouts (₹150–₹500) to build trust, then trap victims in "Prepaid Crypto/VIP Tasks" where withdrawals are frozen unless further payments are made.

**Crucial Defense Rules:**
1. **Stop Paying Immediately:** Demands to pay "clearance fees", "credit score upgrade", or "withdrawal taxes" are 100% fictional. You will NEVER get money back by paying more.
2. **All Group Members Are Shills:** Everyone cheering their payouts in that Telegram group is an actor or fake bot account.
3. **Gather Audit Evidence:** Save transaction IDs, recipient UPI handles, bank account numbers, and Telegram usernames.
4. **File Emergency 1930 Ticket:** Dial **1930** instantly and submit bank evidence on `https://cybercrime.gov.in`."""
    },

    # 5. SEXTORTION, VIDEO CALL BLACKMAIL & LOAN APPS
    "sextortion": {
        "Tamil": """🔞 **செக்ஸ்டார்ஷன் (Sextortion) & வீடியோ கால் மிரட்டல் பாதுகாப்பு**

**மோசடி முறை:** தெரியாத எண்ணிலிருந்து கவர்ச்சியான பெண் வீடியோ கால் செய்வார். அழைப்பை ஏற்றதும் உங்கள் முகத்தையும் ஒரு ஆபாச வீடியோவையும் ஒன்றாக பதிவு செய்து, "பணம் தராவிட்டால் இந்த வீடியோவை குடும்பத்தினர் மற்றும் நண்பர்களுக்கு அனுப்புவேன்" என்று மிரட்டுவார்கள்.

**உடனடி நடவடிக்கைகள்:**
1. **ஒரு ரூபாய் கூட கொடுக்காதீர்கள்:** ஒருமுறை பணம் கொடுத்தால், அவர்கள் மீண்டும் மீண்டும் மேலும் அதிக பணம் கேட்டு மிரட்டுவார்கள்.
2. **அச்சப்பட வேண்டாம் - தற்கொலை எண்ணங்களை தவிருங்கள்:** இது ஒரு சர்வதேச சைபர் கும்பலின் திட்டமிட்ட செயல். நீங்கள் குற்றவாளி அல்ல, பாதிக்கப்பட்டவர்.
3. **அழைப்பாளரை பிளாக் செய்யுங்கள்:** உடனடியாக வாட்ஸ்அப் அல்லது அந்த எண்ணை பிளாக் செய்து ரிப்போர்ட் செய்யவும்.
4. **சமூக ஊடகங்களை லாக் செய்யுங்கள்:** இன்ஸ்டாகிராம்/பேஸ்புக் கணக்குகளை பிரைவேட் (Private) ஆக்கி, தொடர்புகள் பட்டியலை மறைக்கவும்.
5. **தேசிய உதவி எண் 1930:** சைபர் குற்றப்பிரிவில் புகார் பதிவு செய்யுங்கள். வீடியோ பரவாமல் தடுக்க காவல்துறை நடவடிக்கை எடுக்கும்.""",

        "German": """🔞 **Sextortion & Erpressung per Videoanruf Schutzprotokoll**

**Tathergang:** Betrüger initiieren Videoanrufe mit intimen Darstellungen, schneiden das Gesicht des Opfers hinein und drohen mit Veröffentlichung im Freundes- und Kollegenkreis, falls kein Geld gezahlt wird.

**Krisenintervention:**
1. **Kein Geld überweisen:** Eine Zahlung stoppt die Erpressung niemals – sie führt lediglich zu höheren Folgeforderungen.
2. **Kontakt rigoros abbrechen:** Blockieren und melden Sie den Erpresser auf allen Kanälen.
3. **Profile auf privat schalten:** Schützen Sie Ihre Social-Media-Accounts (Freundeslisten verbergen).
4. **Beweise sichern:** Dokumentieren Sie Chatverläufe und Rufnummern per Screenshot.
5. **Anzeige erstatten:** Wenden Sie sich umgehend an die Polizei oder Notruf 1930.""",

        "Japanese": """🔞 **セクストーション（性的脅迫・ビデオ通話恐喝）緊急対策**

**手口:** 見知らぬ相手からビデオ通話がかかり、被害者の顔とわいせつ映像を合成録画した上で「金を払わなければSNSの知人に拡散する」と脅迫します。

**絶対に守るべき5つの対応:**
1. **絶対に要求に応じない・送金しない:** 一度でも支払うと、さらに高額な要求が際限なく続きます。
2. **相手を即座にブロック:** 連絡を完全に断ち切ってください。
3. **SNSの非公開設定:** フォロワーリストや連絡先を見られないよう、アカウントを「非公開」に設定してください。
4. **証拠保存:** 脅迫メッセージのスクリーンショットを保存してください。
5. **相談・通報:** 警察相談専用電話（#9110 / 1930）または最寄りの警察署へ速やかにご相談ください。""",

        "English": """🔞 **Sextortion & Video Call Blackmail Emergency Protocol**

**The Trap:** A scammer initiates an unsolicited video call (often featuring pre-recorded explicit video), screen-records your shocked face, and instantly threatens to blast the spliced video to your contact list or workplace unless you pay.

**Life-Saving Rules:**
1. **DO NOT PAY A SINGLE CENT:** Paying guarantees repeated and escalating extortion demands. They never delete the video upon payment.
2. **Understand You Are the Victim:** This is an automated syndicate targeting thousands daily. Do not panic or harm yourself.
3. **Block & Report Immediately:** Block the blackmailer on WhatsApp/Instagram without negotiating.
4. **Lock Down Social Profiles:** Set your Instagram, Facebook, and LinkedIn profiles to maximum privacy (hide followers and friends list).
5. **Emergency Support:** Dial National Cyber Crime Helpline **1930** and report the extortion. Law enforcement has direct mechanisms with Meta and Google to suppress compromised media."""
    },

    # 6. SIM SWAP & ESIM HIJACKING
    "sim_swap": {
        "Tamil": """📱 **சிம் ஸ்வாப் (SIM Swap) மோசடி பாதுகாப்பு வழிகாட்டி**

**அறிகுறி:** உங்கள் மொபைல் போனில் திடீரென நெட்வொர்க் சிக்னல் முற்றிலுமாக நின்றுவிடும் ("No Service" அல்லது "Emergency Calls Only").

**காரணம்:** குற்றவாளி உங்கள் போலி ஆவணங்களை கொண்டு தொலைத்தொடர்பு நிறுவனத்திடம் இருந்து உங்கள் எண்ணுக்கு மாற்று சிம் கார்டை பெற்றுள்ளார். இதன் மூலம் உங்கள் வங்கி OTP-களை திருடுகிறார்.

**உடனடி நடவடிக்கைகள்:**
1. **தொலைத்தொடர்பு நிறுவனத்தை அழையுங்கள்:** வேறு ஒரு போன் மூலம் உங்கள் நெட்வொர்க் நிறுவனத்தின் வாடிக்கையாளர் மையத்தை (Airtel/Jio/Vi) உடனடியாக அழைத்து உங்கள் சிம்மை தற்காலிகமாக முடக்குங்கள்.
2. **வங்கி கணக்குகளை முடக்குங்கள்:** உடனடியாக வங்கி அவசர எண்ணை அழைத்து நெட் பேங்கிங்கை பிளாக் செய்யுங்கள்.
3. **வங்கி மற்றும் 1930-ல் புகார்:** சிம் ஸ்வாப் மூலம் பண இழப்பு நேர்ந்தால் உடனே 1930-ல் புகார் பதிவு செய்யவும்.""",

        "German": """📱 **SIM-Swapping & eSIM-Hijacking Notfallleitfaden**

**Warnsignal:** Ihr Mobiltelefon verliert plötzlich jegliches Mobilfunksignal ("Kein Netz / Nur Notrufe"), obwohl kein technischer Ausfall vorliegt.

**Hintergrund:** Angreifer erschleichen sich beim Mobilfunkbetreiber eine Ersatz-SIM auf Ihre Rufnummer, um SMS-TANs für Online-Banking abzufangen.

**Sofortmaßnahmen:**
1. **Mobilfunkbetreiber sofort kontaktieren:** Sperren Sie Ihre SIM-Karte umgehend über die Kundenhotline Ihres Mobilfunkanbieters.
2. **Online-Banking sperren:** Lassen Sie alle Bankzugänge über den Sperr-Notruf (116 116 / 1930) blockieren.
3. **Umstellung auf App-basierte 2FA:** Ersetzen Sie SMS-Verfahren künftig durch Authenticator-Apps (z. B. Aegis, Google Authenticator).""",

        "Japanese": """📱 **SIMスワップ（SIM乗っ取り・eSIM不正再発行）緊急対策**

**危険な兆候:** スマートフォンが突然「圏外」または「緊急通報のみ」となり、再起動しても電波を掴まない場合、第三者にSIMカードを不正再発行された可能性があります。

**直ちに行うべき対応:**
1. **携帯通信会社へ緊急連絡:** 別の電話等から契約携帯キャリアのサポートへ連絡し、回線を即時停止してください。
2. **金融機関のネットバンキング凍結:** SMS認証を悪用される前に、利用金融機関の口座を停止してください。
3. **認証手段の変更:** SMS認証からアプリ認証（Google Authenticator等）へ切り替えてください。
4. **通報:** 不正アクセス被害として警察（#9110 / 1930）へ相談してください。""",

        "English": """📱 **SIM Swap & eSIM Takeover Emergency Guide**

**The Dead Giveaway:** Your smartphone abruptly drops from 5G/4G to "No Service" or "Emergency Calls Only", and Wi-Fi continues functioning normally.

**The Threat:** Scammers impersonated you with forged identity papers at a carrier store to transfer your phone number to a duplicate physical SIM or eSIM, enabling them to hijack SMS OTPs.

**Action Steps in the First 15 Minutes:**
1. **Call Your Mobile Carrier Instantly:** From another phone, call customer service (Jio/Airtel/Vodafone/carrier) and request an immediate hard block on the hijacked SIM.
2. **Notify Your Bank to Freeze OTP Services:** Dial your bank's fraud line and freeze UPI handles and phone-based authentication.
3. **Check Primary Email Sessions:** Inspect your Google/Apple account security settings for unauthorized logins and revoke them.
4. **Dial 1930:** Report the SIM swap immediately to register a cyber police record."""
    },

    # 7. PHISHING, FAKE FEDEX/DHL CUSTOMS PARCEL
    "phishing": {
        "Tamil": """📦 **போலி கூரியர் (FedEx/DHL) & பார்சல் சுங்கவரி மோசடி**

**மோசடி அழைப்பு:** "FedEx / Speed Post-லிருந்து பேசுகிறோம். தைவான் அல்லது கம்போடியாவிற்கு உங்கள் பெயரில் அனுப்பப்பட்ட பார்சலில் 140 கிராம் போதைப்பொருள் மற்றும் போலி பாஸ்போர்ட் சிக்கியுள்ளது" என்று கூறுவார்கள்.

**உண்மைகள்:**
1. பார்சலில் சட்டவிரோத பொருட்கள் இருந்தால் உண்மையான சுங்கத்துறை உங்கள் வீட்டிற்கு அதிகாரப்பூர்வ நோட்டீஸ் அனுப்பும்; தொலைபேசியில் வீடியோ கால் செய்யாது.
2. "காவல்துறைக்கு வழக்கை மாற்றுகிறோம்" என்று கூறி அவர்களின் கூட்டாளியிடமே இணைப்பார்கள்.
3. எந்த இணைப்பையும் (link) கிளிக் செய்யாதீர்கள், எந்த பணமும் செலுத்தாதீர்கள்.
4. அதிகாரப்பூர்வ கூரியர் நிறுவன இணையதளத்தில் உண்மையான டிராக்கிங் எண்ணை மட்டுமே சரிபார்க்கவும்.""",

        "German": """📦 **Paket-Phishing, Zollbetrug & Fake-Kuriernachrichten**

**Masche:** SMS oder Anrufe behaupten, ein Paket (DHL, FedEx) werde beim Zoll zurückgehalten (angebliche Schmuggelware oder offene Zollgebühren von wenigen Euro).

**Schutzregeln:**
1. **Niemals auf SMS-Links klicken:** Prüfen Sie Sendungsnummern ausschließlich direkt auf der offiziellen Website des jeweiligen Dienstleisters.
2. **Keine Gebühren über inoffizielle Links zahlen:** Behörden oder Paketdienste versenden keine Zahlungsaufforderungen über verkürzte URLs (bit.ly, tinyurl).
3. **Ignorieren und Nummer sperren:** Blockieren Sie verdächtige Absender.""",

        "Japanese": """📦 **宅配便不在通知・税関偽装フィッシング詐欺**

**手口:** 「FedExや税関です。あなた宛ての荷物から違法薬物が見つかりました」「不在のため荷物を保管中。確認はリンクから」といったSMSや偽着信で個人情報や金銭を騙し取ります。

**対策方針:**
1. **SMS内のリンクは開かない:** 荷物の配送状況は、公式サイトや公式アプリから直接追跡番号を入力して確認してください。
2. **クレジットカード情報の入力厳禁:** 再配達料などの名目でカード情報を入力しないでください。
3. **税関を名乗る脅迫電話は即切断:** 警察や税関を騙る不審電話はすぐに切り、警察窓口（#9110 / 1930）へご相談ください。""",

        "English": """📦 **Phishing, FedEx/DHL Customs Hold & Narcotics Parcel Scam**

**The Narrative:** Scammers call claiming: "A courier parcel sent in your Aadhaar/name to Cambodia has been intercepted with 150g MDMA and 5 fake passports." They threaten immediate transfer to Mumbai Cyber Police.

**Reality & Defense Protocol:**
1. **Courier Companies Do Not Police Contraband by Phone:** If contraband is seized, customs issues physical summons under CrPC. They NEVER connect you to a "police officer on Skype".
2. **Never Pay "Customs Inspection Fees":** Any demand for money transfer to clear your name is fraudulent.
3. **Verify Directly:** If you have an actual shipment, track it solely on the official carrier portal (`fedex.com` or `indiapost.gov.in`).
4. **Report Scam Numbers:** Report the scam caller on the Chakshu portal and dial **1930**."""
    },

    # 8. MALICIOUS APKS & SCREEN SHARE (ANYDESK / TEAMVIEWER)
    "malware_apk": {
        "Tamil": """📲 **போலி APK செயலிகள் & ஸ்கிரீன் ஷேர் (AnyDesk) மோசடி பாதுகாப்பு**

**மோசடி உத்தி:** "மின்கட்டணம் செலுத்த", "வங்கி KYC அப்டேட் செய்ய" அல்லது "வாடிக்கையாளர் சேவைக்காக" வாட்ஸ்அப்பில் ஒரு .apk கோப்பை அனுப்புவார்கள் அல்லது AnyDesk / TeamViewer / QuickSupport செயலியை பதிவிறக்க சொல்வார்கள்.

**உடனடி மீட்பு நடவடிக்கைகள்:**
1. **இணையத்தை துண்டிக்கவும்:** உடனே வைஃபை மற்றும் மொபைல் டேட்டாவை அணைக்கவும் (Airplane Mode).
2. **மோசடி செயலியை நீக்கவும்:** பதிவிறக்கிய .apk அல்லது AnyDesk செயலியை உடனடியாக அன்-இன்ஸ்டால் (Uninstall) செய்யுங்கள்.
3. **போனை பேக்டரி ரீசெட் (Factory Reset) செய்யவும்:** தேவைப்பட்டால் முக்கியமான தரவுகளை பேக்கப் எடுத்துவிட்டு போனை ரீசெட் செய்வது மிக பாதுகாப்பானது.
4. **வங்கி கடவுச்சொற்களை மாற்றவும்:** மற்றொரு பாதுகாப்பான சாதனத்திலிருந்து உங்கள் வங்கி மற்றும் இமெயில் கடவுச்சொற்களை மாற்றவும்.""",

        "German": """📲 **Schad-APKs & Fernsteuerungs-Betrug (AnyDesk / TeamViewer)**

**Gefahr:** Betrüger fordern Sie auf, angebliche Support-Apps (.apk-Dateien) oder Fernwartungssoftware (AnyDesk, TeamViewer) zu installieren, um Ihr Smartphone oder Online-Banking fernzusteuern.

**Sofortige Schutzmaßnahmen:**
1. **Sofort offline gehen:** Flugmodus aktivieren oder WLAN/Mobilfunk unverzüglich trennen.
2. **App deinstallieren:** Entfernen Sie die verdächtige App und entziehen Sie ihr in den Telefoneinstellungen alle Bedienungshilfen- und Administratorrechte.
3. **Werkseinstellungen:** Setzen Sie das Smartphone im Zweifelsfall auf die Werkseinstellungen zurück.
4. **Passwörter ändern:** Ändern Sie von einem sicheren Zweitgerät aus alle Zugangsdaten.""",

        "Japanese": """📲 **不正APK・遠隔操作アプリ（AnyDesk等）詐欺対策**

**危険性:** サポートを装い、画面共有アプリ（AnyDesk、TeamViewer、QuickSupport）や非公式アプリ（.apk）をインストールさせ、遠隔操作でネットバンキングを操作して不正送金します。

**緊急復旧ステップ:**
1. **即座に通信を切断:** 機内モードをONにし、Wi-Fiとモバイル通信を完全に遮断してください。
2. **遠隔操作アプリのアンインストール:** 当該アプリを直ちに削除してください。
3. **端末の初期化:** 不正アプリが深く常駐している可能性があるため、端末の初期化（工場出荷状態）を強く推奨します。
4. **安全な別端末からパスワード変更:** 金融機関や主要サービスのパスワードをすべて更新してください。""",

        "English": """📲 **Malicious APKs & Screen-Sharing Trojans (AnyDesk / TeamViewer)**

**The Danger:** Attackers urge you to install a custom `.apk` (disguised as "ElectricityBillUpdate.apk" or "BankSupport.apk") or legitimate remote access tools (AnyDesk, TeamViewer, QuickSupport, RustDesk) granting full device takeover.

**Immediate Containment Protocol:**
1. **Turn ON Airplane Mode:** Immediately kill Wi-Fi and mobile data to cut the attacker's active command-and-control connection.
2. **Revoke Accessibility Permissions & Uninstall:** Go to `Settings -> Apps -> Special App Access -> Device Admin / Accessibility` and uninstall the suspicious app.
3. **Perform a Factory Reset:** If an unauthorized APK requested SMS reading and notification listener permissions, back up photos and perform a clean factory reset.
4. **Change Netbanking Passwords via Clean Device:** Never change passwords on the infected phone until it has been sanitized."""
    },

    # 9. HACKED ACCOUNT RECOVERY (INSTAGRAM, WHATSAPP, GMAIL)
    "hacked_account": {
        "Tamil": """🔓 **ஹேக் செய்யப்பட்ட கணக்குகளை (Instagram, WhatsApp, Gmail) மீட்பது எப்படி?**

**1. வாட்ஸ்அப் மீட்க:**
• வாட்ஸ்அப்பை மீண்டும் இன்ஸ்டால் செய்து உங்கள் தொலைபேசி எண்ணை பதிவு செய்யுங்கள்.
• SMS மூலம் வரும் 6 இலக்க குறியீட்டை உள்ளிடவும். ஹேக்கர் பயன்படுத்திய கணக்கு தானாக வெளியேறிவிடும்.
• உடனே "Two-step verification" பின்னை அமைக்கவும்.

**2. இன்ஸ்டாகிராம் மீட்க:**
• உள்நுழைவு பக்கத்தில் "Forgot password?" -> "Need more help?" கிளிக் செய்யவும்.
• செல்ஃபி வீடியோ சரிபார்ப்பு (Video Selfie verification) மூலம் உங்கள் கணக்கை மீட்டெடுக்கலாம்.

**3. கூகுள் / ஜிமெயில் மீட்க:**
• `https://accounts.google.com/signin/recovery` பக்கத்திற்கு சென்று மீட்பு இமெயில்/எண் மூலம் சரிபார்க்கவும்.
• அங்கீகரிக்கப்படாத சாதனங்களை "Manage Devices"-ல் இருந்து Logout செய்யவும்.""",

        "German": """🔓 **Wiederherstellung kompromittierter Konten (WhatsApp, Instagram, Google)**

**1. WhatsApp zurückholen:**
• Installieren Sie WhatsApp neu und verifizieren Sie Ihre Handynummer per SMS. Der Angreifer wird automatisch abgemeldet.
• Aktivieren Sie sofort die Verifizierung in zwei Schritten (PIN).

**2. Instagram wiederherstellen:**
• Wählen Sie "Passwort vergessen?" -> "Weitere Hilfe benötigt?".
• Nutzen Sie die Selfie-Video-Verifizierung zur Identitätsbestätigung.

**3. Google / E-Mail retten:**
• Rufen Sie `https://accounts.google.com/signin/recovery` auf.
• Beenden Sie unter "Geräte verwalten" alle verdächtigen aktiven Sitzungen und erneuern Sie 2FA.""",

        "Japanese": """🔓 **乗っ取りアカウント（LINE・Instagram・Google）復旧手順**

**1. LINE / WhatsAppの復旧:**
• アプリを再インストールし、正規の電話番号でSMS認証を行ってください（攻撃者側の端末から自動ログアウトされます）。
• 2段階認証PINコードを直ちに設定してください。

**2. Instagramの復旧:**
• ログイン画面で「パスワードをお忘れですか？」→「サポートが必要な場合」を選択。
• ビデオ自撮り認証（セルフィー動画）により本人確認を行って復旧を申請してください。

**3. Google / 各種メールアカウント:**
• `https://accounts.google.com/signin/recovery` から復旧手続きを行ってください。
• セキュリティ設定から「すべてのデバイスからログアウト」を実行してください。""",

        "English": """🔓 **Compromised Account Recovery (WhatsApp, Instagram, Google)**

**1. Recovering Hijacked WhatsApp:**
- Re-install WhatsApp, input your phone number, and enter the 6-digit SMS verification code. This automatically evicts the fraudster from active sessions.
- Immediately enable Two-Step Verification with a private 6-digit PIN.

**2. Recovering Hacked Instagram:**
- Tap "Forgot Password?" -> "Need more help?". Select "My account was hacked".
- If photos of you exist on the profile, use Instagram's **Video Selfie Verification** to regain control within 24–48 hours.

**3. Securing Google / Gmail:**
- Navigate to `https://accounts.google.com/signin/recovery`.
- Go to `Security -> Your Devices -> Manage all devices` and click "Sign out" on all unknown locations."""
    },

    # 10. NATIONAL REPORTING 1930 & CYBERCRIME.GOV.IN
    "reporting_1930": {
        "Tamil": """🚨 **தேசிய சைபர் உதவி எண் 1930 & புகார் அளிக்கும் முழுமையான வழிகாட்டி**

**1930 என்றால் என்ன?**
மத்திய உள்துறை அமைச்சகத்தின் கீழ் செயல்படும் Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS) உதவி எண் ஆகும்.

**கோல்டன் ஹவர் (Golden Hour) விதி:**
பண இழப்பு ஏற்பட்ட **முதல் 2 முதல் 3 மணி நேரத்திற்குள்** 1930 எண்ணை அழைத்தால், மோசடி கும்பல் பணத்தை ஏடிஎம்மில் எடுப்பதற்கு முன்பே வங்கிகளால் அந்த பணம் முடக்கப்படும் (Freeze) வாய்ப்பு மிக அதிகம்!

**தேவையான தகவல்கள்:**
1. உங்கள் வங்கி பெயர் மற்றும் கணக்கு எண்
2. பரிவர்த்தனை அடையாள எண் (UTR எண் / Transaction ID)
3. பரிவர்த்தனை நடந்த நேரம் மற்றும் தேதி
4. மோசடி செய்பவரின் வங்கி கணக்கு அல்லது UPI ஐடி
5. உங்கள் வங்கிக்கு வந்த பணப் பரிவர்த்தனை SMS

**ஆன்லைன் போர்ட்டல்:**
அழைப்புக்கு பிறகு **https://cybercrime.gov.in** இணையதளத்தில் முழு விவரங்களுடன் புகாரை சமர்ப்பித்து ஒப்புகை சீட்டை (Acknowledgement Slip) பதிவிறக்குங்கள்.""",

        "German": """🚨 **Notfall-Leitfaden: Anzeige erstatten & Notruf 1930**

**Die "Golden Hour" Regel:**
Wenden Sie sich innerhalb der ersten 2–3 Stunden nach einer unbefugten Abbuchung an Ihre Bank und die Cybercrime-Meldestelle (Notruf 1930). In diesem Zeitfenster können Finanztransfers noch auf den Zwischenkonten der Betrüger gestoppt werden.

**Notwendige Angaben für die Strafanzeige:**
1. Name der Bank und Kontonummer des Opfers
2. Transaktionsreferenz (UTR-Nummer / Überweisungs-ID)
3. Exakter Zeitstempel der Belastung
4. Empfängerkontonummer oder UPI-ID des Betrügers
5. Screenshots aller Chatverläufe und Bestätigungs-SMS

**Online-Portal:**
Vollständige Anzeige online unter `https://cybercrime.gov.in` einreichen und die Aktenzeichen-Quittung für Ihre Hausbank ausdrucken.""",

        "Japanese": """🚨 **サイバー犯罪通報ガイド（1930番窓口・被害届提出手順）**

**「ゴールデンアワー（黄金の2時間）」の重要性:**
不正送金発生から2〜3時間以内に通報することで、犯罪グループが資金を引き出す前に中継口座を凍結できる可能性が大幅に高まります。

**通報・相談時に必要な情報:**
1. 被害に遭った銀行口座番号および支店名
2. 取引照会番号（送金受付番号・トランザクションID）
3. 不正送金が行われた正確な日時
4. 振込先の口座情報または送金先識別番号
5. 被害通知SMSやチャット履歴の証拠

**公式通報窓口:**
オンライン相談は `https://cybercrime.gov.in` または警察相談ダイヤル（#9110 / 1930）へ速やかに届け出てください。""",

        "English": """🚨 **National Cybercrime Helpline 1930 & Portal Playbook**

**What is 1930?**
The National Cyber Crime Reporting Helpline operated by the Ministry of Home Affairs (I4C). It connects 250+ banks, wallets, and telecom providers through the Citizen Financial Cyber Fraud Reporting System.

**The Golden Hour Protocol (First 2–3 Hours):**
Reporting within this critical window empowers cyber officers to issue automated API freeze requests directly to beneficiary mule accounts before money is laundered into crypto or cash withdrawals.

**Mandatory Dossier Checklist:**
1. **Victim Account Details:** Bank name, account number, debit card/UPI handle.
2. **Transaction Fingerprints:** UTR / RRN number, exact transaction amount and timestamp.
3. **Perpetrator Coordinates:** Recipient account number, IFSC code, or UPI VPA.
4. **SMS & Call Artifacts:** Full screenshot of debit notifications and sender IDs.

**Next Step:** Register your detailed narrative on `https://cybercrime.gov.in` and present the NCRP acknowledgement slip to your home branch."""
    }
}


def get_scenario_response(topic: str, language: str = "English") -> Optional[str]:
    """Retrieves localized scenario guidance for a matched cybercrime vector."""
    if topic in CYBER_SCENARIOS:
        scenario_data = CYBER_SCENARIOS[topic]
        return scenario_data.get(language, scenario_data.get("English"))
    return None
