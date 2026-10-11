import reflex as rx
from cyber_shield_reflex.state import State


def voice_speech_scripts() -> rx.Component:
    """
    Client-side Web Speech Recognition (Voice Input) & Speech Synthesis (Voice Read Aloud) Engine.
    100% Free, runs natively in all modern browsers without any paid external speech APIs.
    Supports English, Tamil (ta-IN), German (de-DE), and Japanese (ja-JP).
    """
    return rx.html(
        r"""
        <script>
        window.cyberBotTTS = {
            recognition: null,
            isRecording: false,
            
            getLangCode: function(lang) {
                switch(lang) {
                    case 'Tamil': return 'ta-IN';
                    case 'German': return 'de-DE';
                    case 'Japanese': return 'ja-JP';
                    default: return 'en-US';
                }
            },

            startVoiceInput: function() {
                const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRec) {
                    alert("Speech recognition is supported in Google Chrome, Microsoft Edge, and Safari. Please use one of these browsers.");
                    return;
                }

                const statusEl = document.getElementById('voiceMicStatus');
                const micIcon = document.getElementById('micButtonIcon');

                if (window.cyberBotTTS.isRecording) {
                    if (window.cyberBotTTS.recognition) {
                        try { window.cyberBotTTS.recognition.stop(); } catch(e) {}
                    }
                    window.cyberBotTTS.isRecording = false;
                    if (statusEl) statusEl.style.display = 'none';
                    if (micIcon) micIcon.style.color = '#38BDF8';
                    return;
                }

                const currentLang = window.currentBotLang || 'English';
                const langCode = window.cyberBotTTS.getLangCode(currentLang);

                const rec = new SpeechRec();
                rec.lang = langCode;
                rec.interimResults = false;
                rec.continuous = false;
                rec.maxAlternatives = 1;

                if (statusEl) {
                    statusEl.innerHTML = '🎙️ <b>Listening in ' + currentLang + '...</b> Speak now';
                    statusEl.style.display = 'block';
                }

                rec.onstart = function() {
                    window.cyberBotTTS.isRecording = true;
                    if (micIcon) micIcon.style.color = '#EF4444';
                };

                rec.onresult = function(event) {
                    if (event.results && event.results.length > 0) {
                        const transcript = event.results[0][0].transcript;
                        const inputEl = document.getElementById('botChatInput');
                        if (inputEl) {
                            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
                            if (nativeSetter) {
                                nativeSetter.call(inputEl, transcript);
                            } else {
                                inputEl.value = transcript;
                            }
                            inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                            inputEl.dispatchEvent(new Event('change', { bubbles: true }));
                        }
                        
                        if (statusEl) {
                            statusEl.innerHTML = '✅ <i>"' + transcript + '"</i>';
                        }

                        setTimeout(() => {
                            const formEl = document.getElementById('botChatForm');
                            if (formEl && formEl.requestSubmit) {
                                formEl.requestSubmit();
                            } else {
                                const sendBtn = document.getElementById('botSendBtn');
                                if (sendBtn) sendBtn.click();
                            }
                            setTimeout(() => {
                                if (statusEl) statusEl.style.display = 'none';
                            }, 1200);
                        }, 350);
                    }
                };

                rec.onerror = function(event) {
                    console.log("Voice speech recognition error:", event.error);
                    if (statusEl) {
                        statusEl.innerHTML = '⚠️ Voice input: ' + event.error;
                        setTimeout(() => { if (statusEl) statusEl.style.display = 'none'; }, 2000);
                    }
                    window.cyberBotTTS.isRecording = false;
                    if (micIcon) micIcon.style.color = '#38BDF8';
                };

                rec.onend = function() {
                    window.cyberBotTTS.isRecording = false;
                    if (micIcon) micIcon.style.color = '#38BDF8';
                };

                window.cyberBotTTS.recognition = rec;
                try {
                    rec.start();
                } catch(e) {
                    console.log("Speech recognition start exception:", e);
                }
            },

            speak: function(text, lang) {
                if (!('speechSynthesis' in window)) return;
                window.speechSynthesis.cancel(); // Stop any previous speech

                // Strip markdown formatting symbols for clean vocal speech
                const plainText = text.replace(/[*#_`>]/g, '').replace(/https?:\/\/\S+/g, 'link');
                const utterance = new SpeechSynthesisUtterance(plainText);
                const langCode = window.cyberBotTTS.getLangCode(lang || window.currentBotLang || 'English');
                utterance.lang = langCode;
                utterance.rate = 1.0;
                utterance.pitch = 1.0;

                // Pick best localized voice if available
                const voices = window.speechSynthesis.getVoices();
                const matchedVoice = voices.find(v => v.lang && v.lang.toLowerCase().startsWith(langCode.substring(0, 2).toLowerCase()));
                if (matchedVoice) utterance.voice = matchedVoice;

                window.speechSynthesis.speak(utterance);
            },

            stopSpeaking: function() {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                }
            }
        };
        </script>
        """
    )


