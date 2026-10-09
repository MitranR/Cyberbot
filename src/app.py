import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import json
import time

# Page config
st.set_page_config(
    page_title="Cyber Fraud Shield AI Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich cybersecurity aesthetics, glassmorphism, dark theme & dynamic visual badges
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Container */
    .cyber-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    .cyber-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    .cyber-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 6px;
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    /* Threat Badges */
    .badge-safe {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid #10b981;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
    }
    .badge-caution {
        background-color: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid #f59e0b;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
    }
    .badge-high {
        background-color: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid #ef4444;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
    }
    .badge-critical {
        background-color: rgba(225, 29, 72, 0.25);
        color: #f43f5e;
        border: 2px solid #f43f5e;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 800;
        animation: pulse 1.8s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(244, 63, 94, 0); }
        100% { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0); }
    }
    
    /* Stat Metric Box */
    .metric-box {
        background: #1e293b;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        border: 1px solid #334155;
    }
    
    .metric-val {
        font-size: 2rem;
        font-weight: 800;
        color: #38bdf8;
    }
    
    .metric-lbl {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Code / Guide highlight */
    .guide-box {
        background: #0f172a;
        border-left: 4px solid #38bdf8;
        padding: 16px;
        border-radius: 0 8px 8px 0;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)

# Imports after page config
from src.config import Config, EMERGENCY_PLAYBOOKS
from src.agents.orchestrator import FreeAgentOrchestrator
from src.database.db_manager import DatabaseManager

# Initialize Database & Orchestrator in session state
if "db" not in st.session_state:
    st.session_state.db = DatabaseManager()

db = st.session_state.db

if "orchestrator" not in st.session_state or not hasattr(st.session_state.orchestrator.bot_agent, "rag_engine"):
    st.session_state.orchestrator = FreeAgentOrchestrator(db_manager=db)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user" not in st.session_state:
    st.session_state.user = None

orchestrator = st.session_state.orchestrator

# Header Banner
st.markdown("""
<div class="cyber-header">
    <div class="cyber-title">🛡️ Cyber Fraud Shield AI Assistant</div>
    <div class="cyber-subtitle">Multi-Agent AI Defense Platform • Voice & Text Scam Detection • End-to-End Data Idempotency</div>
</div>
""", unsafe_allow_html=True)

# Sidebar System Controls
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/shield.png", width=70)
    st.title("System Status")
    
    # Account status in sidebar
    if st.session_state.user:
        u = st.session_state.user
        st.markdown(f"👤 **Logged in as:** `{u['username']}`")
        if st.button("🔒 Logout", key="sidebar_logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        st.caption("🔒 Guest Mode (Log in under 'User Account' tab)")

    st.markdown("---")
    
    active_mode = Config.active_mode()
    if "Free API" in active_mode:
        st.success(f"🟢 {active_mode}")
    else:
        st.info(f"⚡ {active_mode}")
        
    st.markdown("---")
    st.subheader("Free API Configurations")
    
    st.markdown("**1. Groq Free API:** " + ("✅ Connected" if Config.GROQ_API_KEY else "❌ Unset (Using Heuristic Engine)"))
    st.markdown("**2. HuggingFace Token:** " + ("✅ Connected" if Config.HUGGINGFACE_API_KEY else "❌ Unset"))
    st.markdown("**3. Gemini Free API:** " + ("✅ Connected" if Config.GEMINI_API_KEY else "❌ Unset"))
    
    rag_count = len(orchestrator.bot_agent.rag_engine.documents) if hasattr(orchestrator.bot_agent, "rag_engine") else 6
    st.markdown(f"**4. Cyber RAG Engine:** ✅ Active ({rag_count} Playbooks)")

    st.markdown("---")
    st.subheader("⚡ Data Idempotency Cache")
    idempotency_stats = db.get_idempotency_stats()
    st.markdown(f"**Cached Records:** `{idempotency_stats['total_records']}` entries")
    if st.button("🗑️ Clear Idempotency Cache", use_container_width=True):
        ok, msg = db.clear_idempotency_cache()
        if ok:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)
    
    st.markdown("---")
    st.markdown("### 🚨 Emergency Hotlines")
    st.warning("**India National Cyber Hotline:** `1930`\n\n**Report Cyber Crime Portal:** `cybercrime.gov.in`")


# Navigation Tabs
tab_bot, tab_speech, tab_text, tab_profile, tab_benchmark, tab_guide = st.tabs([
    "🤖 Cyber Shield Bot (AI Assistant)",
    "🎙️ Speech & Voice AI Scanner",
    "🔍 Text Scam Scanner",
    "👤 User Account & Profile",
    "📊 Tricky Scenarios Benchmark (100 Cases)",
    "📚 Free AI Agents & Setup Instructions"
])


# ==========================================
# TAB 1: CYBER SHIELD BOT (AI ASSISTANT)
# ==========================================
with tab_bot:
    st.markdown("### 🤖 Cyber Shield Emergency Assistant")
    st.caption("Ask questions about suspicious callers, security threats, or click quick emergency action buttons below.")

    # Quick Emergency Action Buttons
    st.markdown("**🚨 Quick Emergency Protocols:**")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_prompt = None
    with col1:
        if st.button("🔑 Shared OTP / PIN", use_container_width=True):
            quick_prompt = "I mistakenly shared my bank OTP with a caller!"
    with col2:
        if st.button("🌐 Clicked Fake Link", use_container_width=True):
            quick_prompt = "I clicked a suspicious link from an SMS message."
    with col3:
        if st.button("📞 Fake Police/Customs Call", use_container_width=True):
            quick_prompt = "I got a call claiming to be customs saying a illegal package is in my name."
    with col4:
        if st.button("💸 Money Transferred Scam", use_container_width=True):
            quick_prompt = "I transferred money to a scammer, how do I recover funds?"

    st.markdown("---")

    # Render Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Handle user input or quick prompt
    user_input = st.chat_input("Describe the suspicious incident or ask for advice...")
    active_prompt = quick_prompt or user_input

    if active_prompt:
        # Append User Message
        st.session_state.chat_history.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        # Generate Bot Response using CyberShieldBotAgent
        with st.chat_message("assistant"):
            with st.spinner("Cyber Shield Bot is analyzing threat parameters..."):
                response_text = orchestrator.bot_agent.respond(active_prompt, st.session_state.chat_history)
                st.markdown(response_text)
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})

