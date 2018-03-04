import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../etc/"))
import dartsense_config

SESSION_SECRET = dartsense_config.SESSION_SECRET or ""

