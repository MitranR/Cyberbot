/**
 * Cyberbot AI Voice & Speech Recognition Engine
 * Provides native browser-based Speech Recognition (Voice Input)
 * and Speech Synthesis (Voice Read Aloud / TTS).
 * 100% Client-side, works in Google Chrome, Microsoft Edge, Safari, Brave, and Opera.
 */

(function () {
    console.log("[Cyberbot Voice] Initializing Voice & Speech Engine...");

    window.currentBotLang = window.currentBotLang || 'English';

    window.cyberBotTTS = {
        recognition: null,
        isRecording: false,

        getLangCode: function (lang) {
            const l = (lang || window.currentBotLang || 'English').toLowerCase();
            if (l.includes('tamil') || l.includes('தமிழ்')) return 'ta-IN';
            if (l.includes('german') || l.includes('deutsch')) return 'de-DE';
            if (l.includes('japanese') || l.includes('日本語')) return 'ja-JP';
            return 'en-US';
        },

        startVoiceInput: function () {
            console.log("[Cyberbot Voice] startVoiceInput clicked.");
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;

            const statusEl = document.getElementById('voiceMicStatus');
            const micIcon = document.getElementById('micButtonIcon');
            const micBtn = document.getElementById('micButton');

            if (!SpeechRec) {
                const msg = "Voice speech recognition is supported in Google Chrome, Microsoft Edge, and Safari. Please open the website in Chrome or Edge.";
                alert(msg);
                if (statusEl) {
                    statusEl.innerHTML = '⚠️ Voice input is supported in Google Chrome & Microsoft Edge.';
                    statusEl.style.display = 'block';
                    statusEl.style.background = 'rgba(239, 68, 68, 0.2)';
                    statusEl.style.color = '#FCA5A5';
                }
                return;
            }

            // Toggle off if already recording
            if (window.cyberBotTTS.isRecording) {
                console.log("[Cyberbot Voice] Manually stopping voice recognition");
                if (window.cyberBotTTS.recognition) {
                    try { window.cyberBotTTS.recognition.stop(); } catch (e) { }
                }
                window.cyberBotTTS.isRecording = false;
                if (statusEl) statusEl.style.display = 'none';
                if (micIcon) micIcon.style.color = '#38BDF8';
                if (micBtn) {
                    micBtn.style.borderColor = '#38BDF8';
                    micBtn.style.boxShadow = 'none';
                }
                return;
            }

            const currentLang = window.currentBotLang || 'English';
            const langCode = window.cyberBotTTS.getLangCode(currentLang);
            console.log("[Cyberbot Voice] Starting SpeechRec with language:", currentLang, "code:", langCode);

            let rec;
            try {
                rec = new SpeechRec();
            } catch (err) {
                console.error("[Cyberbot Voice] Could not construct SpeechRecognition:", err);
                if (statusEl) {
                    statusEl.innerHTML = '⚠️ Speech Recognition error: ' + err.message;
                    statusEl.style.display = 'block';
                }
                return;
            }

            rec.lang = langCode;
            rec.interimResults = true;
            rec.continuous = false;
            rec.maxAlternatives = 1;

            let finalTranscript = '';

            rec.onstart = function () {
                console.log("[Cyberbot Voice] Speech recognition started. Listening...");
                window.cyberBotTTS.isRecording = true;

                if (micIcon) micIcon.style.color = '#EF4444';
                if (micBtn) {
                    micBtn.style.borderColor = '#EF4444';
                    micBtn.style.boxShadow = '0 0 14px rgba(239, 68, 68, 0.7)';
                }

                if (statusEl) {
                    statusEl.innerHTML = '🔴 <b>Listening (' + currentLang + ')...</b> Speak into your microphone';
                    statusEl.style.display = 'block';
                    statusEl.style.background = 'rgba(239, 68, 68, 0.15)';
                    statusEl.style.color = '#FCA5A5';
                }
            };

            rec.onresult = function (event) {
                let interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }

                const spokenNow = (finalTranscript || interimTranscript).trim();
                console.log("[Cyberbot Voice] Recognized speech:", spokenNow);

                if (statusEl && spokenNow) {
                    statusEl.innerHTML = '🎙️ <i>"' + spokenNow + '"</i>';
                }

                const inputEl = document.getElementById('botChatInput');
                if (inputEl && spokenNow) {
                    const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
                    if (nativeSetter) {
                        nativeSetter.call(inputEl, spokenNow);
                    } else {
                        inputEl.value = spokenNow;
                    }
                    inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                    inputEl.dispatchEvent(new Event('change', { bubbles: true }));
                }
            };

            rec.onerror = function (event) {
                console.warn("[Cyberbot Voice] Speech recognition error event:", event.error);
                window.cyberBotTTS.isRecording = false;

                if (micIcon) micIcon.style.color = '#38BDF8';
                if (micBtn) {
                    micBtn.style.borderColor = '#38BDF8';
                    micBtn.style.boxShadow = 'none';
                }

                if (statusEl) {
                    if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
                        statusEl.innerHTML = '⚠️ <b>Microphone blocked.</b> Please allow microphone access in your browser address bar.';
                        alert("Microphone access is blocked. Please click the lock or site settings icon in your browser address bar and allow Microphone access.");
                    } else if (event.error === 'no-speech') {
                        statusEl.innerHTML = '⚠️ No voice detected. Tap microphone and speak again.';
                    } else {
                        statusEl.innerHTML = '⚠️ Voice error: ' + event.error;
                    }
                    statusEl.style.display = 'block';
                    setTimeout(function () {
                        if (!window.cyberBotTTS.isRecording && statusEl) {
                            statusEl.style.display = 'none';
                        }
                    }, 3500);
                }
            };

            rec.onend = function () {
                console.log("[Cyberbot Voice] Speech recognition ended. Final text:", finalTranscript);
                window.cyberBotTTS.isRecording = false;

                if (micIcon) micIcon.style.color = '#38BDF8';
                if (micBtn) {
                    micBtn.style.borderColor = '#38BDF8';
                    micBtn.style.boxShadow = 'none';
                }

                const textToSend = finalTranscript.trim();
                if (textToSend) {
                    if (statusEl) {
                        statusEl.innerHTML = '✅ Sending: "<b>' + textToSend + '</b>"';
                        statusEl.style.background = 'rgba(16, 185, 129, 0.15)';
                        statusEl.style.color = '#6EE7B7';
                    }

                    const inputEl = document.getElementById('botChatInput');
                    if (inputEl) {
                        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
                        if (nativeSetter) {
                            nativeSetter.call(inputEl, textToSend);
                        } else {
                            inputEl.value = textToSend;
                        }
                        inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                        inputEl.dispatchEvent(new Event('change', { bubbles: true }));
                    }

                    setTimeout(function () {
                        const sendBtn = document.getElementById('botSendBtn');
                        const formEl = document.getElementById('botChatForm');
                        if (sendBtn) {
                            sendBtn.click();
                        } else if (formEl && formEl.requestSubmit) {
                            formEl.requestSubmit();
                        }
                        setTimeout(function () {
                            if (statusEl) statusEl.style.display = 'none';
                        }, 1200);
                    }, 300);
                } else {
                    if (statusEl) {
                        setTimeout(function () {
                            if (!window.cyberBotTTS.isRecording && statusEl) {
                                statusEl.style.display = 'none';
                            }
                        }, 1500);
                    }
                }
            };

            window.cyberBotTTS.recognition = rec;
            try {
                rec.start();
            } catch (e) {
                console.error("[Cyberbot Voice] rec.start() threw error:", e);
                window.cyberBotTTS.isRecording = false;
                if (micIcon) micIcon.style.color = '#38BDF8';
                if (micBtn) {
                    micBtn.style.borderColor = '#38BDF8';
                    micBtn.style.boxShadow = 'none';
                }
            }
        },

        speak: function (text, lang) {
            if (!('speechSynthesis' in window)) return;
            window.speechSynthesis.cancel();

            const plainText = text.replace(/[*#_`>]/g, '').replace(/https?:\/\/\S+/g, 'link');
            const utterance = new SpeechSynthesisUtterance(plainText);
            const langCode = window.cyberBotTTS.getLangCode(lang || window.currentBotLang || 'English');
            utterance.lang = langCode;
            utterance.rate = 1.0;
            utterance.pitch = 1.0;

            const voices = window.speechSynthesis.getVoices();
            if (voices && voices.length > 0) {
                const matchedVoice = voices.find(function (v) {
                    return v.lang && v.lang.toLowerCase().startsWith(langCode.substring(0, 2).toLowerCase());
                });
                if (matchedVoice) utterance.voice = matchedVoice;
            }

            window.speechSynthesis.speak(utterance);
        },

        stopSpeaking: function () {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
            }
        }
    };

    window.startCyberBotVoiceInput = function () {
        if (window.cyberBotTTS && window.cyberBotTTS.startVoiceInput) {
            window.cyberBotTTS.startVoiceInput();
        } else {
            console.error("[Cyberbot Voice] window.cyberBotTTS not yet initialized.");
        }
    };

    console.log("[Cyberbot Voice] Engine ready. window.startCyberBotVoiceInput is available.");
})();
