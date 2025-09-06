#!/usr/bin/env python3
"""
Post-UAT Generation Validation Hook v1.0
Hook automático executado após geração de cenários UAT para validação de qualidade.
"""

import sys
import os
import re
from pathlib import Path

def main():
    """Hook principal executado após geração de cenários UAT"""
    # Configurar encoding para Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
        
    print("\n" + "="*60)
    print("HOOK: VALIDACAO AUTOMATICA POS-UAT")  
    print("="*60)
    
    # Procurar pelos arquivos de UAT gerados
    try:
        import glob
        uat_files = glob.glob("UAT_*.md")
        if not uat_files:
            print("ERRO: Nenhum arquivo de UAT encontrado (UAT_*.md)")
            return False
            
        latest_uat_file = max(uat_files, key=lambda f: Path(f).stat().st_mtime)
        print(f"Validando arquivo UAT: {latest_uat_file}")
        
        # Validar estrutura dos cenários UAT
        validation_results = validate_uat_structure(latest_uat_file)
        
        # Mostrar resultados
        print_validation_results(validation_results)
        
        # Verificar se passou
        total_checks = validation_results['total_checks']
        passed_checks = validation_results['passed_checks']
        score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        print(f"\n📊 Score de Qualidade UAT: {score:.1f}%")
        
        if score >= 80:
            print("\nHOOK RESULTADO: CENARIOS UAT APROVADOS")
            print("Cenários UAT gerados com qualidade adequada.")
            return True
        else:
            print("\nHOOK RESULTADO: CENARIOS UAT REJEITADOS")
            print("Melhorar qualidade dos cenários antes de usar.")
            return False
            
    except Exception as e:
        print(f"\nERRO no hook de validação: {e}")
        return False

def validate_uat_structure(file_path):
    """Valida a estrutura e qualidade dos cenários UAT"""
    results = {
        'total_checks': 0,
        'passed_checks': 0,
        'scenarios_found': 0,
        'issues': []
    }
    
    try:
        content = Path(file_path).read_text(encoding='utf-8')
        
        # 1. Verificar se há cenários (padrão UAT_XXX_XXX)
        results['total_checks'] += 1
        scenario_pattern = r'\*\*ID do Cenário:\*\*\s+UAT_\w+_\d+'
        scenarios = re.findall(scenario_pattern, content)
        results['scenarios_found'] = len(scenarios)
        
        if results['scenarios_found'] >= 4:  # Mínimo de cenários
            results['passed_checks'] += 1
            print(f"  ✓ Encontrados {results['scenarios_found']} cenários UAT")
        else:
            results['issues'].append(f"Poucos cenários encontrados: {results['scenarios_found']} (mínimo: 4)")
            print(f"  ✗ Poucos cenários: {results['scenarios_found']} (mínimo: 4)")
        
        # 2. Verificar estrutura padronizada dos cenários
        required_fields = [
            'ID do Cenário',
            'Título do Cenário',
            'Fluxo Testado',
            'Componentes do Blueprint Envolvidos',
            'Pré-condições',
            'Passos para Execução',
            'Resultado Esperado',
            'Critério de Passagem'
        ]
        
        for field in required_fields:
            results['total_checks'] += 1
            pattern = rf'\*\*{re.escape(field)}:\*\*'
            if re.search(pattern, content):
                results['passed_checks'] += 1
                print(f"  ✓ Campo encontrado: {field}")
            else:
                results['issues'].append(f"Campo obrigatório ausente: {field}")
                print(f"  ✗ Campo ausente: {field}")
        
        # 3. Verificar qualidade dos passos (numeração)
        results['total_checks'] += 1
        step_pattern = r'1\.\s+\w+.*\n2\.\s+\w+'  # Pelo menos 2 passos numerados
        if re.search(step_pattern, content, re.MULTILINE):
            results['passed_checks'] += 1
            print("  ✓ Passos numerados encontrados")
        else:
            results['issues'].append("Passos de execução não seguem numeração adequada")
            print("  ✗ Passos não numerados adequadamente")
        
        # 4. Verificar menções ao Blueprint
        results['total_checks'] += 1
        if 'Blueprint' in content or 'blueprint' in content:
            results['passed_checks'] += 1
            print("  ✓ Referência ao Blueprint encontrada")
        else:
            results['issues'].append("Nenhuma referência ao Blueprint encontrada")
            print("  ✗ Sem referência ao Blueprint")
            
    except Exception as e:
        results['issues'].append(f"Erro ao analisar arquivo: {e}")
        
    return results

def print_validation_results(results):
    """Imprime resumo dos resultados de validação"""
    print(f"\n📋 Resumo da Validação UAT:")
    print(f"   Cenários encontrados: {results['scenarios_found']}")
    print(f"   Verificações totais: {results['total_checks']}")
    print(f"   Verificações aprovadas: {results['passed_checks']}")
    
    if results['issues']:
        print(f"\n⚠️  Problemas encontrados:")
        for issue in results['issues']:
            print(f"   - {issue}")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)