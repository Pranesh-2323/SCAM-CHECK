"""Rule-based red-flag engine (explainable, offline, no data stored)."""
import re

# (id, weight, regex) - English + Hindi + Tamil keywords
RULES = [
    ("guaranteed", 3, r"guarantee|assured\s+return|risk[- ]?free|100%\s*(profit|return)|double (your )?money|\d+\s*%\s*(daily|weekly|per day|per week)|गारंटी|दोगुना|உத்தரவாத|இரட்டிப்பு"),
    ("urgency", 2, r"limited (seats|slots|time)|hurry|today only|last chance|act now|join now|only \d+ (seats|slots)|जल्दी|இன்றே"),
    ("group", 2, r"\bvip\b|premium (group|tips|channel)|t\.me/|chat\.whatsapp\.com|telegram\.me|join (our|my) (whatsapp|telegram)"),
    ("payment", 3, r"[\w.\-]{2,}@(ok\w+|ybl|paytm|upi|axl|ibl|apl|sbi|hdfcbank|icici)\b|registration fee|processing fee|send money|transfer .{0,20}(account|upi)|pay .{0,15}upi"),
    ("authority", 2, r"sebi[- ]?(registered|approved|certified|reg)|nse[/ ]bse approved|rbi approved"),
    ("tips", 2, r"sure[- ]?shot|jackpot|multibagger|insider|operator|stock tip|pre[- ]?ipo|target\s*\d+"),
    ("app", 2, r"\.apk\b|download (our|the|this) (trading )?app|bit\.ly|tinyurl"),
    ("otp", 3, r"\botp\b|\bcvv\b|share .{0,10}(pin|password)|aadhaar|pan (card|number)"),
    ("crypto", 1, r"crypto|forex|binary option|usdt|bitcoin"),
]

def mask(text: str) -> str:
    """Remove phone numbers / UPI IDs / emails before any text leaves the device."""
    text = re.sub(r"(\+91[- ]?)?\b[6-9]\d{9}\b", "[PHONE]", text)
    return re.sub(r"[\w.\-]{2,}@[\w.\-]{2,}", "[ID]", text)

def analyse(text: str):
    """Returns (level, score, [flag ids]). level: none/low/medium/high."""
    hits = [(i, w) for i, w, p in RULES if re.search(p, text, re.I)]
    score = sum(w for _, w in hits)
    level = "high" if score >= 6 else "medium" if score >= 3 else "low" if score >= 1 else "none"
    return level, score, [i for i, _ in hits]