# ==========================================
# TAB 2: SPEECH & VOICE AI SCANNER
# ==========================================
with tab_speech:
    st.markdown("### 🎙️ Speech & AI Voice Spoof Scanner")
    st.caption("Upload or record audio clips to transcribe speech and detect AI-cloned / synthetic voice signatures.")

    col_up, col_info = st.columns([1.2, 1])

    with col_up:
        uploaded_file = st.file_uploader("Upload suspicious voice recording or call audio (.wav, .mp3, .m4a, .ogg)", type=["wav", "mp3", "m4a", "ogg"])
        
        st.markdown("**OR Try Built-in Test Sample Voice Clips:**")
        sample_choice = st.selectbox("Select sample test case:", [
            "None (Upload own file above)",
            "Sample 1: Fake Bank Urgent OTP Call",
            "Sample 2: Customs Seizure Threats (Impersonation)",
            "Sample 3: Family Emergency Impersonation Scam"
        ])

    with col_info:
        st.info("""
        **How Speech Analysis Works:**
        - **Whisper Speech-to-Text:** Transcribes spoken audio into full text transcripts.
        - **Synthetic Voice Detector:** Evaluates spectral micro-variations, pitch stability, and acoustic artifacts to catch deepfake/cloned voice audio.
        - **Fraud Content Engine:** Scans transcribed text for scam indicators.
        """)

    if uploaded_file is not None or sample_choice != "None (Upload own file above)":
        if st.button("🚀 Run Speech & Voice Spoof Analysis", type="primary", use_container_width=True):
            with st.spinner("Transcribing speech and running voice acoustic analysis..."):
                if uploaded_file is not None:
                    audio_bytes = uploaded_file.read()
                    fname = uploaded_file.name
                else:
                    audio_bytes = sample_choice.encode("utf-8")
                    fname = f"{sample_choice.replace(' ', '_').lower()}.wav"
                
                result = orchestrator.speech_agent.analyze_audio(audio_bytes, fname)
                
                st.markdown("---")
                if result.get("idempotent_hit"):
                    st.success("⚡ **Idempotent Cache Hit:** Serving pre-computed, verified audio analysis result instantly without re-processing!")
                st.markdown("### 📊 Voice Analysis Results")
                
                res_col1, res_col2, res_col3 = st.columns(3)
                with res_col1:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-val">{result['overall_voice_risk_score']}/100</div>
                        <div class="metric-lbl">Overall Voice Threat Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                with res_col2:
                    is_synth = result['voice_spoof_metrics']['is_synthetic']
                    badge_class = "badge-critical" if is_synth else "badge-safe"
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size: 1.3rem; margin-top:4px;" class="{badge_class}">{result['voice_spoof_metrics']['voice_nature']}</div>
                        <div class="metric-lbl" style="margin-top:10px;">Voice Classification</div>
                    </div>
                    """, unsafe_allow_html=True)
                with res_col3:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-val">{result['voice_spoof_metrics']['synthetic_confidence']}%</div>
                        <div class="metric-lbl">AI Synthetic Confidence</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("#### 📝 Speech-to-Text Transcription")
                st.info(f"\"{result['transcription']}\"")
                st.caption(f"🎙️ STT Engine: `{result['transcription_engine']}`")

                st.markdown("---")
                st.markdown("### 🔬 Executive Voice Forensics & Forensic Report")

                col_f1, col_f2 = st.columns(2)

                with col_f1:
                    st.markdown("""
                    <div class="glass-card">
                        <h4 style="margin-top:0; color:#38bdf8;">🎙️ Acoustic & Spectral Analysis</h4>
                    """, unsafe_allow_html=True)
                    
                    spoof_m = result['voice_spoof_metrics']
                    st.markdown(f"**Voice Signature:** `{spoof_m.get('voice_nature', 'N/A')}`")
                    st.markdown(f"**Pitch Micro-Stability:** `{spoof_m.get('pitch_stability', 'N/A')}`")
                    st.markdown(f"**Spectral Flatness Index:** `{spoof_m.get('spectral_flatness', 0.0)}`")
                    st.caption(f"Detector Engine: `{result.get('voice_spoof_engine', 'Acoustic Evaluator')}`")
                    
                    st.markdown("**Detected Acoustic Artifacts:**")
                    for artifact in spoof_m.get("artifacts_detected", []):
                        icon = "⚠️" if spoof_m.get("is_synthetic") else "✅"
                        st.markdown(f"- {icon} {artifact}")
                    st.markdown("</div>", unsafe_allow_html=True)

                with col_f2:
                    content_eval = result.get("content_analysis", {})
                    st.markdown("""
                    <div class="glass-card">
                        <h4 style="margin-top:0; color:#818cf8;">🔍 Spoken Content Threat Evaluation</h4>
                    """, unsafe_allow_html=True)
                    st.markdown(f"**Fraud Category:** `{content_eval.get('scam_type', 'N/A')}`")
                    st.markdown(f"**Threat Classification:** `{content_eval.get('threat_level', 'Caution')}`")
                    
                    st.markdown("**Matched Scam Cues:**")
                    for tactic in content_eval.get("matched_tactics", []):
                        st.markdown(f"- 🚩 {tactic}")
                    
                    st.markdown(f"💡 **Actionable Advice:** {content_eval.get('actionable_advice', 'Verify caller identity before acting.')}")
                    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 3: TEXT SCAM SCANNER
# ==========================================
with tab_text:
    st.markdown("### 🔍 Text Scam & Phishing Scanner")
    st.caption("Scan suspicious SMS messages, WhatsApp chats, emails, or call transcripts for scam indicators.")

    sample_texts = {
        "Custom": "",
        "Bank OTP Scam": "URGENT: Your HDFC bank account ending in 4921 has been blocked due to missing KYC. Click http://hdfc-verify-update.com immediately to unblock within 24 hours.",
        "Courier Scam": "FedEx Express: Package #IND9841 could not be delivered due to unpaid customs fee of $5. Pay now at http://bit.ly/fedex-custom-pay or parcel will be returned.",
        "Prize/Lottery Scam": "Congratulations! You have won $50,000 in the Amazon International Lucky Draw. Reply with your bank account number and UPI ID to claim your prize."
    }

    selected_sample = st.selectbox("Load sample threat text:", list(sample_texts.keys()))
    default_text = sample_texts[selected_sample] if selected_sample != "Custom" else ""

    input_text = st.text_area("Paste suspicious text / email content below:", value=default_text, height=140, placeholder="Paste SMS, WhatsApp message, or email here...")

    if st.button("🔍 Scan Text For Fraud", type="primary", use_container_width=True):
        if not input_text.strip():
            st.warning("Please paste some text to scan.")
        else:
            with st.spinner("Text Scam Detector Agent analyzing message patterns..."):
                analysis = orchestrator.text_agent.analyze(input_text)

                st.markdown("---")
                if analysis.get("idempotent_hit"):
                    st.success("⚡ **Idempotent Cache Hit:** Serving pre-computed, verified text scam report instantly without re-processing!")
                st.markdown("### 📋 Scam Analysis Report")

                col_a, col_b = st.columns([1, 1.8])

                with col_a:
                    st.metric("Threat Risk Score", f"{analysis['risk_score']} / 100")
                    st.markdown(f"**Threat Classification:** {analysis['threat_level']}")
                    st.markdown(f"**Scam Category:** `{analysis['scam_type']}`")
                    st.caption(f"Engine: {analysis.get('engine_used', 'Heuristic')}")

                with col_b:
                    st.markdown("**Matched Scam Tactics & Red Flags:**")
                    for flag in analysis.get("matched_tactics", []):
                        st.markdown(f"- ⚠️ {flag}")
                    
                    st.markdown("**Key Warning Signs:**")
                    for sign in analysis.get("key_warning_signs", []):
                        st.markdown(f"- 🔴 {sign}")

                st.info(f"💡 **Actionable Advice:** {analysis.get('actionable_advice', '')}")

# ==========================================
# TAB 4: USER ACCOUNT & PERSONAL PROFILE
# ==========================================
with tab_profile:
    st.markdown("### 👤 User Account & Personal Details")
    
    if st.session_state.user is None:
        st.caption("Log in to your account or register a new profile to personalize your security assistant.")
        
        login_tab, register_tab = st.tabs(["🔑 Login", "📝 Register New Account"])
        
        with login_tab:
            st.markdown("#### Login to Cyber Shield")
            login_user = st.text_input("Username or Email", key="login_user_input")
            login_pass = st.text_input("Password", type="password", key="login_pass_input")
            
            if st.button("🔑 Log In", type="primary", use_container_width=True):
                user_data, msg = db.authenticate_user(login_user, login_pass)
                if user_data:
                    st.session_state.user = user_data
                    st.success(f"Welcome back, {user_data['full_name']}!")
                    st.rerun()
                else:
                    st.error(msg)
                    
        with register_tab:
            st.markdown("#### Create New User Profile")
            with st.form("register_form"):
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    reg_username = st.text_input("Username *", placeholder="johndoe")
                    reg_email = st.text_input("Email Address *", placeholder="john@example.com")
                    reg_password = st.text_input("Password *", type="password")
                    reg_fullname = st.text_input("Full Name *", placeholder="John Doe")
                with col_r2:
                    reg_age = st.number_input("Age *", min_value=18, max_value=120, value=25)
                    reg_mobile = st.text_input("Mobile Number *", placeholder="+91 9876543210")
                    reg_address = st.text_area("Residential Address", placeholder="Street, City, State, Pincode", height=100)
                
                submitted = st.form_submit_button("📝 Register Account", use_container_width=True)
                if submitted:
                    success, msg = db.register_user(
                        username=reg_username,
                        email=reg_email,
                        password=reg_password,
                        full_name=reg_fullname,
                        age=reg_age,
                        mobile_number=reg_mobile,
                        address=reg_address
                    )
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
    else:
        u = st.session_state.user
        st.markdown(f"#### 🛡️ Welcome, **{u['full_name']}** (`@{u['username']}`)")
        
        col_p1, col_p2 = st.columns([1.2, 1])
        
        with col_p1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="margin-top:0; color:#38bdf8;">📋 Saved Personal Profile Details</h4>
            """, unsafe_allow_html=True)
            st.markdown(f"**Full Name:** `{u.get('full_name')}`")
            st.markdown(f"**Username:** `@{u.get('username')}`")
            st.markdown(f"**Email:** `{u.get('email')}`")
            st.markdown(f"**Age:** `{u.get('age')}` years old")
            st.markdown(f"**Mobile Number:** `{u.get('mobile_number')}`")
            st.markdown(f"**Address:** `{u.get('address') or 'Not provided'}`")
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🔒 Log Out of Account", type="secondary", use_container_width=True):
                st.session_state.user = None
                st.rerun()

        with col_p2:
            st.markdown("#### ✏️ Edit Profile Information")
            with st.form("edit_profile_form"):
                edit_name = st.text_input("Full Name", value=u.get('full_name', ''))
                edit_age = st.number_input("Age", min_value=18, max_value=120, value=int(u.get('age') or 25))
                edit_mobile = st.text_input("Mobile Number", value=u.get('mobile_number', ''))
                edit_address = st.text_area("Residential Address", value=u.get('address', ''), height=100)
                
                saved = st.form_submit_button("💾 Save Profile Changes", use_container_width=True)
                if saved:
                    ok, msg = db.update_user_profile(
                        user_id=u['user_id'],
                        full_name=edit_name,
                        age=edit_age,
                        mobile_number=edit_mobile,
                        address=edit_address
                    )
                    if ok:
                        updated_profile = db.get_user_profile(u['user_id'])
                        if updated_profile:
                            st.session_state.user['full_name'] = updated_profile['full_name']
                            st.session_state.user['age'] = updated_profile['age']
                            st.session_state.user['mobile_number'] = updated_profile['mobile_number']
                            st.session_state.user['address'] = updated_profile['address']
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

