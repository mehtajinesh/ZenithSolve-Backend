import re
import math


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

def parse_complexity(complexity):
    """ Parse complexity string like O(n^2), O(log n), O(n!), O(2^n), etc. """
    complexity = complexity.replace(" ", "")
    # Handle n^k, log(n), n!, 2^n, etc.
    if re.match(r"O\(n\^\d+\)", complexity):
        _, exp = "n", int(re.search(r"\d+", complexity).group())
        return ("polynomial", exp)
    elif re.match(r"O\(log\(n\)\)", complexity):
        return ("logarithmic", 1)
    elif re.match(r"O\(nlog\(n\)\)", complexity):
        return ("linearithmic", 1)
    elif re.match(r"O\(n!\)", complexity):
        return ("factorial", math.factorial)
    elif re.match(r"O\(2\^n\)", complexity):
        return ("exponential", 2)
    elif re.match(r"O\(n\)", complexity):
        return ("linear", 1)
    elif re.match(r"O\(1\)", complexity):
        return ("constant", 0)
    else:
        raise ValueError("Invalid or unsupported complexity format")

def complexity_rank(complexity):
    """ Assign a rank to each complexity type for comparison purposes. """
    ranks = {
        "constant": 0,
        "logarithmic": 1,
        "linearithmic": 2,
        "linear": 3,
        "polynomial": 4,
        "exponential": 5,
        "factorial": 6
    }
    return ranks.get(complexity[0], float('inf'))

def get_better_complexity(c1, c2):
    """ Compare two complexities and return the better one. """
    try:
        if c1 == "NA" or c2 == "NA":
            return c1 if c1 != "NA" else c2
        if c1 == c2:
            return c1
        parsed1 = parse_complexity(c1)
        parsed2 = parse_complexity(c2)
        rank1 = complexity_rank(parsed1)
        rank2 = complexity_rank(parsed2)

        if rank1 < rank2:
            return c1
        elif rank1 > rank2:
            return c2
        else:
            return c1 if parsed1[1] <= parsed2[1] else c2
    except ValueError as e:
        return str(e)

def compare_approaches(time1, space1, time2, space2):
    """ Compare two approaches based on time and space complexity, prioritizing time. """
    better_time = get_better_complexity(time1, time2)
    if time1 == time2:
        better_space = get_better_complexity(space1, space2)
        return better_time, better_space
    return better_time, space1 if better_time == time1 else space2