def lang_pill(label: str, lang_key: str, flag: str) -> rx.Component:
    """Renders a language switch pill button."""
    is_active = State.bot_language == lang_key
    return rx.button(
        rx.hstack(
            rx.text(flag, font_size="13px"),
            rx.text(label, font_size="11px", font_weight="700"),
            spacing="1",
            align="center",
        ),
        size="1",
        background=rx.cond(is_active, "#1D4ED8", "#1E293B"),
        color=rx.cond(is_active, "#FFFFFF", "#94A3B8"),
        border=rx.cond(is_active, "1px solid #38BDF8", "1px solid #334155"),
        border_radius="16px",
        padding_x="10px",
        padding_y="4px",
        cursor="pointer",
        on_click=[
            State.set_bot_language(lang_key),
            rx.call_script(f"window.currentBotLang = '{lang_key}';"),
        ],
        _hover={"background": "#2563EB", "color": "#FFFFFF"},
    )


def quick_chip(label: str, prompt: str) -> rx.Component:
    """Renders a 1-click quick suggestion chip for instant queries."""
    return rx.button(
        label,
        size="1",
        variant="surface",
        background="#0F172A",
        color="#38BDF8",
        border="1px solid #1E293B",
        border_radius="12px",
        font_size="10px",
        font_weight="600",
        padding_x="8px",
        padding_y="2px",
        cursor="pointer",
        on_click=State.send_quick_prompt(prompt),
        _hover={"background": "#1E293B", "border_color": "#38BDF8", "color": "#FFFFFF"},
    )


def render_message(msg: rx.Var[dict]) -> rx.Component:
    """Renders an individual chat message with read-aloud TTS button."""
    is_bot = msg["sender"] == "bot"  # type: ignore
    return rx.hstack(
        rx.cond(
            is_bot,
            rx.box(
                rx.icon("bot", size=18, color="#FFFFFF"),
                background="#1D4ED8",
                padding="6px",
                border_radius="50%",
                flex_shrink="0",
                box_shadow="0 0 10px rgba(56, 189, 248, 0.4)",
            ),
        ),
        rx.vstack(
            rx.box(
                rx.markdown(
                    msg["text"],  # type: ignore
                    font_size="13px",
                    color="#FFFFFF",
                    font_family="'Outfit', sans-serif",
                ),
                background=rx.cond(is_bot, "#1E293B", "#1D4ED8"),
                padding="10px 14px",
                border_radius="12px",
                border=rx.cond(is_bot, "1px solid #334155", "none"),
                box_shadow="0 4px 14px rgba(0, 0, 0, 0.3)",
                width="100%",
            ),
            # Speak / Read Aloud Action for bot responses
            rx.cond(
                is_bot,
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("volume-2", size=12, color="#38BDF8"),
                            rx.text("Read Aloud", font_size="10px", color="#38BDF8", font_weight="600"),
                            spacing="1",
                            align="center",
                        ),
                        variant="ghost",
                        size="1",
                        padding_x="6px",
                        padding_y="2px",
                        cursor="pointer",
                        on_click=State.speak_bot_text(msg["text"]),  # type: ignore
                        _hover={"background": "rgba(56, 189, 248, 0.15)"},
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("volume-x", size=12, color="#94A3B8"),
                            rx.text("Stop", font_size="10px", color="#94A3B8"),
                            spacing="1",
                            align="center",
                        ),
                        variant="ghost",
                        size="1",
                        padding_x="6px",
                        padding_y="2px",
                        cursor="pointer",
                        on_click=State.stop_bot_speech,
                        _hover={"background": "rgba(148, 163, 184, 0.15)"},
                    ),
                    spacing="2",
                    align="center",
                    margin_top="2px",
                ),
            ),
            spacing="1",
            align=rx.cond(is_bot, "start", "end"),
            max_width="85%",
        ),
        justify=rx.cond(is_bot, "start", "end"),
        width="100%",
        spacing="2",
        align="start",
        margin_y="4px",
    )


