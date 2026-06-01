import sys
from pathlib import Path

_PACT_ROOT = Path(__file__).resolve().parent
if str(_PACT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PACT_ROOT))
