import random
import string

def generate_id(length: int = 8) -> str:
    """生成随机ID
    
    Args:
        length: ID长度，默认8位
        
    Returns:
        str: 随机生成的ID
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))