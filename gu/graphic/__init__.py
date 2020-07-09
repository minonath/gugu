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

from .texture import Texture
from .buffer import Buffer
from .program import program_manager, load_all_program

from ..system import gu

gu.texture = Texture
gu.buffer = Buffer
gu.program = program_manager
