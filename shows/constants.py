CAPTCHA_IN_URL = 'http://2captcha.com/in.php'
CAPTCHA_RESULT_URL = 'http://2captcha.com/res.php'

"""
API Limit Constants

https://2captcha.com/2captcha-api#limits

- If server returns ERROR_NO_SLOT_AVAILABLE make a 5 seconds timeout before
  sending next request.
- If captcha is not solved yet - retry to get the answer after 5 seconds.
- After uploading a captcha wait a least 5 seconds (10-20 for recaptcha)
  and only then try to get the answer.
"""

NO_SLOT_AVAILABLE_RESPONSE = 'ERROR_NO_SLOT_AVAILABLE'
NO_SLOT_AVAILABLE_RETRY_DELAY = 5
G_RECAPTCHA_RESPONSE_RETRY_DELAY = 5
RECAPTCHA_REQUEST_DELAY = 20

GOOGLE_CAPTCHA_SITE_KEY = '6LeIhQ4TAAAAACUkR1rzWeVk63ko-sACUlB7i932'
