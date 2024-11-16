from functools import wraps
from fastapi import HTTPException
from app import logger

def try_catch_decorator():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Failed to execute operation: {str(e)}")
                if isinstance(e, HTTPException):
                    raise e
                else:
                    raise HTTPException(status_code=400, detail=str(e))
        return wrapper
    return decorator