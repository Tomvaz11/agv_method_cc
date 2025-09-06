#!/usr/bin/env python3
"""
Post-Scaffold Validation Script - Wrapper para novo sistema de validação modular
Executa automaticamente após scaffold usando o novo ValidatorGenerator v3.0
"""

import sys
import os
from pathlib import Path

# Adicionar src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agv_system.post_scaffold_validation import main

if __name__ == "__main__":
    main()