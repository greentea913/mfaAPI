You can use Google Cloud Run to deploy this simple MFA API as docker container.  
POST the application name and username to /v1/generateToken/ to generate token.  
GET the vaild states of OTP, by providing the secret key and the OTP, if method = "email" OTP vaild window = 5mins (10 loop) using /v1/verifyOTP/  
GET the OTP for email user, by providing the secret key use /v1/generateOTP/  
Use uvicorn main:app tp run