def bot_agent() -> rx.Component:
    """
    Multilingual, Voice-Controlled Cyber Shield AI Assistant Widget.
    Includes voice input microphone, read aloud text-to-speech,
    and supports English, Tamil (தமிழ்), German (Deutsch), and Japanese (日本語).
    """
    return rx.box(
        # Client-side Speech Recognition & Synthesis Integration
        voice_speech_scripts(),

        # Floating Chat Window Popup
        rx.cond(
            State.bot_open,
            rx.box(
                # Header Bar
                rx.box(
                    rx.hstack(
                        rx.hstack(
                            rx.icon("bot", size=22, color="#38BDF8"),
                            rx.vstack(
                                rx.text("Cyberbot AI Assistant", font_size="14px", font_weight="700", color="#FFFFFF", font_family="'Space Grotesk', sans-serif"),
                                rx.text(f"Voice & Multilingual • {State.bot_language}", font_size="11px", color="#38BDF8", font_family="'Outfit', sans-serif"),
                                spacing="0",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.hstack(
                            # Auto-read toggle button
                            rx.button(
                                rx.hstack(
                                    rx.icon("volume-2", size=13, color=rx.cond(State.auto_read_aloud, "#38BDF8", "#64748B")),
                                    rx.text("Auto Read", font_size="10px", color=rx.cond(State.auto_read_aloud, "#38BDF8", "#64748B")),
                                    spacing="1",
                                    align="center",
                                ),
                                variant="ghost",
                                size="1",
                                padding_x="4px",
                                on_click=State.toggle_auto_read,
                                title="Toggle Auto Read-Aloud for responses",
                                _hover={"opacity": 0.8},
                            ),
                            # Clear chat
                            rx.icon(
                                "trash-2",
                                size=16,
                                color="#94A3B8",
                                cursor="pointer",
                                on_click=State.clear_bot_chat,
                                title="Clear conversation",
                                _hover={"color": "#EF4444"},
                            ),
                            # Stop TTS Voice Audio button
                            rx.icon(
                                "volume-x",
                                size=17,
                                color="#94A3B8",
                                cursor="pointer",
                                on_click=State.stop_bot_speech,
                                title="Stop Speech Audio",
                                _hover={"color": "#EF4444"},
                            ),
                            # Close Window
                            rx.icon(
                                "x",
                                size=19,
                                color="#94A3B8",
                                cursor="pointer",
                                on_click=State.toggle_bot,  # type: ignore
                                _hover={"color": "#FFFFFF"},
                            ),
                            spacing="2",
                            align="center",
                        ),
                        justify="between",
                        align="center",
                        padding="12px 16px",
                        background="#0B132B",
                        border_bottom="1px solid #1E293B",
                        border_top_left_radius="16px",
                        border_top_right_radius="16px",
                    ),
                    # Dropdown Control Bar (Language & Complaints Dropdowns)
                    rx.vstack(
                        # 1. Language Dropdown Menu
                        rx.hstack(
                            rx.hstack(
                                rx.icon("languages", size=14, color="#38BDF8"),
                                rx.text("Language:", font_size="11px", font_weight="600", color="#94A3B8"),
                                spacing="1",
                                align="center",
                                min_width="76px",
                            ),
                            rx.box(
                                rx.select(
                                    [
                                        "🇬🇧 English",
                                        "🇮🇳 தமிழ் (Tamil)",
                                        "🇩🇪 Deutsch (German)",
                                        "🇯🇵 日本語 (Japanese)",
                                    ],
                                    value=State.bot_language_display,
                                    on_change=State.change_language_select,
                                    size="1",
                                    variant="surface",
                                    color_scheme="blue",
                                    width="100%",
                                    cursor="pointer",
                                ),
                                flex="1",
                                width="100%",
                            ),
                            width="100%",
                            align="center",
                            spacing="2",
                        ),
                        # 2. Complaints & Threat Scenarios Dropdown Menu
                        rx.hstack(
                            rx.hstack(
                                rx.icon("shield-alert", size=14, color="#F87171"),
                                rx.text("Complaints:", font_size="11px", font_weight="600", color="#94A3B8"),
                                spacing="1",
                                align="center",
                                min_width="76px",
                            ),
                            rx.box(
                                rx.select(
                                    [
                                        "🚨 1930 Helpline - Report Fraud",
                                        "🛑 Digital Arrest - Fake Police",
                                        "🎙️ Voice Clone - Deepfake Call",
                                        "💳 Bank OTP & KYC Scam",
                                        "💼 Telegram Task Scheme",
                                        "🔞 Sextortion - Video Blackmail",
                                        "📱 SIM Swap - Lost Signal",
                                        "📦 FedEx Customs Parcel Hold",
                                        "📲 Malicious APK & AnyDesk",
                                        "🔓 Hacked Account Recovery",
                                        "🔐 Strong Password & 2FA",
                                        "💻 Python Security Script",
                                    ],
                                    placeholder="⚡ Select Threat / Complaint...",
                                    value=State.selected_complaint_topic,
                                    on_change=State.handle_complaint_select,
                                    size="1",
                                    variant="surface",
                                    color_scheme="blue",
                                    width="100%",
                                    cursor="pointer",
                                ),
                                flex="1",
                                width="100%",
                            ),
                            width="100%",
                            align="center",
                            spacing="2",
                        ),
                        spacing="2",
                        padding_x="14px",
                        padding_y="9px",
                        background="#070D1E",
                        border_bottom="1px solid #1E293B",
                        width="100%",
                    ),
                    width="100%",
                ),
                
                # Chat Messages Container
                rx.vstack(
                    rx.foreach(State.bot_messages, render_message),
                    padding="16px",
                    height="325px",
                    overflow_y="auto",
                    width="100%",
                    spacing="2",
                    background="#030712",
                ),

                # Voice Microphone Status Indicator (Shown while speaking)
                rx.html(
                    """
                    <div id="voiceMicStatus" style="display: none; padding: 6px 14px; background: rgba(220, 38, 38, 0.2); border-top: 1px solid rgba(239, 68, 68, 0.4); color: #FCA5A5; font-size: 11px; font-weight: 700; font-family: monospace; animation: pulse 1.5s infinite; text-align: center;">
                        🎙️ Listening... Speak now
                    </div>
                    """
                ),
                
                # Bottom Input Form (Instant Single-Enter submission + Voice Microphone + Send)
                rx.form(
                    rx.hstack(
                        rx.input(
                            id="botChatInput",
                            name="message",
                            placeholder="Type a query and press Enter (or tap mic to speak)...",
                            font_size="13px",
                            background="#1E293B",
                            color="#FFFFFF",
                            border="1px solid #334155",
                            border_radius="8px",
                            width="100%",
                            padding_x="12px",
                            _focus={"border": "1px solid #38BDF8"},
                            auto_focus=True,
                        ),
                        # Voice Microphone Control Button (type="button" so it does not submit form)
                        rx.button(
                            rx.html("""<span id="micButtonIcon" style="color: #38BDF8; font-size: 16px;">🎙️</span>"""),
                            type="button",
                            cursor="pointer",
                            background="#0F172A",
                            border="1px solid #38BDF8",
                            border_radius="8px",
                            padding_x="10px",
                            title="Click to speak using your microphone",
                            on_click=rx.call_script("window.cyberBotTTS.startVoiceInput();"),
                            _hover={"background": "#1E293B", "box-shadow": "0 0 10px rgba(56, 189, 248, 0.5)"},
                        ),
                        # Send Button (type="submit" to natively submit form)
                        rx.button(
                            rx.icon("send", size=16, color="#FFFFFF"),
                            id="botSendBtn",
                            type="submit",
                            background="linear-gradient(90deg, #1D4ED8 0%, #0284C7 100%)",
                            cursor="pointer",
                            border_radius="8px",
                            padding_x="14px",
                            _hover={"opacity": 0.9},
                        ),
                        padding="12px 16px",
                        border_top="1px solid #1E293B",
                        background="#0B132B",
                        border_bottom_left_radius="16px",
                        border_bottom_right_radius="16px",
                        width="100%",
                        spacing="2",
                        align="center",
                    ),
                    id="botChatForm",
                    on_submit=State.handle_chat_submit,
                    reset_on_submit=True,
                    width="100%",
                ),
                position="fixed",
                bottom="86px",
                right="24px",
                width="400px",
                max_width="calc(100vw - 32px)",
                height="530px",
                background="#030712",
                border_radius="16px",
                box_shadow="0 20px 50px rgba(0, 0, 0, 0.85)",
                border="1px solid #1E293B",
                z_index="1000",
                display="flex",
                flex_direction="column",
                overflow="hidden",
            ),
        ),
        
        # Floating Trigger Circle Button with Glow Badge
        rx.button(
            rx.hstack(
                rx.icon("bot", size=24, color="#FFFFFF"),
                rx.text("Cyberbot AI", font_size="13px", font_weight="700", color="#FFFFFF", display={"initial": "none", "sm": "block"}),
                rx.box(
                    width="8px",
                    height="8px",
                    border_radius="50%",
                    background="#38BDF8",
                    box_shadow="0 0 8px #38BDF8",
                ),
                spacing="2",
                align="center",
            ),
            on_click=State.toggle_bot,  # type: ignore
            position="fixed",
            bottom="24px",
            right="24px",
            background="linear-gradient(90deg, #1D4ED8 0%, #0284C7 100%)",
            color="#FFFFFF",
            padding="12px 20px",
            border_radius="30px",
            box_shadow="0 8px 24px rgba(2, 132, 199, 0.5)",
            cursor="pointer",
            z_index="999",
            _hover={"transform": "scale(1.05)", "box_shadow": "0 10px 30px rgba(56, 189, 248, 0.7)"},
            transition="all 0.2s ease-in-out",
        ),
    )
