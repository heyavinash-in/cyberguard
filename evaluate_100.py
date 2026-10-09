import requests

table = """
|   1 | `https://google.com`                                                                                          | SAFE        |
|   2 | `https://www.google.com`                                                                                      | SAFE        |
|   3 | `https://github.com`                                                                                          | SAFE        |
|   4 | `https://github.com/login`                                                                                    | SAFE        |
|   5 | `https://www.microsoft.com`                                                                                   | SAFE        |
|   6 | `https://amazon.in`                                                                                           | SAFE        |
|   7 | `https://www.amazon.in/gp/help/customer/display.html`                                                         | SAFE        |
|   8 | `https://netflix.com`                                                                                         | SAFE        |
|   9 | `https://accounts.google.com`                                                                                 | SAFE        |
|  10 | `https://login.microsoftonline.com`                                                                           | SAFE        |
|  11 | `https://support.google.com/accounts`                                                                         | SAFE        |
|  12 | `https://developer.mozilla.org/en-US/docs/Web`                                                                | SAFE        |
|  13 | `https://stackoverflow.com/questions`                                                                         | SAFE        |
|  14 | `https://www.apple.com/in/`                                                                                   | SAFE        |
|  15 | `https://www.linkedin.com/login`                                                                              | SAFE        |
|  16 | `https://www.instagram.com/accounts/login/`                                                                   | SAFE        |
|  17 | `https://www.paypal.com/signin`                                                                               | SAFE        |
|  18 | `https://www.adobe.com/account.html`                                                                          | SAFE        |
|  19 | `https://cloudflare.com/login`                                                                                | SAFE        |
|  20 | `https://www.nasa.gov/`                                                                                       | SAFE        |
|  21 | `https://paypal-security-check.example.com`                                                                   | CRITICAL    |
|  22 | `https://paypal-login-verification.example.net`                                                               | CRITICAL    |
|  23 | `https://microsoft-account-security.example.org`                                                              | HIGH        |
|  24 | `https://google-login-confirm.example.com`                                                                    | HIGH        |
|  25 | `https://amazon-verification.example.net`                                                                     | HIGH        |
|  26 | `https://apple-id-verification.example.org`                                                                   | HIGH        |
|  27 | `https://github-security-alert.example.com`                                                                   | HIGH        |
|  28 | `https://instagram-account-verify.example.net`                                                                | HIGH        |
|  29 | `https://netflix-payment-update.example.org`                                                                  | HIGH        |
|  30 | `https://linkedin-security-check.example.com`                                                                 | HIGH        |
|  31 | `https://paypa1.com`                                                                                          | CRITICAL    |
|  32 | `https://paypaI.com`                                                                                          | CRITICAL    |
|  33 | `https://micros0ft.com`                                                                                       | CRITICAL    |
|  34 | `https://g00gle.com`                                                                                          | CRITICAL    |
|  35 | `https://arnazon.com`                                                                                         | CRITICAL    |
|  36 | `https://faceb00k.com`                                                                                        | CRITICAL    |
|  37 | `https://netf1ix.com`                                                                                         | CRITICAL    |
|  38 | `https://app1e.com`                                                                                           | HIGH        |
|  39 | `https://linkedln.com`                                                                                        | HIGH        |
|  40 | `https://pay-pal.example.com`                                                                                 | HIGH        |
|  41 | `http://192.168.1.10/login`                                                                                   | MEDIUM/HIGH |
|  42 | `http://185.10.20.30/verify`                                                                                  | HIGH        |
|  43 | `https://203.0.113.10/account/login`                                                                          | HIGH        |
|  44 | `http://198.51.100.20/security/update`                                                                        | HIGH        |
|  45 | `https://203.0.113.50/download.exe`                                                                           | HIGH        |
|  46 | `https://paypal.login.verify.example.com`                                                                     | CRITICAL    |
|  47 | `https://google.account.verify.example.net`                                                                   | HIGH        |
|  48 | `https://microsoft.security.account.example.org`                                                              | HIGH        |
|  49 | `https://amazon.customer.support.example.com`                                                                 | HIGH        |
|  50 | `https://apple.id.confirmation.example.net`                                                                   | HIGH        |
|  51 | `https://account.security.login.verify.example.com`                                                           | HIGH        |
|  52 | `https://secure.login.account.verify.example.net`                                                             | HIGH        |
|  53 | `https://update.security.authentication.example.org`                                                          | MEDIUM/HIGH |
|  54 | `https://customer-support-billing.example.com`                                                                | MEDIUM      |
|  55 | `https://help-center.example.net/account`                                                                     | MEDIUM      |
|  56 | `https://example.com/login`                                                                                   | LOW/MEDIUM  |
|  57 | `https://example.com/security`                                                                                | LOW/MEDIUM  |
|  58 | `https://example.com/account/verify`                                                                          | LOW/MEDIUM  |
|  59 | `https://example.com/password/reset`                                                                          | LOW/MEDIUM  |
|  60 | `https://example.com/payment/confirm`                                                                         | LOW/MEDIUM  |
|  61 | `https://example.com/download/update.exe`                                                                     | MEDIUM      |
|  62 | `http://example.com/login`                                                                                    | LOW/MEDIUM  |
|  63 | `http://example.com/account/verify`                                                                           | LOW/MEDIUM  |
|  64 | `https://example.com/?redirect=https%3A%2F%2Fevil.example`                                                    | MEDIUM/HIGH |
|  65 | `https://example.com/?url=https%3A%2F%2Fmalicious.example`                                                    | MEDIUM/HIGH |
|  66 | `https://example.com/?next=https%3A%2F%2Fevil.example/login`                                                  | MEDIUM/HIGH |
|  67 | `https://example.com/?continue=https%3A%2F%2Fevil.example`                                                    | MEDIUM/HIGH |
|  68 | `https://example.com/?destination=https%3A%2F%2Fevil.example`                                                 | MEDIUM/HIGH |
|  69 | `https://example.com/login?redirect=http%3A%2F%2Fevil.example`                                                | HIGH        |
|  70 | `https://example.com/verify?return=https%3A%2F%2Fevil.example`                                                | HIGH        |
|  71 | `https://xn--pple-43d.com/login`                                                                              | HIGH        |
|  72 | `https://xn--oogle-qmc.com/verify`                                                                            | HIGH        |
|  73 | `https://xn--microsft-abc.com/account`                                                                        | HIGH        |
|  74 | `https://xn--paypa1-xyz.com/login`                                                                            | HIGH        |
|  75 | `https://example.com/%6c%6f%67%69%6e`                                                                         | LOW/MEDIUM  |
|  76 | `https://example.com/%76%65%72%69%66%79`                                                                      | LOW/MEDIUM  |
|  77 | `https://example.com/login/%2e%2e/%2e%2e/account`                                                             | MEDIUM      |
|  78 | `https://example.com/%252e%252e/%252e%252e/login`                                                             | MEDIUM      |
|  79 | `https://example.com/login?token=9f8a7b6c5d4e3f2a1b0c`                                                        | LOW/MEDIUM  |
|  80 | `https://example.com/a8f91c7e6d5b4a392817/login`                                                              | LOW/MEDIUM  |
|  81 | `https://example.com/update.exe`                                                                              | MEDIUM      |
|  82 | `https://example.com/document.zip`                                                                            | LOW/MEDIUM  |
|  83 | `https://example.com/mobile/app.apk`                                                                          | MEDIUM      |
|  84 | `https://example.com/download/security-update.msi`                                                            | MEDIUM      |
|  85 | `https://paypal-security.example.com/login?verify=1&account=1`                                                | CRITICAL    |
|  86 | `https://google-security.example.net/account/login?verify=true`                                               | CRITICAL    |
|  87 | `https://microsoft-update.example.org/security/password`                                                      | CRITICAL    |
|  88 | `https://amazon-refund.example.com/payment/card`                                                              | HIGH        |
|  89 | `https://netflix-billing.example.net/payment/update`                                                          | HIGH        |
|  90 | `https://instagram-security.example.org/password/reset`                                                       | HIGH        |
|  91 | `https://user:password@example.com/login`                                                                     | MEDIUM      |
|  92 | `https://example.com:8080/login`                                                                              | LOW/MEDIUM  |
|  93 | `http://example.com:31337/admin`                                                                              | MEDIUM      |
|  94 | `https://example.com/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q/r/s/t`                                                 | LOW/MEDIUM  |
|  95 | `https://secure.example.com`                                                                                  | LOW         |
|  96 | `https://login.example.com`                                                                                   | LOW         |
|  97 | `https://security.example.com/account`                                                                        | LOW/MEDIUM  |
|  98 | `https://verify.example.com`                                                                                  | LOW/MEDIUM  |
|  99 | `https://example.com/?q=login+verify+security+account`                                                        | LOW/MEDIUM  |
| 100 | `https://paypal.login.security.verify.example.com/account/password/reset?redirect=https%3A%2F%2Fevil.example` | CRITICAL    |
"""

