"""
Example: Discover and run tests in each module.
"""
from .fixtures import bigprint, errors
from . import test_utensils

failed = dict()
failed.update(errors(test_utensils))
bigprint(**failed)
print(f"{len(failed)} FAILURES" if failed else "OK")
