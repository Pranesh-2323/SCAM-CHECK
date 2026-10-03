# Scam Check - Investor Fraud Warning Aid (SANGYAN, Track A)

Paste, speak or upload a screenshot of a suspicious investment message. Get warning signs, a risk level
and next steps in English / Tamil / Hindi, with voice read-out.

## How it works
1. `rules.py` - explainable rule engine (regex, weighted) detects 9 scam patterns.
2. Optional LLM (Claude) writes a short plain-language explanation - only if `ANTHROPIC_API_KEY` is set.
   Phone numbers, UPI IDs and emails are masked first.
3. Browser Web Speech API for voice input/output. Tesseract OCR for screenshots.

## Privacy and guardrails
- Nothing is stored or logged. No OTP/SMS access.
- No stock tips, predictions, broker promotion or monetisation.
- Never says "safe"; always shows uncertainty and points to SEBI SCORES, cybercrime.gov.in, 1930.

## Run
pip install -r requirements.txt
streamlit run app.py   (optional: export ANTHROPIC_API_KEY=...)

## Third-party components
Streamlit, Tesseract OCR, Pillow, Anthropic API (optional), browser Web Speech API.