failures = []
passed = 0
total = 0

for line in table.strip().split('\n'):
    if not line.strip() or '|' not in line: continue
    parts = [p.strip() for p in line.split('|')]
    if len(parts) < 4: continue
    
    url_raw = parts[2].replace('`', '').strip()
    expected = parts[3].strip()

    if url_raw == 'Test URL' or '---' in url_raw:
        continue

    total += 1
    try:
        res = requests.post("http://127.0.0.1:8000/api/predict", json={"url": url_raw}, timeout=5)
        if res.status_code == 200:
            actual_severity = res.json()['risk']['severity']
            risk_score = res.json()['risk']['score']
        else:
            actual_severity = f"HTTP {res.status_code}"
            risk_score = 0
    except Exception as e:
        actual_severity = "ERROR"
        risk_score = 0

    expected_options = expected.split('/')
    if actual_severity not in expected_options:
        failures.append((url_raw, expected, actual_severity, risk_score))
    else:
        passed += 1

print(f"Total Tests: {total}")
print(f"Passed: {passed}")
print(f"Failed: {len(failures)}")
print("\n### Full Results Table\n")
print("| # | URL | Expected | Actual | Risk | Severity | Pass/Fail |")
print("| - | --- | -------- | -----: | ---: | -------- | --------- |")

