def format_response(response_model):
    """
    Decorator to format the response of a FastAPI endpoint using a specified Pydantic model.
    
    This decorator modifies the response of the decorated function to ensure that it conforms
    to the structure defined by the provided Pydantic model. It handles serialization and
    validation of the response data.

    Parameters:
        response_model (Pydantic model): The Pydantic model that defines the expected structure of the response.

    Returns:
        Callable: The wrapped function with formatted response.
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            response = await func(*args, **kwargs)
            return response_model(**response)
        return wrapper
    return decorator
    