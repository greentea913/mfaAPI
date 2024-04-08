from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import base64
from pyotp import TOTP
import secrets
app = FastAPI()

def generate_secure_secret_key() -> str:
    # Generate a secure random byte sequence of a suitable length for TOTP
    random_bytes = secrets.token_bytes(20)  # 160 bits is a common length for TOTP keys
    
    # Encode the random bytes to base32
    secret_key = base64.b32encode(random_bytes).decode('utf-8').rstrip('=')
    
    return secret_key

@app.post("/v1/generateToken/")
async def generate_otp(request: Request):
    # Parse JSON body
    body = await request.json()
    username = body.get("username")
    application_name = body.get("application_name")
    
    if not username or not application_name:
        raise HTTPException(status_code=400, detail="Missing username or application name")

    # Generate secret key
    secret_key = generate_secure_secret_key()

    # Create a TOTP object
    totp = TOTP(secret_key)
    
    # Generate the OTP URI
    otp_uri = totp.provisioning_uri(name=username, issuer_name=application_name)

    # Return the OTP URI
    return JSONResponse(content={"otp_uri": otp_uri, "secret_key": secret_key})


@app.post("/v1/verifyOTP/")
async def verify_otp(request: Request):
    # Parse JSON body
    body = await request.json()
    secret_key = body.get("secret_key")
    method = body.get("method")
    otp = body.get("otp")

    if not secret_key or not otp:
        raise HTTPException(status_code=400, detail="Missing secret key or OTP")

    # Create a TOTP object
    if method == "email":
        valid_time = 10
    else:
        valid_time = 1
    totp = TOTP(secret_key)
    
    # Verify the OTP
    if totp.verify(otp, valid_window=valid_time):
        return JSONResponse(content={"valid": True})
    else:
        return JSONResponse(content={"valid": False})
    
@app.post("/v1/generateOTP/")
async def generate_otp(request: Request):
    body = await request.json()
    secret_key = body.get("secret_key")
    # The secret key (token) which is usually provided as a Base32 encoded string
    if not secret_key:
        raise HTTPException(status_code=400, detail="Missing secret key")
    # Create a TOTP object
    totp = TOTP(secret_key)

    # Generate a current OTP
    current_otp = totp.now()

    return JSONResponse(content={"otp": current_otp})

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8080)