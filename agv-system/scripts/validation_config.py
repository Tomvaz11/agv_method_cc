#!/usr/bin/env python3
"""
Validation Config Script - Wrapper para sistema de configuração de validação
Gerencia profiles e configurações do sistema de validação
"""

import sys
import os
from pathlib import Path

# Adicionar src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agv_system.validation_config import main

if __name__ == "__main__":
    main()