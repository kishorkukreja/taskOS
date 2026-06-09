# Speechmatics Academy Voice AI Examples

Status: backlog

**Status:** ready
**Priority:** medium
**Created:** 2026-06-09
**Source:** https://github.com/speechmatics/speechmatics-academy

## What we are trying to do
Evaluate Speechmatics Academy as a practical resource for building speech/voice AI workflows: ASR/STT, real-time transcription, voice agents, TTS, diarization, telephony, and industry-specific examples.

## Why it matters
Speechmatics Academy is a working-examples repository rather than a marketing page. It may provide copy-paste-ready patterns for voice AI agents and speech pipelines, including LiveKit, Pipecat, Twilio, VAPI, healthcare dictation, call analytics, captioning, multilingual transcription, smart turn detection, and speaker identification/focus.

This is relevant to future Hermes/Self-OS voice workflows and to any product demo or agent workflow that needs robust speech input/output, transcription, diarization, or telephony integration.

## Current state
The repository presents itself as a comprehensive collection of examples, integrations, migration guides, and templates for Speechmatics SDK packages:

- `speechmatics-batch` — async batch transcription.
- `speechmatics-rt` — real-time WebSocket streaming transcription.
- `speechmatics-voice` — voice agent SDK with conversation management.
- `speechmatics-tts` — text-to-speech.

Notable examples/categories to inspect:

- Basics: hello world, batch vs real-time, configuration, TTS, channel diarization, audio intelligence, multilingual/translation, turn detection, speaker ID/focus, Voice API explorer.
- Integrations: LiveKit simple voice assistant, LiveKit + Twilio telephony, Pipecat voice bot/web bot, Twilio outbound dialer, VAPI assistant, Tambourine healthcare dictation.
- Use cases: medical transcription, video captioning, call center analytics, AI receptionist/calendar booking, medical assistant, medical microbatching, alphanumerics form filler.
- Migration guides: Deepgram available; AssemblyAI, Google Cloud Speech, AWS Transcribe, Azure Speech listed as coming soon.

## Desired outcome
A short operator-grade evaluation of whether Speechmatics Academy is worth adopting as a reference/workflow source, and which 2–3 examples are worth cloning or adapting first.

## Constraints
- Do not hardcode or commit Speechmatics API keys.
- Treat `.env` files and browser/session tokens as secrets; only `.env.example` should be committed.
- Prefer local smoke tests only if a valid API key is already available or the user explicitly provides one.
- Keep any product/demo artifacts outside Self-OS unless the user explicitly asks otherwise.
- Compare against current alternatives only if useful: Deepgram, AssemblyAI, OpenAI Whisper/Realtime, Azure Speech, Google Speech, ElevenLabs/Twilio/LiveKit stacks.

## Acceptance criteria
- [ ] Inspect repository structure and identify the highest-value examples for Moh's interests.
- [ ] Summarize the SDK packages and which use cases they map to.
- [ ] Evaluate voice-agent examples: LiveKit, Pipecat, Twilio, VAPI, turn detection, speaker ID/focus.
- [ ] Identify any examples relevant to Hermes voice/Telegram/WhatsApp workflows.
- [ ] Identify prerequisites: API key, Python version, package installs, audio assets, telephony accounts.
- [ ] Note security/secrets handling and deployment considerations.
- [ ] Recommend 2–3 next actions: clone/test an example, write a Hermes skill, or park as reference.
- [ ] If testing is feasible, run one minimal example with safe credentials handling and record the result.

## Open questions
- Do we have or want a Speechmatics API key for live tests?
- Which target matters first: transcription, realtime voice agents, TTS, telephony, or healthcare/call-center workflows?
- Should the output become a reusable Hermes skill, a voice pipeline spike, or just a curated reference note?
- Should this be compared with existing speech stack options before deciding?

## Future documents to create
- [ ] docs/idea.md
- [ ] docs/evaluation.md
- [ ] docs/example-shortlist.md
- [ ] docs/smoke-test-log.md
