#!/usr/bin/env python3
"""
Post-Integration Testing Validation Hook v1.0
Hook automático executado após criação de testes de integração para validação especializada.
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """Hook principal executado após criação de testes de integração"""
    # Configurar encoding para Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
        
    print("\n" + "="*60)
    print("HOOK: VALIDACAO AUTOMATICA POS-TESTES DE INTEGRACAO")  
    print("="*60)
    
    # Executar validação usando o sistema ValidatorGenerator (tipo integration)
    try:
        # Para pós-testes de integração, usar integration com fase T1 como padrão
        blueprint_path = "BLUEPRINT_ARQUITETURAL.md"
        gen_result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent.parent.parent / "scripts" / "agv-validate"),
            blueprint_path,
            "integration",
            "--integration-phase", "T1"  # Usar T1 como base para validação de testes
        ], capture_output=True, text=True, cwd=Path.cwd())
        
        if gen_result.returncode != 0:
            print(f"ERRO na geração do validador:")
            print(f"STDOUT: {gen_result.stdout}")
            print(f"STDERR: {gen_result.stderr}")
            return False
        else:
            print("Validador gerado com sucesso!")
            print(f"Output: {gen_result.stdout}")
            
        # Executar o validador gerado diretamente
        try:
            import glob
            validator_files = glob.glob("agv-outputs/validadores/validate_t1_*.py")
            if validator_files:
                latest_validator = max(validator_files, key=lambda f: Path(f).stat().st_mtime)
                print(f"Executando validador: {latest_validator}")
            else:
                print("ERRO: Nenhum validador de integração gerado encontrado")
                return False
        except Exception as e:
            print(f"ERRO ao localizar validador: {e}")
            return False
            
        # Executar o validador gerado diretamente
        result = subprocess.run([
            sys.executable, 
            latest_validator
        ], capture_output=True, text=True, encoding='utf-8', errors='ignore', cwd=Path.cwd())
        
        # Mostrar output da validação
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
            
        # Verificar se passou
        if result.returncode == 0:
            print("\nHOOK RESULTADO: TESTES DE INTEGRACAO APROVADOS")
            print("Testes de integração implementados com sucesso e conforme Blueprint.")
            return True
        else:
            print("\nHOOK RESULTADO: TESTES DE INTEGRACAO REJEITADOS")
            print("Corrigir problemas nos testes antes de prosseguir.")
            return False
            
    except Exception as e:
        print(f"\nERRO no hook de validação: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)