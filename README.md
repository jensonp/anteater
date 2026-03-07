# Anteater

Monitors UCI COMPSCI 175 (Spring 2026) for waitlist openings. When sections B, B1, or B2 (codes 34330, 34331, 34332) transition from n/a to a numeric waitlist, sends an email via [Resend](https://resend.com).

## Setup

1. **Install dependencies**
   ```bash
   pip install requests
   ```

2. **Create `.env`** in this directory:
   ```
   RESEND_API_KEY=re_your_api_key_here
   RESEND_EMAIL_TO=your@email.com
   ```

3. **Get Resend credentials**
   - Sign up at [resend.com](https://resend.com)
   - Create an API key in the dashboard
   - Free tier: `onboarding@resend.dev` only sends to your Resend account email. To send to other addresses, [verify a domain](https://resend.com/domains).

## Usage

```bash
python anteater.py          # Poll every 60 seconds, email when WL opens
python anteater.py --once   # Run once, no polling
```

## Output

Prints Max, Enr, WL, and Status for each section. Sorts by section (A, A1, A2, B, B1, B2).
