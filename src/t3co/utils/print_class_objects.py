
from typing import List


def obj_to_string(obj, extra='    '):
    if isinstance(obj, list) or isinstance(obj, List):  # Check if the object is a list
        return '[\n' + ',\n'.join(
            extra + obj_to_string(item, extra + '    ') if hasattr(item, '__dict__') else extra + str(item)
            for item in obj
        ) + '\n' + extra[:-4] + ']'  # Match the indentation level
    
    elif hasattr(obj, '__dict__'):  # Check if the object has __dict__ attribute
        return str(obj.__class__) + '\n' + '\n'.join(
        (extra + (str(item) + ' = ' +
                  obj_to_string(obj.__dict__[item], extra + '    ') ))
                  for item in sorted(obj.__dict__))
    else:  # For other data types
        return str(obj)