i = 1
false_positives = 0
false_negatives = 0

for line in table.strip().split('\n'):
    if not line.strip() or '|' not in line: continue
    parts = [p.strip() for p in line.split('|')]
    if len(parts) < 4: continue
    
    url_raw = parts[2].replace('`', '').strip()
    expected = parts[3].strip()

    if url_raw == 'Test URL' or '---' in url_raw:
        continue

    try:
        res = requests.post("http://127.0.0.1:8000/api/predict", json={"url": url_raw}, timeout=5)
        if res.status_code == 200:
            actual_severity = res.json()['risk']['severity']
            risk_score = res.json()['risk']['score']
        else:
            actual_severity = f"HTTP {res.status_code}"
            risk_score = 0
    except Exception as e:
        actual_severity = "ERROR"
        risk_score = 0

    expected_options = expected.split('/')
    pass_fail = "Pass" if actual_severity in expected_options else "Fail"
    
    # Simple FP / FN logic
    is_expected_safe = "SAFE" in expected_options or "LOW" in expected_options
    is_actual_safe = actual_severity in ["SAFE", "LOW"]
    
    if pass_fail == "Fail":
        if is_expected_safe and not is_actual_safe:
            false_positives += 1
        elif not is_expected_safe and is_actual_safe:
            false_negatives += 1

    print(f"| {i} | `{url_raw}` | {expected} | {actual_severity} | {risk_score} | {actual_severity} | {pass_fail} |")
    i += 1

print("\n### Summary Statistics\n")
print(f"**Total tests:** {total}")
print(f"**Passed:** {passed}")
print(f"**Failed:** {len(failures)}")
print(f"**False positives:** {false_positives}")
print(f"**False negatives:** {false_negatives}")
