import bcrypt

def hash_password(password: str) -> str:
    """对密码进行哈希处理"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, password_hash: str) -> bool:
    """验证密码"""
    return bcrypt.checkpw(password.encode(), password_hash.encode()) 