import logging
from functools import wraps
import inspect

###########################
#### DEVELOPER OPTIONS ####

# Para que te imprima en consola por donde va pasando el flujo de ejecución de la guía.
USE_DEBUG = False
# Si es True, usará el sistema anterior con un modal operator.
# Si es False, usará el nuevo sistema de gizmo.
USE_MODAL = False

###########################

def DEBUG(message: str or bool):
    if not USE_DEBUG:
        return
    print(message)

# At the beginning of every .py file in the project
def logger(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        log = logging.getLogger(fn.__name__)
        log.info('About to run %s' % fn.__name__)

        out = fn(*args, **kwargs)

        log.info('Done running %s' % fn.__name__)
        # Return the return value
        return out
    return wrapper


def conditional_decorator(dec, condition):
    def decorator(func):
        if not condition:
            # Return the function unchanged, not decorated.
            return func
        return dec(func)
    return decorator


def debug(dec=logger, condition=USE_DEBUG):
    def decorator(func):
        if not condition:
            # Return the function unchanged, not decorated.
            return func
        return dec(func)
    return decorator
