from fastapi.security import OAuth2PasswordBearer

oauth = OAuth2PasswordBearer(tokenUrl="token")