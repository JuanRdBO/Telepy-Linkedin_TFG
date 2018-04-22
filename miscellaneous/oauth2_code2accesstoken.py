from linkedin import linkedin
import sys

CLIENT_ID = '78ddrft9tucb2h'
CLIENT_SECRET = 'yvbO1aCKleNAmPXo'

RETURN_URL = 'http://localhost:8080/code/'

authentication = linkedin.LinkedInAuthentication(
                    CLIENT_ID,
                    CLIENT_SECRET,
                    RETURN_URL,
                    linkedin.PERMISSIONS.enums.values()
                )

# Note: edit permissions according to what you defined in the linkedin
# developer console.

authentication.authorization_code = 'AQSVxA4y6vRvvSA1n6GK8LjtAQsYWcWGtEBuE_fS78dkT0Xrk9uEwwmAiJpoVgKjYdqYjGPS4aXHPa4eo5Boyh1wRrq994-FOe1ausfmSDkkUbmW0FMgSudmFqffHVC6ky8dyUMRRG7ZT9J5fTy3AntuZIQaTA'
result = authentication.get_access_token()

print("Access Token:", result.access_token)
print("Expires in (seconds):", result.expires_in)
