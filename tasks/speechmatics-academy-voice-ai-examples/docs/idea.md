# Idea: Speechmatics Academy Voice AI Examples

## Source

- GitHub: https://github.com/speechmatics/speechmatics-academy
- Title: `speechmatics/speechmatics-academy: Speechmatics Academy`

## Capture

Moh shared the Speechmatics Academy repository and asked to add it to taskOS and Kanban.

The repository describes itself as a comprehensive collection of working examples, integrations, templates, and use cases for Speechmatics SDKs. It covers batch transcription, real-time streaming, voice agents, text-to-speech, diarization, speaker identification/focus, audio intelligence, multilingual transcription/translation, and third-party integrations.

## Why this might be useful

Speechmatics Academy looks valuable because it is example-driven. Rather than only documenting APIs, it includes runnable project structures and real integrations:

- LiveKit voice assistants and telephony.
- Pipecat voice bots and web bots.
- Twilio outbound dialer / media streams.
- VAPI assistant integration.
- Healthcare dictation and medical assistant patterns.
- Call center analytics.
- Video captioning.
- Smart turn detection and speaker focus.

This may be useful for:

- Future Hermes voice workflows.
- Voice-agent product demos.
- Speech-to-text evaluation against Deepgram/AssemblyAI/Whisper/Azure/Google.
- Real-time transcription and diarization experiments.
- Telephony voice-agent examples.

## Initial evaluation path

1. Inspect repo structure and docs/index metadata.
2. Shortlist examples most relevant to Moh's current interests:
   - Real-time voice agents.
   - Telephony / WhatsApp / Telegram adjacent workflows.
   - Meeting/call transcription and summarization.
   - Speaker diarization / speaker focus.
3. Check prerequisites and credential needs.
4. If a safe API key is available, run one tiny smoke test.
5. Decide whether to:
   - keep as reference,
   - write a reusable Hermes skill,
   - build a voice pipeline spike,
   - or compare against alternative providers first.

## Security notes

- Do not commit `.env` files or Speechmatics API keys.
- Prefer environment variables or secret manager entries.
- If examples clone/copy `.env.example`, verify `.gitignore` protects `.env`.
- Do not run telephony examples against real phone numbers without explicit user approval.

## Done means

A future agent can pick this up and produce an evidence-backed recommendation with example shortlist, implementation path, and any smoke-test results.
