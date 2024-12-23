import pyotp

otp_secret = "MFSG22LOGEZDGNBVGY3TQOI="
 # The OTP secret for admin
totp = pyotp.TOTP(otp_secret)
print("Generated OTP:", totp.now())
