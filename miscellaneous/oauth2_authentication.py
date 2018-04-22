from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication,
                               PERMISSIONS)
import sys

if __name__ == '__main__':

    # id_Telepy = '78ddrft9tucb2h'
    # secret_id_Telepy = 'yvbO1aCKleNAmPXo'

    # id_Juan = '77ptq4iasj89wa'
    # secret_id_Juan = 'XB2vH79xARyCuLmJ'

    # id_Telepy_2 = '78942etf4507oi'
    # secret_id_Telepy_2 = 'qqH69nZ28paVFyIR'

    # id_Telepy_3 = '78dx543yss0s98'
    # secret_id_Telepy_3 = 'HFv5I0I1UOSUiIj6'    
    
    CLIENT_ID = '78ddrft9tucb2h'
    CLIENT_SECRET = 'yvbO1aCKleNAmPXo'
    RETURN_URL = 'http://localhost:8080/code/'

    authentication = LinkedInAuthentication(
                        CLIENT_ID,
                        CLIENT_SECRET,
                        RETURN_URL,
                        permissions=['r_basicprofile']
                    )

    # Note: edit permissions according to what you defined in the linkedin
    # developer console.

    # Optionally one can send custom "state" value that will be returned from
    # OAuth server It can be used to track your user state or something else
    # (it's up to you) Be aware that this value is sent to OAuth server AS IS -
    # make sure to encode or hash it
    #authorization.state = '453b144b400beef98d50a1bd34be8e71'

    print(authentication.authorization_url)
    application = LinkedInApplication(authentication)
