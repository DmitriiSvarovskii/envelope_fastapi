from fastapi.security import APIKeyHeader
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

apikey_scheme = APIKeyHeader(name="Authorization")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
