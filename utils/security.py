from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from models.users import User
from database import get_db
from sqlalchemy.orm import Session  
from fastapi import security


SECRET_KEY = "b5a2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6A7B8C9D0E"  # Replace with a strong secret key
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



oauth2_scheme = HTTPBearer()
 
def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):  # Add db dependency
    try:
        payload = jwt.decode(token.credentials,SECRET_KEY, algorithms=[ALGORITHM] )
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.email == user_email).first()  # Get user from DB
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user  # Return the user object
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    



def is_admin(user: User = Depends(verify_token)):
    print(user.role)
    if user.role != ("Admin" and "admin"):
        raise HTTPException(status_code=403, detail="not have permission to perform this action")
    return user



