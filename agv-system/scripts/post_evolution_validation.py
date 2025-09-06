#!/usr/bin/env python3
"""
Wrapper script para post-evolution validation hook
Permite execução via linha de comando do sistema de validação pós-evolução
"""

import sys
from pathlib import Path

# Adicionar o diretório src ao Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agv_system.post_evolution_validation import main

if __name__ == "__main__":
    main()