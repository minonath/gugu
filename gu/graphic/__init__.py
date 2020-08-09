"""
┼
┌──────┬─────────┬───────────┐
│ base │  object │           │
└──────┴─────────┴───────────┘

│                   │    program    │
├──────────┼────────┼───────────────┤
│  texture │ buffer │ shader member │
├──────────┴────────┴───────────────┤
│                object             │
└───────────────────────────────────┘
"""

from .object import gl_objects
from .texture import Texture
from .buffer import Buffer
from .program import program_manager, load_all_program