# ==========================================
# TAB 5: TRICKY SCENARIOS BENCHMARK
# ==========================================
with tab_benchmark:
    st.markdown("### 📊 Tricky Scenarios Benchmark (100 Cases)")
    st.caption("Evaluate the performance of Cyber Fraud Shield AI Agents against the dataset of 100 tricky test scenarios (Prompt Injection, Negation, Multilingual, Gap Tests).")

    # Load scenarios
    scenarios_path = "src/model/data/tricky_test_scenarios.json"
    if not os.path.exists(scenarios_path):
        st.error(f"Dataset file not found at `{scenarios_path}`")
    else:
        with open(scenarios_path, "r", encoding="utf-8") as f:
            scenarios = json.load(f)

        # Count stats
        total_cases = len(scenarios)
        scam_cases = sum(1 for s in scenarios if s.get("is_scam") == 1)
        safe_cases = sum(1 for s in scenarios if s.get("is_scam") == 0)

        # Display Stats Summary
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{total_cases}</div>
                <div class="metric-lbl">Total Scenarios</div>
            </div>
            """, unsafe_allow_html=True)
        with stat_col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: #ef4444;">{scam_cases}</div>
                <div class="metric-lbl">Scam Targets</div>
            </div>
            """, unsafe_allow_html=True)
        with stat_col3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: #10b981;">{safe_cases}</div>
                <div class="metric-lbl">Safe Targets</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Interactive explorer
        st.markdown("#### 🔍 Select Scenario to Run Live Agent Analysis")
        categories = sorted(list(set(s.get("category", "General") for s in scenarios)))
        selected_cat = st.selectbox("Filter by Category:", ["All"] + categories)

        filtered_scenarios = [s for s in scenarios if selected_cat == "All" or s.get("category") == selected_cat]

        scenario_options = [f"#{i+1}: {s.get('text')[:75]}..." for i, s in enumerate(filtered_scenarios)]
        selected_scenario_idx = st.selectbox("Choose a scenario:", range(len(filtered_scenarios)), format_func=lambda x: scenario_options[x])

        if len(filtered_scenarios) > 0:
            target_scenario = filtered_scenarios[selected_scenario_idx]
            st.markdown(f"""
            <div class="glass-card">
                <h5>Scenario Prompt:</h5>
                <p style="font-size: 1.1rem; font-style: italic; color: #cbd5e1;">"{target_scenario.get('text')}"</p>
                <p><b>Category:</b> {target_scenario.get('category')} | <b>Expected Threat:</b> {"⚠️ SCAM / FRAUD" if target_scenario.get('is_scam') == 1 else "✅ SAFE / NO ACTION"}</p>
                <p><b>Expected Behavior Focus:</b> <code>{target_scenario.get('expected_behavior')}</code></p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚀 Run Live Scenario Evaluation", key="btn_run_benchmark", type="primary", use_container_width=True):
                with st.spinner("Executing agent evaluation pipelines..."):
                    text = target_scenario.get("text")
                    analysis = orchestrator.text_agent.analyze(text)
                    
                    st.markdown("##### 📋 Agent Output Details")
                    res_a, res_b = st.columns([1, 1.8])
                    with res_a:
                        st.metric("Threat Risk Score", f"{analysis['risk_score']} / 100")
                        st.markdown(f"**Threat Classification:** {analysis['threat_level']}")
                        st.markdown(f"**Scam Category:** `{analysis['scam_type']}`")
                        st.caption(f"Engine: {analysis.get('engine_used', 'Heuristic')}")
                    with res_b:
                        st.markdown("**Red Flags & Tactics Detected:**")
                        for flag in analysis.get("matched_tactics", []):
                            st.markdown(f"- ⚠️ {flag}")
                        
                        st.markdown("**Key Warning Signs:**")
                        for sign in analysis.get("key_warning_signs", []):
                            st.markdown(f"- 🔴 {sign}")
                    
                    # Verify correctness
                    is_scam_expected = target_scenario.get("is_scam") == 1
                    is_scam_predicted = analysis["threat_level"] != "Safe"
                    passed = is_scam_expected == is_scam_predicted

                    st.markdown("---")
                    if passed:
                        st.success("✅ **EVALUATION PASSED** - The AI agent's prediction matches the target threat assessment.")
                    else:
                        st.warning("⚠️ **EVALUATION MISMATCH** - The AI agent flagged this differently from the expected baseline. Verify details below.")
                        
                    st.info(f"💡 **Actionable Advice:** {analysis.get('actionable_advice', '')}")

# ==========================================
# TAB 6: FREE AI AGENTS & SETUP GUIDE
# ==========================================
with tab_guide:

    st.markdown("### 📚 Free AI Keys & Agents Setup Guide")
    st.markdown("""
    This project is built to run 100% free using open-source models, free-tier AI APIs, and local fallback engines.
    Below is your complete step-by-step walkthrough to configure free API keys and understand the multi-agent architecture.
    """)

    st.markdown("---")
    st.markdown("### 🔑 Step 1: Acquiring 100% Free API Keys")

    st.markdown("""
    <div class="guide-box">
        <h4>1. Groq Free API (Recommended - Ultra Fast)</h4>
        <ul>
            <li><b>What it provides:</b> Free access to <code>Llama 3.3 70B Versatile</code> (LLM agent) and <code>Whisper Large v3</code> (voice transcription).</li>
            <li><b>Cost:</b> 100% Free with generous daily rate limits.</li>
            <li><b>How to get key:</b>
                <ol>
                    <li>Go to <a href="https://console.groq.com" target="_blank">console.groq.com</a></li>
                    <li>Sign up / log in with Google or GitHub.</li>
                    <li>Navigate to <b>API Keys</b> &rarr; Click <b>Create API Key</b>.</li>
                    <li>Copy key starting with <code>gsk_...</code></li>
                </ol>
            </li>
        </ul>
    </div>
    
    <div class="guide-box">
        <h4>2. Hugging Face Free Token</h4>
        <ul>
            <li><b>What it provides:</b> Free access to open-source speech, voice spoof, and NLP models.</li>
            <li><b>How to get key:</b>
                <ol>
                    <li>Go to <a href="https://huggingface.co/settings/tokens" target="_blank">huggingface.co/settings/tokens</a></li>
                    <li>Create a free account &rarr; Click <b>New Token</b> (Role: Read).</li>
                    <li>Copy key starting with <code>hf_...</code></li>
                </ol>
            </li>
        </ul>
    </div>

    <div class="guide-box">
        <h4>3. Google Gemini Free API Key</h4>
        <ul>
            <li><b>What it provides:</b> Free access to <code>Gemini 1.5 Flash</code> for advanced reasoning.</li>
            <li><b>How to get key:</b>
                <ol>
                    <li>Go to <a href="https://aistudio.google.com" target="_blank">aistudio.google.com</a></li>
                    <li>Click <b>Get API Key</b> &rarr; Create Key in new project.</li>
                </ol>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🛠️ Step 2: Configuring Environment & Running the Web App")

    st.code("""
# 1. Open .env file or copy from .env.example
cp .env.example .env

# 2. Add your free API key in .env:
GROQ_API_KEY=gsk_your_free_groq_key_here

# 3. Launch the Streamlit Web Application:
streamlit run src/app.py
""", language="bash")

    st.markdown("---")
    st.markdown("### 🤖 Step 3: Multi-Agent Architecture Overview")
    st.markdown("""
    The application coordinates three dedicated AI agents:
    1. **Text Scam Detector Agent (`src/agents/text_agent.py`):** Uses heuristic threat rules + Llama-3.3-70B to detect social engineering and phishing tactics.
    2. **Speech & Voice Spoof Agent (`src/agents/speech_agent.py`):** Runs Whisper voice transcription + spectral acoustic artifact analysis for deepfake voice detection.
    3. **Cyber Shield Bot Agent (`src/agents/bot_agent.py`):** Interactive emergency advisor agent providing step-by-step banking freeze & cybercrime reporting playbooks.
    """)

# Footer
st.markdown("---")
st.caption("🛡️ Cyber Fraud Shield • Built for HackIndia • Open-Source & Free AI Powered")
