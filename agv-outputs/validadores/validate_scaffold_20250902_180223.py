#!/usr/bin/env python3
"""
Validador especializado para scaffold completo (Alvo 0)
Gerado automaticamente pelo ValidatorGenerator v3.0 - Sistema Modular AGV
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ValidationIssue:
    """Representa um problema encontrado na validação."""
    file_path: str
    issue_type: str
    description: str
    expected: str
    actual: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW

@dataclass
class ValidationResults:
    """Resultados completos da validação."""
    total_checks: int
    passed_checks: int
    failed_checks: int
    issues: List[ValidationIssue]
    score: float
    categories: Dict[str, int]

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário para serialização JSON."""
        return {
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "issues": [asdict(issue) for issue in self.issues],
            "score": self.score,
            "categories": self.categories
        }


def validate_directory_structure():
    '''Valida estrutura completa de diretórios conforme Blueprint.'''
    import os
    from pathlib import Path
    
    issues = []
    required_paths = ['iabank/', 'iabank/.github/', 'iabank/.github/workflows/', 'iabank/.github/workflows/main.yml', 'iabank/backend/', 'iabank/backend/src/', 'iabank/backend/src/iabank/', 'iabank/backend/src/iabank/__init__.py', 'iabank/backend/src/iabank/asgi.py', 'iabank/backend/src/iabank/settings.py', 'iabank/backend/src/iabank/urls.py', 'iabank/backend/src/iabank/wsgi.py', 'iabank/backend/src/iabank/core/', 'iabank/backend/src/iabank/customers/', 'iabank/backend/src/iabank/customers/__init__.py', 'iabank/backend/src/iabank/customers/models.py', 'iabank/backend/src/iabank/customers/admin.py', 'iabank/backend/src/iabank/customers/apps.py', 'iabank/backend/src/iabank/customers/serializers.py', 'iabank/backend/src/iabank/customers/views.py', 'iabank/backend/src/iabank/customers/tests/', 'iabank/backend/src/iabank/customers/tests/__init__.py', 'iabank/backend/src/iabank/customers/tests/test_models.py', 'iabank/backend/src/iabank/customers/tests/test_views.py', 'iabank/backend/src/iabank/finance/', 'iabank/backend/src/iabank/operations/', 'iabank/backend/src/iabank/users/', 'iabank/backend/manage.py', 'iabank/backend/Dockerfile', 'iabank/backend/pyproject.toml', 'iabank/frontend/', 'iabank/frontend/public/', 'iabank/frontend/src/', 'iabank/frontend/Dockerfile', 'iabank/frontend/package.json', 'iabank/frontend/tsconfig.json', 'iabank/frontend/vite.config.ts', 'iabank/tests/', 'iabank/tests/integration/', 'iabank/tests/integration/__init__.py', 'iabank/tests/integration/test_full_loan_workflow.py', 'iabank/docker-compose.yml', 'iabank/.gitignore', 'iabank/.pre-commit-config.yaml', 'iabank/CHANGELOG.md', 'iabank/CONTRIBUTING.md', 'iabank/LICENSE', 'iabank/README.md']
    
    for required_path in required_paths:
        path = Path(required_path)
        
        if required_path.endswith('/'):
            # Diretório
            if not path.is_dir():
                issues.append(ValidationIssue(
                    file_path=str(path),
                    issue_type="missing_directory",
                    description=f"Diretório obrigatório não encontrado: " + required_path,
                    expected=f"Diretório " + required_path + " deve existir",
                    actual="Diretório não existe",
                    severity="HIGH"
                ))
        else:
            # Arquivo
            if not path.is_file():
                issues.append(ValidationIssue(
                    file_path=str(path),
                    issue_type="missing_file",
                    description=f"Arquivo obrigatório não encontrado: " + required_path,
                    expected=f"Arquivo " + required_path + " deve existir",
                    actual="Arquivo não existe",
                    severity="MEDIUM"
                ))
    
    return issues if issues else None


def validate_gitignore_content():
    '''Valida se .gitignore tem conteúdo EXATO do Blueprint (certeza absoluta).'''
    issues = []
    
    gitignore_paths = list(Path('.').rglob('**/.gitignore'))
    if not gitignore_paths:
        issues.append(ValidationIssue(
            file_path=".gitignore",
            issue_type="missing_gitignore_file",
            description="Arquivo .gitignore não encontrado",
            expected="Arquivo .gitignore deve existir na raiz",
            actual="Arquivo não existe",
            severity="CRITICAL"
        ))
        return issues
    
    gitignore_file = gitignore_paths[0]
    content = gitignore_file.read_text(encoding='utf-8', errors='ignore')
    
    # Conteúdo COMPLETO esperado do Blueprint (seção 8)
    expected_blueprint_sections = [
        # Byte-compiled / optimized / DLL files
        '__pycache__/', '*.py[cod]', '*$py.class', '*.so',
        
        # Distribution / packaging
        '.Python', 'build/', 'develop-eggs/', 'dist/', 'downloads/',
        'eggs/', '.eggs/', 'lib/', 'lib64/', 'parts/', 'sdist/',
        'var/', 'wheels/', 'share/python-wheels/', '*.egg-info/',
        '.installed.cfg', '*.egg', 'MANIFEST',
        
        # PyInstaller
        '*.manifest', '*.spec',
        
        # Installer logs  
        'pip-log.txt', 'pip-delete-this-directory.txt',
        
        # Unit test / coverage reports
        'htmlcov/', '.tox/', '.nox/', '.coverage', '.coverage.*',
        '.cache', 'nosetests.xml', 'coverage.xml', '*.cover',
        '*.py,cover', '.hypothesis/', '.pytest_cache/', 'cover/',
        
        # Translations
        '*.mo', '*.pot',
        
        # Django stuff
        '*.log', 'local_settings.py', 'db.sqlite3', 'db.sqlite3-journal',
        
        # Environments
        '.env', '.venv', 'env/', 'venv/', 'ENV/', 'env.bak/', 'venv.bak/',
        
        # IDE files
        '.idea/', '.vscode/', '*.swp', '*.swo',
        
        # Node.js
        'node_modules/', 'dist/', 'dist-ssr/', '*.local',
        'npm-debug.log*', 'yarn-debug.log*', 'yarn-error.log*', 'pnpm-debug.log*',
        
        # Docker
        'docker-compose.override.yml',
        
        # OS files
        '.DS_Store', 'Thumbs.db'
    ]
    
    # Validação RIGOROSA: cada seção deve estar presente
    missing_critical = []
    missing_optional = []
    
    critical_sections = [
        '__pycache__/', '*.py[cod]', 'node_modules/', 'dist/',
        '.env', '.venv', '.idea/', '.vscode/', 'db.sqlite3', '*.log'
    ]
    
    for section in expected_blueprint_sections:
        if section not in content:
            if section in critical_sections:
                missing_critical.append(section)
            else:
                missing_optional.append(section)
    
    # Reportar seções críticas ausentes
    for section in missing_critical:
        issues.append(ValidationIssue(
            file_path=str(gitignore_file),
            issue_type="missing_critical_gitignore_section",
            description=f"Seção CRÍTICA ausente no .gitignore: {section}",
            expected=f"Seção '{section}' é OBRIGATÓRIA conforme Blueprint seção 8",
            actual="Seção crítica não encontrada",
            severity="HIGH"
        ))
    
    # Reportar seções opcionais ausentes (para completude)
    if len(missing_optional) > 5:  # Muitas seções ausentes
        issues.append(ValidationIssue(
            file_path=str(gitignore_file),
            issue_type="incomplete_gitignore_content", 
            description=f"Gitignore incompleto: {len(missing_optional)} seções Blueprint ausentes",
            expected="Conteúdo completo do Blueprint seção 8 deve estar presente",
            actual=f"Faltam seções: {', '.join(missing_optional[:3])}...",
            severity="MEDIUM"
        ))
    
    return issues if issues else None

def validate_pyproject_content():
    '''Valida se pyproject.toml tem configurações específicas do Blueprint.'''
    issues = []
    
    pyproject_paths = list(Path('.').rglob('**/pyproject.toml'))
    # Filtrar arquivos do agv-system
    project_files = [f for f in pyproject_paths if 'agv-system' not in str(f)]
    
    if not project_files:
        issues.append(ValidationIssue(
            file_path="pyproject.toml",
            issue_type="missing_pyproject_file",
            description="Arquivo pyproject.toml não encontrado",
            expected="Arquivo pyproject.toml deve existir no backend",
            actual="Arquivo não existe",
            severity="HIGH"
        ))
        return issues
    
    pyproject_file = project_files[0]
    content = pyproject_file.read_text(encoding='utf-8', errors='ignore')
    
    # Configurações obrigatórias do Blueprint
    required_configs = [
        '[tool.ruff]',     # Linter configuration
        '[tool.black]',    # Formatter configuration  
        'line-length',     # Code style
        'django',          # Django dependency
        'djangorestframework', # DRF dependency
        'psycopg2-binary'  # PostgreSQL driver
    ]
    
    for config in required_configs:
        if config not in content:
            issues.append(ValidationIssue(
                file_path=str(pyproject_file),
                issue_type="missing_pyproject_config",
                description=f"Configuração obrigatória não encontrada: {config}",
                expected=f"Configuração '{config}' deve estar no pyproject.toml conforme Blueprint",
                actual="Configuração não encontrada",
                severity="MEDIUM"
            ))
    
    return issues if issues else None

def validate_precommit_config_content():
    '''Valida se .pre-commit-config.yaml tem configuração específica do Blueprint.'''
    issues = []
    
    precommit_paths = list(Path('.').rglob('**/.pre-commit-config.yaml'))
    if not precommit_paths:
        issues.append(ValidationIssue(
            file_path=".pre-commit-config.yaml",
            issue_type="missing_precommit_config",
            description="Arquivo .pre-commit-config.yaml não encontrado",
            expected="Arquivo deve existir na raiz conforme Blueprint",
            actual="Arquivo não existe",
            severity="MEDIUM"
        ))
        return issues
    
    precommit_file = precommit_paths[0]
    content = precommit_file.read_text(encoding='utf-8', errors='ignore')
    
    # Hooks obrigatórios do Blueprint
    required_hooks = [
        'pre-commit-hooks',  # Basic hooks
        'trailing-whitespace', 'end-of-file-fixer',  # File formatting
        'black',             # Python formatter
        'ruff'               # Python linter
    ]
    
    for hook in required_hooks:
        if hook not in content:
            issues.append(ValidationIssue(
                file_path=str(precommit_file),
                issue_type="missing_precommit_hook",
                description=f"Hook obrigatório não encontrado: {hook}",
                expected=f"Hook '{hook}' deve estar configurado conforme Blueprint",
                actual="Hook não encontrado",
                severity="MEDIUM"
            ))
    
    return issues if issues else None

def validate_env_example_file():
    '''Valida se .env.example existe conforme escopo scaffolder.'''
    issues = []
    
    env_example_paths = list(Path('.').rglob('**/.env.example'))
    if not env_example_paths:
        issues.append(ValidationIssue(
            file_path=".env.example",
            issue_type="missing_env_example",
            description="Arquivo .env.example não encontrado",
            expected="Template de variáveis de ambiente deve existir",
            actual="Arquivo não existe",
            severity="MEDIUM"
        ))
        return issues
    
    env_file = env_example_paths[0]
    content = env_file.read_text(encoding='utf-8', errors='ignore')
    
    # Variáveis básicas obrigatórias
    basic_vars = ['DEBUG', 'SECRET_KEY', 'DATABASE_URL']
    
    for var in basic_vars:
        if var not in content:
            issues.append(ValidationIssue(
                file_path=str(env_file),
                issue_type="missing_env_variable",
                description=f"Variável de ambiente obrigatória não encontrada: {var}",
                expected=f"Variável '{var}' deve estar no template",
                actual="Variável não encontrada",
                severity="LOW"
            ))
    
    return issues if issues else None


def validate_content_settings_py():
    '''Valida conteúdo específico de settings.py.'''
    issues = []
    
    file_paths = list(Path('.').rglob('**/settings.py'))
    if not file_paths:
        return ValidationIssue(
            file_path="settings.py",
            issue_type="missing_file",
            description="Arquivo settings.py não encontrado",
            expected="Arquivo deve existir",
            actual="Arquivo não existe",
            severity="HIGH"
        )
    
    for file_path_obj in file_paths:
        if file_path_obj.exists():
            file_path_str = str(file_path_obj)
            content = file_path_obj.read_text(encoding='utf-8', errors='ignore')
            
            # Verificar INSTALLED_APPS
            if 'INSTALLED_APPS' in content:
                for app in ['customers', 'operations', 'finance', 'core']:
                    if app not in content:
                        issues.append(ValidationIssue(
                            file_path=file_path_str,
                            issue_type="missing_installed_app",
                            description=f"App " + app + " não encontrada em INSTALLED_APPS",
                            expected=f"" + app + " deve estar em INSTALLED_APPS",
                            actual="App não listada",
                            severity="HIGH"
                        ))
            # Verificar configuracao PostgreSQL - SCAFFOLD: estrutura apenas
            if 'DATABASES' in content:
                # Para scaffold, verificar se usa django-environ ou tem estrutura PostgreSQL
                if ('env.db()' not in content and 
                    'postgresql' not in content.lower() and 
                    'psycopg' not in content.lower()):
                    issues.append(ValidationIssue(
                        file_path=file_path_str,
                        issue_type="wrong_database_config",
                        description="Database não configurado para PostgreSQL",
                        expected="ENGINE deve usar PostgreSQL (psycopg2) ou env.db()",
                        actual="PostgreSQL não detectado",
                        severity="HIGH"
                    ))
            # Verificar configuracao DRF
            if 'REST_FRAMEWORK' not in content:
                issues.append(ValidationIssue(
                    file_path=file_path_str,
                    issue_type="missing_drf_config",
                    description="Configuração REST_FRAMEWORK não encontrada",
                    expected="REST_FRAMEWORK deve estar configurado",
                    actual="Configuração ausente",
                    severity="MEDIUM"
                ))
    
    return issues if issues else None



def validate_content_models_py():
    '''Valida conteúdo específico de models.py.'''
    issues = []
    
    file_paths = list(Path('.').rglob('**/models.py'))
    if not file_paths:
        return ValidationIssue(
            file_path="models.py",
            issue_type="missing_file",
            description="Arquivo models.py não encontrado",
            expected="Arquivo deve existir",
            actual="Arquivo não existe",
            severity="HIGH"
        )
    
    for file_path_obj in file_paths:
        if file_path_obj.exists():
            file_path_str = str(file_path_obj)
            content = file_path_obj.read_text(encoding='utf-8', errors='ignore')
            
    
    return issues if issues else None



def validate_content_pyproject_toml():
    '''Valida conteúdo específico de pyproject.toml.'''
    issues = []
    
    file_paths = list(Path('.').rglob('**/pyproject.toml'))
    if not file_paths:
        return ValidationIssue(
            file_path="pyproject.toml",
            issue_type="missing_file",
            description="Arquivo pyproject.toml não encontrado",
            expected="Arquivo deve existir",
            actual="Arquivo não existe",
            severity="HIGH"
        )
    
    for file_path_obj in file_paths:
        if file_path_obj.exists():
            file_path_str = str(file_path_obj)
            content = file_path_obj.read_text(encoding='utf-8', errors='ignore')
            
    
    return issues if issues else None



def validate_dependency_django():
    '''Valida dependência específica django.'''
    issues = []
    
    # Verificar em pyproject.toml (excluindo agv-system próprio)
    pyproject_files = list(Path('.').rglob('**/pyproject.toml'))
    # Filtrar arquivos do agv-system para evitar validar as próprias dependências  
    project_files = [f for f in pyproject_files if 'agv-system' not in str(f)]
    found = False
    
    for pyproject_file in project_files:
        if pyproject_file.exists():
            content = pyproject_file.read_text(encoding='utf-8', errors='ignore')
            if 'django' in content:
                found = True
                break
    
    if not found:
        issues.append(ValidationIssue(
            file_path="pyproject.toml",
            issue_type="missing_critical_dependency",
            description="Dependência crítica não encontrada: django",
            expected="Dependência django deve estar em pyproject.toml",
            actual="Dependência não encontrada",
            severity="HIGH"
        ))
    
    return issues if issues else None



def validate_dependency_djangorestframework():
    '''Valida dependência específica djangorestframework.'''
    issues = []
    
    # Verificar em pyproject.toml (excluindo agv-system próprio)
    pyproject_files = list(Path('.').rglob('**/pyproject.toml'))
    # Filtrar arquivos do agv-system para evitar validar as próprias dependências  
    project_files = [f for f in pyproject_files if 'agv-system' not in str(f)]
    found = False
    
    for pyproject_file in project_files:
        if pyproject_file.exists():
            content = pyproject_file.read_text(encoding='utf-8', errors='ignore')
            if 'djangorestframework' in content:
                found = True
                break
    
    if not found:
        issues.append(ValidationIssue(
            file_path="pyproject.toml",
            issue_type="missing_critical_dependency",
            description="Dependência crítica não encontrada: djangorestframework",
            expected="Dependência djangorestframework deve estar em pyproject.toml",
            actual="Dependência não encontrada",
            severity="HIGH"
        ))
    
    return issues if issues else None



def validate_dependency_psycopg2_binary():
    '''Valida dependência específica psycopg2-binary.'''
    issues = []
    
    # Verificar em pyproject.toml (excluindo agv-system próprio)
    pyproject_files = list(Path('.').rglob('**/pyproject.toml'))
    # Filtrar arquivos do agv-system para evitar validar as próprias dependências  
    project_files = [f for f in pyproject_files if 'agv-system' not in str(f)]
    found = False
    
    for pyproject_file in project_files:
        if pyproject_file.exists():
            content = pyproject_file.read_text(encoding='utf-8', errors='ignore')
            if 'psycopg2-binary' in content:
                found = True
                break
    
    if not found:
        issues.append(ValidationIssue(
            file_path="pyproject.toml",
            issue_type="missing_critical_dependency",
            description="Dependência crítica não encontrada: psycopg2-binary",
            expected="Dependência psycopg2-binary deve estar em pyproject.toml",
            actual="Dependência não encontrada",
            severity="HIGH"
        ))
    
    return issues if issues else None


def validate_django_settings_advanced():
    '''Valida que settings.py existe com docstring conforme scaffolder.'''
    issues = []
    
    settings_files = list(Path('.').rglob('**/settings.py'))
    if not settings_files:
        issues.append(ValidationIssue(
            file_path="settings.py",
            issue_type="missing_settings_file",
            description="Arquivo settings.py não encontrado",
            expected="Arquivo settings.py deve existir",
            actual="Arquivo não existe",
            severity="HIGH"
        ))
        return issues
    
    for settings_file in settings_files:
        if settings_file.exists():
            content = settings_file.read_text(encoding='utf-8', errors='ignore').strip()
            
            # Para scaffolder, validamos apenas que tem docstring
            # NÃO validamos configurações implementadas (isso é para fases posteriores)
            if not content:
                issues.append(ValidationIssue(
                    file_path=str(settings_file),
                    issue_type="empty_settings_file",
                    description="Arquivo settings.py está vazio",
                    expected="Arquivo deve ter pelo menos uma docstring",
                    actual="Arquivo vazio",
                    severity="MEDIUM"
                ))
                continue
            
            lines = content.split('\n')
            first_non_empty = None
            for line in lines:
                if line.strip():
                    first_non_empty = line.strip()
                    break
            
            if not first_non_empty or not (first_non_empty.startswith('"""') or first_non_empty.startswith("'''")):
                issues.append(ValidationIssue(
                    file_path=str(settings_file),
                    issue_type="missing_scaffold_docstring",
                    description="Arquivo settings.py deve começar com docstring",
                    expected="APENAS docstring conforme agv-scaffolder",
                    actual="Arquivo não começa com docstring",
                    severity="MEDIUM"
                ))
    
    return issues if issues else None

def validate_multi_tenancy_implementation():
    '''Valida estrutura para multi-tenancy conforme scaffolder (apenas docstring).'''
    issues = []
    
    # Verificar que core/models.py existe (onde ficará BaseTenantModel futuramente)
    core_models_files = list(Path('.').rglob('**/core/models.py'))
    
    if not core_models_files:
        issues.append(ValidationIssue(
            file_path="core/models.py",
            issue_type="missing_core_models",
            description="Arquivo core/models.py não encontrado para multi-tenancy",
            expected="Arquivo core/models.py deve existir para estrutura multi-tenant",
            actual="Arquivo não existe",
            severity="HIGH"
        ))
        return issues
    
    # Para scaffolder, validamos apenas que tem docstring
    for model_file in core_models_files:
        if model_file.exists():
            content = model_file.read_text(encoding='utf-8', errors='ignore').strip()
            
            if not content:
                issues.append(ValidationIssue(
                    file_path=str(model_file),
                    issue_type="empty_core_models",
                    description="Arquivo core/models.py está vazio",
                    expected="Arquivo deve ter docstring para multi-tenancy",
                    actual="Arquivo vazio",
                    severity="MEDIUM"
                ))
                continue
            
            lines = content.split('\n')
            first_non_empty = None
            for line in lines:
                if line.strip():
                    first_non_empty = line.strip()
                    break
            
            if not first_non_empty or not (first_non_empty.startswith('"""') or first_non_empty.startswith("'''")):
                issues.append(ValidationIssue(
                    file_path=str(model_file),
                    issue_type="missing_scaffold_docstring",
                    description="Arquivo core/models.py deve começar com docstring",
                    expected="APENAS docstring conforme agv-scaffolder",
                    actual="Arquivo não começa com docstring",
                    severity="MEDIUM"
                ))
    
    return issues if issues else None

def validate_all_blueprint_models():
    '''Valida que arquivos models.py existem com docstrings conforme scaffolder.'''
    issues = []
    
    # Para scaffolder, validamos que os arquivos models.py existem com docstrings
    # NÃO validamos classes implementadas (isso é para fases posteriores)
    
    
    # Verificar app customers
    model_patterns = [
        '**/backend/src/*/customers/models.py',
        '**/src/*/customers/models.py', 
        '**/customers/models.py'
    ]
    
    found_model_file = False
    for pattern in model_patterns:
        matches = list(Path('.').glob(pattern))
        django_models = [p for p in matches if p.is_file() and (p.parent / '__init__.py').exists()]
        
        if django_models:
            found_model_file = True
            # Validar que tem docstring (conforme scaffolder)
            for model_file in django_models:
                content = model_file.read_text(encoding='utf-8', errors='ignore').strip()
                if not content:
                    continue
                    
                lines = content.split('\n')
                first_non_empty = None
                for line in lines:
                    if line.strip():
                        first_non_empty = line.strip()
                        break
                
                if not first_non_empty or not (first_non_empty.startswith('"""') or first_non_empty.startswith("'''")):
                    issues.append(ValidationIssue(
                        file_path=str(model_file),
                        issue_type="missing_scaffold_docstring",
                        description="Arquivo models.py do app customers deve começar com docstring",
                        expected="APENAS docstring conforme agv-scaffolder",
                        actual="Arquivo não começa com docstring",
                        severity="MEDIUM"
                    ))
            break
    
    if not found_model_file:
        issues.append(ValidationIssue(
            file_path="customers/models.py",
            issue_type="missing_models_file",
            description="Arquivo models.py não encontrado para app customers",
            expected="Arquivo models.py deve existir no app customers",
            actual="Arquivo não existe",
            severity="HIGH"
        ))

    # Verificar app operations
    model_patterns = [
        '**/backend/src/*/operations/models.py',
        '**/src/*/operations/models.py', 
        '**/operations/models.py'
    ]
    
    found_model_file = False
    for pattern in model_patterns:
        matches = list(Path('.').glob(pattern))
        django_models = [p for p in matches if p.is_file() and (p.parent / '__init__.py').exists()]
        
        if django_models:
            found_model_file = True
            # Validar que tem docstring (conforme scaffolder)
            for model_file in django_models:
                content = model_file.read_text(encoding='utf-8', errors='ignore').strip()
                if not content:
                    continue
                    
                lines = content.split('\n')
                first_non_empty = None
                for line in lines:
                    if line.strip():
                        first_non_empty = line.strip()
                        break
                
                if not first_non_empty or not (first_non_empty.startswith('"""') or first_non_empty.startswith("'''")):
                    issues.append(ValidationIssue(
                        file_path=str(model_file),
                        issue_type="missing_scaffold_docstring",
                        description="Arquivo models.py do app operations deve começar com docstring",
                        expected="APENAS docstring conforme agv-scaffolder",
                        actual="Arquivo não começa com docstring",
                        severity="MEDIUM"
                    ))
            break
    
    if not found_model_file:
        issues.append(ValidationIssue(
            file_path="operations/models.py",
            issue_type="missing_models_file",
            description="Arquivo models.py não encontrado para app operations",
            expected="Arquivo models.py deve existir no app operations",
            actual="Arquivo não existe",
            severity="HIGH"
        ))

    # Verificar app finance
    model_patterns = [
        '**/backend/src/*/finance/models.py',
        '**/src/*/finance/models.py', 
        '**/finance/models.py'
    ]
    
    found_model_file = False
    for pattern in model_patterns:
        matches = list(Path('.').glob(pattern))
        django_models = [p for p in matches if p.is_file() and (p.parent / '__init__.py').exists()]
        
        if django_models:
            found_model_file = True
            # Validar que tem docstring (conforme scaffolder)
            for model_file in django_models:
                content = model_file.read_text(encoding='utf-8', errors='ignore').strip()
                if not content:
                    continue
                    
                lines = content.split('\n')
                first_non_empty = None
                for line in lines:
                    if line.strip():
                        first_non_empty = line.strip()
                        break
                
                if not first_non_empty or not (first_non_empty.startswith('"""') or first_non_empty.startswith("'''")):
                    issues.append(ValidationIssue(
                        file_path=str(model_file),
                        issue_type="missing_scaffold_docstring",
                        description="Arquivo models.py do app finance deve começar com docstring",
                        expected="APENAS docstring conforme agv-scaffolder",
                        actual="Arquivo não começa com docstring",
                        severity="MEDIUM"
                    ))
            break
    
    if not found_model_file:
        issues.append(ValidationIssue(
            file_path="finance/models.py",
            issue_type="missing_models_file",
            description="Arquivo models.py não encontrado para app finance",
            expected="Arquivo models.py deve existir no app finance",
            actual="Arquivo não existe",
            severity="HIGH"
        ))

    # Verificar app core
    model_patterns = [
        '**/backend/src/*/core/models.py',
        '**/src/*/core/models.py', 
        '**/core/models.py'
    ]
    
    found_model_file = False
    for pattern in model_patterns:
        matches = list(Path('.').glob(pattern))
        django_models = [p for p in matches if p.is_file() and (p.parent / '__init__.py').exists()]
        
        if django_models:
            found_model_file = True
            # Validar que tem docstring (conforme scaffolder)
            for model_file in django_models:
                content = model_file.read_text(encoding='utf-8', errors='ignore').strip()
                if not content:
                    continue
                    
                lines = content.split('\n')
                first_non_empty = None
                for line in lines:
                    if line.strip():
                        first_non_empty = line.strip()
                        break
                
                if not first_non_empty or not (first_non_empty.startswith('"""') or first_non_empty.startswith("'''")):
                    issues.append(ValidationIssue(
                        file_path=str(model_file),
                        issue_type="missing_scaffold_docstring",
                        description="Arquivo models.py do app core deve começar com docstring",
                        expected="APENAS docstring conforme agv-scaffolder",
                        actual="Arquivo não começa com docstring",
                        severity="MEDIUM"
                    ))
            break
    
    if not found_model_file:
        issues.append(ValidationIssue(
            file_path="core/models.py",
            issue_type="missing_models_file",
            description="Arquivo models.py não encontrado para app core",
            expected="Arquivo models.py deve existir no app core",
            actual="Arquivo não existe",
            severity="HIGH"
        ))

    
    return issues if issues else None

def validate_model_files_docstrings():
    '''Valida se arquivos models.py têm docstrings de módulo obrigatórias.'''
    issues = []
    
    # Buscar models.py em estruturas Django típicas
    models_files = []
    django_patterns = [
        '**/backend/src/*/models.py',
        '**/backend/src/*/*/models.py', 
        '**/src/*/models.py',
        '**/src/*/*/models.py',
        '**/models.py',
    ]
    
    for pattern in django_patterns:
        matches = list(Path('.').glob(pattern))
        django_models = [p for p in matches if p.is_file() and (p.parent / '__init__.py').exists()]
        models_files.extend(django_models)
    
    seen = set()
    models_files = [x for x in models_files if not (x in seen or seen.add(x))]
    
    for model_file in models_files:
        if model_file.exists():
            content = model_file.read_text(encoding='utf-8', errors='ignore').strip()
            
            # Verificar se tem docstring de módulo no início
            has_docstring = content.startswith(chr(34)*3) or content.startswith(chr(39)*3)
            if not has_docstring:
                issues.append(ValidationIssue(
                    file_path=str(model_file),
                    issue_type="missing_module_docstring",
                    description=f"Arquivo models.py sem docstring de módulo: {model_file.name}",
                    expected="Arquivo deve começar com docstring de módulo explicando seu propósito",
                    actual="Docstring de módulo não encontrada",
                    severity="MEDIUM"
                ))
    
    return issues if issues else None

def validate_django_apps_structure():
    '''Valida estrutura completa de apps Django conforme Blueprint.'''
    issues = []
    required_apps = ['customers', 'operations', 'finance', 'core']
    
    for app_name in required_apps:
        # Buscar apps Django de forma inteligente
        app_path = []
        
        # Padrões típicos de estrutura Django
        django_patterns = [
            '**/backend/src/*/' + app_name + '/',  # iabank/backend/src/iabank/app_name/
            '**/src/*/' + app_name + '/',          # projeto/src/projeto/app_name/
            '**/' + app_name + '/',                # projeto/app_name/ (fallback)
        ]
        
        for pattern in django_patterns:
            matches = list(Path('.').glob(pattern))
            # Filtrar apenas diretórios que parecem apps Django (têm __init__.py)
            django_apps = [p for p in matches if p.is_dir() and (p / '__init__.py').exists()]
            if django_apps:
                app_path = django_apps
                break
        
        app_found = False
        
        for app_dir in app_path:
            if app_dir.is_dir():
                app_found = True
                
                # Arquivos obrigatórios em cada app
                required_files = ['models.py', 'views.py', 'apps.py', '__init__.py']
                
                for req_file in required_files:
                    file_path = app_dir / req_file
                    if not file_path.exists():
                        issues.append(ValidationIssue(
                            file_path=str(file_path),
                            issue_type="missing_app_file",
                            description="Arquivo obrigatório não encontrado em app " + app_name + ": " + req_file,
                            expected="Arquivo " + req_file + " deve existir no app Django",
                            actual="Arquivo não existe",
                            severity="HIGH"
                        ))
                
                # Verificar diretório de testes
                tests_dir = app_dir / 'tests'
                if not tests_dir.exists():
                    issues.append(ValidationIssue(
                        file_path=str(tests_dir),
                        issue_type="missing_tests_directory",
                        description="Diretório de testes não encontrado no app " + app_name,
                        expected="Diretório tests/ deve existir no app",
                        actual="Diretório não existe",
                        severity="MEDIUM"
                    ))
        
        if not app_found:
            issues.append(ValidationIssue(
                file_path=app_name,
                issue_type="missing_django_app",
                description="App Django não encontrado: " + app_name,
                expected="App " + app_name + " deve estar implementado",
                actual="App não existe",
                severity="HIGH"
            ))
    
    return issues if issues else None

def validate_github_actions_pipeline():
    '''Valida pipeline de CI/CD conforme Blueprint.'''
    issues = []
    
    # Verificar workflow do GitHub Actions
    workflow_paths = list(Path('.').rglob('**/.github/workflows/*.yml')) + \
                    list(Path('.').rglob('**/.github/workflows/*.yaml'))
    
    if not workflow_paths:
        issues.append(ValidationIssue(
            file_path=".github/workflows/",
            issue_type="missing_ci_pipeline",
            description="Pipeline de CI/CD não encontrado",
            expected="Workflow GitHub Actions deve estar configurado",
            actual="Nenhum arquivo de workflow encontrado",
            severity="MEDIUM"
        ))
        return issues
    
    # Verificar conteúdo do workflow principal
    main_workflow = None
    for workflow in workflow_paths:
        content = workflow.read_text(encoding='utf-8', errors='ignore')
        if 'python' in content.lower() or 'node' in content.lower():
            main_workflow = workflow
            break
    
    if main_workflow:
        content = main_workflow.read_text(encoding='utf-8', errors='ignore')
        
        # Verificar steps essenciais
        essential_steps = ['test', 'lint', 'build']
        for step in essential_steps:
            if step not in content.lower():
                issues.append(ValidationIssue(
                    file_path=str(main_workflow),
                    issue_type="missing_ci_step",
                    description=f"Step essencial não encontrado no pipeline: " + step,
                    expected=f"Step '" + step + "' deve estar configurado no workflow",
                    actual="Step não configurado",
                    severity="MEDIUM"
                ))
    
    return issues if issues else None

def validate_complete_test_structure():
    '''Valida estrutura completa de testes conforme Blueprint Arquitetural.'''
    issues = []
    required_apps = ['customers', 'operations', 'finance', 'core']
    
    # Validar arquivos de teste para cada app Django
    for app_name in required_apps:
        # Padrões para localizar apps
        app_patterns = [
            '**/backend/src/*/' + app_name + '/tests/',
            '**/src/*/' + app_name + '/tests/',
            '**/' + app_name + '/tests/'
        ]
        
        app_found = False
        for pattern in app_patterns:
            test_dirs = list(Path('.').glob(pattern))
            if test_dirs:
                app_found = True
                test_dir = test_dirs[0]
                
                # Arquivos obrigatórios em cada diretório de testes
                required_test_files = [
                    '__init__.py',
                    'factories.py', 
                    'test_models.py',
                    'test_views.py'
                ]
                
                for test_file in required_test_files:
                    file_path = test_dir / test_file
                    if not file_path.exists():
                        issues.append(ValidationIssue(
                            file_path=str(file_path),
                            issue_type="missing_test_file",
                            description="Arquivo de teste obrigatório não encontrado: " + test_file,
                            expected="Arquivo " + test_file + " deve existir em tests/ do app " + app_name,
                            actual="Arquivo não existe",
                            severity="HIGH"
                        ))
                break
        
        if not app_found:
            issues.append(ValidationIssue(
                file_path=app_name + "/tests/",
                issue_type="missing_app_test_directory", 
                description="Diretório de testes não encontrado para app " + app_name,
                expected="Diretório tests/ deve existir no app " + app_name,
                actual="Diretório não existe",
                severity="HIGH"
            ))
    
    # Validar testes de integração
    integration_test_patterns = [
        'tests/integration/test_full_loan_workflow.py',
        'backend/tests/integration/test_full_loan_workflow.py',
        '**/tests/integration/test_full_loan_workflow.py'
    ]
    
    integration_found = False
    for pattern in integration_test_patterns:
        if list(Path('.').glob(pattern)):
            integration_found = True
            break
    
    if not integration_found:
        issues.append(ValidationIssue(
            file_path="tests/integration/test_full_loan_workflow.py",
            issue_type="missing_integration_test",
            description="Teste de integração principal não encontrado",
            expected="Arquivo test_full_loan_workflow.py deve existir em tests/integration/",
            actual="Arquivo não existe",
            severity="MEDIUM"
        ))
    
    return issues if issues else None

def validate_django_core_files():
    '''Valida existência dos arquivos core do Django com docstrings.'''
    issues = []
    
    # Arquivos core Django obrigatórios
    core_files = [
        {
            'patterns': ['**/backend/src/*/asgi.py', '**/src/*/asgi.py', '**/asgi.py'],
            'name': 'asgi.py',
            'description': 'Configuração ASGI para deployment assíncrono'
        },
        {
            'patterns': ['**/backend/src/*/wsgi.py', '**/src/*/wsgi.py', '**/wsgi.py'],
            'name': 'wsgi.py', 
            'description': 'Configuração WSGI para deployment'
        },
        {
            'patterns': ['**/backend/src/*/urls.py', '**/src/*/urls.py', '**/urls.py'],
            'name': 'urls.py',
            'description': 'Roteamento principal do Django'
        },
        {
            'patterns': ['**/backend/manage.py', '**/manage.py'],
            'name': 'manage.py',
            'description': 'Script de gerenciamento Django'
        }
    ]
    
    for file_info in core_files:
        found = False
        
        for pattern in file_info['patterns']:
            matches = list(Path('.').glob(pattern))
            # Para manage.py, verificar na raiz ou backend
            if file_info['name'] == 'manage.py':
                django_files = [f for f in matches if f.is_file()]
            else:
                # Para outros arquivos, verificar se estão em estrutura Django
                django_files = [f for f in matches if f.is_file() and 
                               any(parent.name in ['iabank', 'backend', 'src'] for parent in f.parents)]
            
            if django_files:
                found = True
                
                # Verificar se tem docstring (conforme scaffolder)
                for core_file in django_files:
                    content = core_file.read_text(encoding='utf-8', errors='ignore').strip()
                    if not content:
                        issues.append(ValidationIssue(
                            file_path=str(core_file),
                            issue_type="empty_core_file",
                            description=f"Arquivo {file_info['name']} está vazio",
                            expected=f"{file_info['name']} deve ter docstring explicando {file_info['description']}",
                            actual="Arquivo vazio",
                            severity="HIGH"
                        ))
                        continue
                    
                    lines = content.split('\n')
                    first_non_empty = None
                    for line in lines:
                        if line.strip():
                            first_non_empty = line.strip()
                            break
                    
                    # Verificar docstring (menos rigoroso para arquivos de config)
                    if not first_non_empty or not (
                        first_non_empty.startswith('"""') or 
                        first_non_empty.startswith("'''") or
                        first_non_empty.startswith('#')  # Permite comentários
                    ):
                        issues.append(ValidationIssue(
                            file_path=str(core_file),
                            issue_type="missing_core_file_docstring",
                            description=f"Arquivo {file_info['name']} deve começar com docstring/comentário",
                            expected=f"Docstring explicando {file_info['description']}",
                            actual="Arquivo não começa com docstring/comentário",
                            severity="MEDIUM"
                        ))
                break
        
        if not found:
            issues.append(ValidationIssue(
                file_path=file_info['name'],
                issue_type="missing_core_file",
                description=f"Arquivo Django core não encontrado: {file_info['name']}",
                expected=f"Arquivo {file_info['name']} deve existir ({file_info['description']})",
                actual="Arquivo não existe",
                severity="HIGH"
            ))
    
    return issues if issues else None

def validate_frontend_dependencies_complete():
    '''Valida dependências frontend completas conforme Blueprint Arquitetural.'''
    issues = []
    
    # Localizar package.json do frontend
    package_json_patterns = [
        '**/frontend/package.json',
        '**/frontend/*/package.json',
        '**/web/package.json',
        '**/client/package.json',
        '**/package.json'  # fallback
    ]
    
    package_json_file = None
    for pattern in package_json_patterns:
        matches = list(Path('.').glob(pattern))
        if matches:
            # Priorizar package.json em diretórios frontend
            frontend_packages = [p for p in matches if 
                                any(part in str(p).lower() for part in ['frontend', 'web', 'client'])]
            if frontend_packages:
                package_json_file = frontend_packages[0]
            else:
                package_json_file = matches[0]
            break
    
    if not package_json_file:
        issues.append(ValidationIssue(
            file_path="package.json",
            issue_type="missing_package_json",
            description="Arquivo package.json não encontrado no frontend",
            expected="package.json deve existir no diretório frontend",
            actual="Arquivo não encontrado",
            severity="HIGH"
        ))
        return issues
    
    try:
        import json
        with open(package_json_file, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
    except Exception as e:
        issues.append(ValidationIssue(
            file_path=str(package_json_file),
            issue_type="invalid_package_json",
            description="package.json inválido ou corrompido",
            expected="JSON válido",
            actual=f"Erro: {str(e)}",
            severity="HIGH"
        ))
        return issues
    
    # Dependências obrigatórias conforme análise anterior
    required_deps = {
        'dependencies': {
            'react': 'Framework React principal',
            'react-dom': 'React DOM para web',
            '@tanstack/react-query': 'Gerenciamento estado server',
            'zustand': 'Gerenciamento estado client',
            'axios': 'Cliente HTTP',
            'zod': 'Validação schemas',
            'react-router-dom': 'Roteamento React',
            'react-hook-form': 'Gerenciamento formulários',
            '@hookform/resolvers': 'Resolvers para react-hook-form'
        },
        'devDependencies': {
            'typescript': 'Suporte TypeScript',
            '@types/react': 'Tipos TypeScript para React',
            '@types/react-dom': 'Tipos TypeScript para React DOM', 
            'vite': 'Build tool moderno',
            '@vitejs/plugin-react': 'Plugin React para Vite',
            'tailwindcss': 'Framework CSS utility-first',
            'autoprefixer': 'PostCSS plugin',
            'postcss': 'Processador CSS',
            'eslint': 'Linter JavaScript/TypeScript',
            '@typescript-eslint/parser': 'Parser ESLint para TypeScript',
            '@typescript-eslint/eslint-plugin': 'Plugin ESLint para TypeScript'
        }
    }
    
    # Verificar dependências obrigatórias
    for dep_type, deps in required_deps.items():
        if dep_type not in package_data:
            issues.append(ValidationIssue(
                file_path=str(package_json_file),
                issue_type="missing_dependency_section",
                description=f"Seção {dep_type} não encontrada em package.json",
                expected=f"Seção {dep_type} deve existir",
                actual="Seção não existe",
                severity="HIGH"
            ))
            continue
            
        for dep_name, dep_description in deps.items():
            if dep_name not in package_data[dep_type]:
                issues.append(ValidationIssue(
                    file_path=str(package_json_file),
                    issue_type="missing_required_dependency",
                    description=f"Dependência obrigatória não encontrada: {dep_name}",
                    expected=f"{dep_name} deve estar em {dep_type} ({dep_description})",
                    actual=f"{dep_name} não está em {dep_type}",
                    severity="HIGH"
                ))
    
    # Verificar scripts obrigatórios
    required_scripts = {
        'dev': 'Script de desenvolvimento',
        'build': 'Script de build de produção',
        'lint': 'Script de linting',
        'preview': 'Script de preview'
    }
    
    if 'scripts' not in package_data:
        issues.append(ValidationIssue(
            file_path=str(package_json_file),
            issue_type="missing_scripts_section",
            description="Seção scripts não encontrada em package.json",
            expected="Seção scripts deve existir com scripts de build e dev",
            actual="Seção scripts não existe",
            severity="HIGH"
        ))
    else:
        for script_name, script_description in required_scripts.items():
            if script_name not in package_data['scripts']:
                issues.append(ValidationIssue(
                    file_path=str(package_json_file),
                    issue_type="missing_required_script",
                    description=f"Script obrigatório não encontrado: {script_name}",
                    expected=f"Script '{script_name}' deve existir ({script_description})",
                    actual=f"Script '{script_name}' não encontrado",
                    severity="MEDIUM"
                ))
    
    return issues if issues else None

def validate_backend_dependencies_complete():
    '''Valida dependências backend completas conforme Blueprint Arquitetural.'''
    issues = []
    
    # Localizar arquivo de dependências do backend
    dep_file = None
    dep_type = None
    
    # Padrões de busca priorizando pyproject.toml
    dependency_patterns = [
        ('pyproject.toml', [
            '**/backend/pyproject.toml',
            '**/backend/*/pyproject.toml',
            '**/pyproject.toml'
        ]),
        ('requirements.txt', [
            '**/backend/requirements.txt',
            '**/backend/*/requirements.txt', 
            '**/requirements.txt'
        ])
    ]
    
    for file_type, patterns in dependency_patterns:
        for pattern in patterns:
            matches = list(Path('.').glob(pattern))
            if matches:
                # Priorizar arquivos em diretórios backend
                backend_deps = [p for p in matches if 
                               any(part in str(p).lower() for part in ['backend', 'api', 'server'])]
                if backend_deps:
                    dep_file = backend_deps[0]
                    dep_type = file_type
                    break
                else:
                    dep_file = matches[0]
                    dep_type = file_type
                    break
        if dep_file:
            break
    
    if not dep_file:
        issues.append(ValidationIssue(
            file_path="pyproject.toml|requirements.txt",
            issue_type="missing_dependencies_file",
            description="Arquivo de dependências não encontrado no backend",
            expected="pyproject.toml ou requirements.txt deve existir no backend",
            actual="Nenhum arquivo de dependências encontrado",
            severity="HIGH"
        ))
        return issues
    
    # Dependências obrigatórias Django expandidas
    required_deps = {
        'core_django': {
            'django': 'Framework web principal',
            'djangorestframework': 'API REST framework',
            'django-cors-headers': 'CORS para frontend'
        },
        'database': {
            'psycopg2-binary': 'Driver PostgreSQL (ou sqlite se usando)',
            'django-extensions': 'Extensões úteis para desenvolvimento'
        },
        'authentication': {
            'djangorestframework-simplejwt': 'JWT authentication',
            'django-allauth': 'Sistema autenticação completo (opcional)'
        },
        'production': {
            'gunicorn': 'WSGI server para produção',
            'whitenoise': 'Servir arquivos estáticos',
            'python-decouple': 'Gerenciamento de configurações'
        },
        'development': {
            'django-debug-toolbar': 'Debug toolbar para desenvolvimento',
            'pytest': 'Framework de testes',
            'pytest-django': 'Plugin pytest para Django',
            'pytest-cov': 'Cobertura de testes'
        },
        'api_docs': {
            'drf-spectacular': 'Documentação automática OpenAPI/Swagger'
        }
    }
    
    if dep_type == 'pyproject.toml':
        try:
            import tomli
            with open(dep_file, 'rb') as f:
                toml_data = tomli.load(f)
        except ImportError:
            try:
                import tomllib
                with open(dep_file, 'rb') as f:
                    toml_data = tomllib.load(f)
            except ImportError:
                issues.append(ValidationIssue(
                    file_path=str(dep_file),
                    issue_type="missing_toml_parser",
                    description="Parser TOML não disponível (tomli/tomllib)",
                    expected="tomli ou tomllib deve estar disponível",
                    actual="Parser TOML não encontrado",
                    severity="MEDIUM"
                ))
                return issues
        except Exception as e:
            issues.append(ValidationIssue(
                file_path=str(dep_file),
                issue_type="invalid_pyproject_toml",
                description="pyproject.toml inválido ou corrompido",
                expected="TOML válido",
                actual=f"Erro: {str(e)}",
                severity="HIGH"
            ))
            return issues
        
        # Verificar dependências no pyproject.toml
        dependencies = {}
        if 'project' in toml_data and 'dependencies' in toml_data['project']:
            # Formato padrão PEP 621
            for dep in toml_data['project']['dependencies']:
                dep_name = dep.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].strip()
                dependencies[dep_name] = 'main'
        
        if 'project' in toml_data and 'optional-dependencies' in toml_data['project']:
            for group, deps in toml_data['project']['optional-dependencies'].items():
                for dep in deps:
                    dep_name = dep.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].strip()
                    dependencies[dep_name] = group
        
        # Formato poetry/setuptools
        if 'tool' in toml_data:
            if 'poetry' in toml_data['tool'] and 'dependencies' in toml_data['tool']['poetry']:
                for dep_name in toml_data['tool']['poetry']['dependencies']:
                    if dep_name != 'python':
                        dependencies[dep_name] = 'main'
            
            if 'poetry' in toml_data['tool'] and 'group' in toml_data['tool']['poetry']:
                for group_name, group_data in toml_data['tool']['poetry']['group'].items():
                    if 'dependencies' in group_data:
                        for dep_name in group_data['dependencies']:
                            dependencies[dep_name] = group_name
        
    else:  # requirements.txt
        try:
            with open(dep_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            issues.append(ValidationIssue(
                file_path=str(dep_file),
                issue_type="invalid_requirements_txt",
                description="requirements.txt inválido ou ilegível",
                expected="Arquivo de texto válido",
                actual=f"Erro: {str(e)}",
                severity="HIGH"
            ))
            return issues
        
        dependencies = {}
        for line in content.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                dep_name = line.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].strip()
                dependencies[dep_name] = 'main'
    
    # Verificar dependências obrigatórias
    for category, deps in required_deps.items():
        for dep_name, dep_description in deps.items():
            if dep_name not in dependencies:
                # Algumas dependências são opcionais dependendo do caso
                severity = "HIGH" if category in ['core_django', 'database'] else "MEDIUM"
                issues.append(ValidationIssue(
                    file_path=str(dep_file),
                    issue_type="missing_backend_dependency",
                    description=f"Dependência backend não encontrada: {dep_name}",
                    expected=f"{dep_name} deve estar nas dependências ({dep_description})",
                    actual=f"{dep_name} não encontrado",
                    severity=severity
                ))
    
    # Verificar estrutura do arquivo TOML
    if dep_type == 'pyproject.toml':
        if 'project' not in toml_data:
            issues.append(ValidationIssue(
                file_path=str(dep_file),
                issue_type="missing_project_section",
                description="Seção [project] não encontrada em pyproject.toml",
                expected="pyproject.toml deve ter seção [project] com metadados",
                actual="Seção [project] não existe",
                severity="HIGH"
            ))
        else:
            required_project_fields = ['name', 'version', 'description', 'dependencies']
            for field in required_project_fields:
                if field not in toml_data['project']:
                    issues.append(ValidationIssue(
                        file_path=str(dep_file),
                        issue_type="missing_project_field",
                        description=f"Campo obrigatório não encontrado em [project]: {field}",
                        expected=f"Campo '{field}' deve existir em [project]",
                        actual=f"Campo '{field}' não encontrado",
                        severity="MEDIUM"
                    ))
    
    return issues if issues else None

def validate_frontend_core_files():
    '''Valida arquivos frontend core conforme Blueprint Arquitetural.'''
    issues = []
    
    # Localizar diretório frontend
    frontend_dirs = []
    frontend_patterns = [
        '**/frontend/',
        '**/web/',
        '**/client/',
        '**/ui/',
        '**/'  # fallback para raiz se tiver package.json
    ]
    
    for pattern in frontend_patterns:
        matches = list(Path('.').glob(pattern))
        for match in matches:
            if match.is_dir():
                # Verificar se tem package.json para confirmar que é frontend
                if (match / 'package.json').exists():
                    frontend_dirs.append(match)
                    break
    
    if not frontend_dirs:
        issues.append(ValidationIssue(
            file_path="frontend/",
            issue_type="missing_frontend_directory",
            description="Diretório frontend não encontrado",
            expected="Diretório frontend com package.json deve existir",
            actual="Nenhum diretório frontend encontrado",
            severity="HIGH"
        ))
        return issues
    
    frontend_dir = frontend_dirs[0]  # Usar o primeiro encontrado
    
    # Arquivos de configuração obrigatórios para frontend moderno
    required_config_files = [
        {
            'patterns': ['vite.config.ts', 'vite.config.js'],
            'name': 'vite.config',
            'description': 'Configuração do Vite build tool',
            'severity': 'HIGH'
        },
        {
            'patterns': ['tsconfig.json'],
            'name': 'tsconfig.json',
            'description': 'Configuração TypeScript',
            'severity': 'HIGH'
        },
        {
            'patterns': ['tailwind.config.js', 'tailwind.config.ts'],
            'name': 'tailwind.config',
            'description': 'Configuração Tailwind CSS',
            'severity': 'MEDIUM'  # Opcional se não usar Tailwind
        },
        {
            'patterns': ['postcss.config.js', 'postcss.config.ts'],
            'name': 'postcss.config',
            'description': 'Configuração PostCSS',
            'severity': 'MEDIUM'
        },
        {
            'patterns': ['.eslintrc.js', '.eslintrc.json', '.eslintrc.ts', 'eslint.config.js'],
            'name': 'eslint config',
            'description': 'Configuração ESLint',
            'severity': 'MEDIUM'
        }
    ]
    
    for config in required_config_files:
        found = False
        for pattern in config['patterns']:
            config_file = frontend_dir / pattern
            if config_file.exists():
                found = True
                
                # Verificar se arquivo não está vazio
                try:
                    content = config_file.read_text(encoding='utf-8', errors='ignore').strip()
                    if not content:
                        issues.append(ValidationIssue(
                            file_path=str(config_file),
                            issue_type="empty_config_file",
                            description=f"Arquivo de configuração {config['name']} está vazio",
                            expected=f"Arquivo deve conter configuração para {config['description']}",
                            actual="Arquivo vazio",
                            severity=config['severity']
                        ))
                    elif config['name'] == 'tsconfig.json':
                        # Validação específica para tsconfig.json
                        try:
                            import json
                            json.loads(content)
                        except json.JSONDecodeError:
                            issues.append(ValidationIssue(
                                file_path=str(config_file),
                                issue_type="invalid_tsconfig_json",
                                description="tsconfig.json contém JSON inválido",
                                expected="JSON válido",
                                actual="Erro de sintaxe JSON",
                                severity="HIGH"
                            ))
                except Exception:
                    issues.append(ValidationIssue(
                        file_path=str(config_file),
                        issue_type="unreadable_config_file",
                        description=f"Arquivo de configuração {config['name']} não pode ser lido",
                        expected="Arquivo legível",
                        actual="Erro ao ler arquivo",
                        severity=config['severity']
                    ))
                break
        
        if not found and config['severity'] == 'HIGH':
            issues.append(ValidationIssue(
                file_path=f"{frontend_dir}/{config['patterns'][0]}",
                issue_type="missing_config_file",
                description=f"Arquivo de configuração obrigatório não encontrado: {config['name']}",
                expected=f"Arquivo {config['name']} deve existir ({config['description']})",
                actual="Arquivo não existe",
                severity=config['severity']
            ))
    
    # Arquivos fonte principais obrigatórios
    required_source_files = [
        {
            'patterns': ['src/main.tsx', 'src/main.ts', 'src/index.tsx', 'src/index.ts'],
            'name': 'main entry point',
            'description': 'Ponto de entrada principal da aplicação'
        },
        {
            'patterns': ['src/App.tsx', 'src/App.ts', 'src/app.tsx', 'src/app.ts'],
            'name': 'App component',
            'description': 'Componente raiz da aplicação'
        },
        {
            'patterns': ['index.html'],
            'name': 'index.html',
            'description': 'Template HTML principal'
        }
    ]
    
    for source in required_source_files:
        found = False
        for pattern in source['patterns']:
            source_file = frontend_dir / pattern
            if source_file.exists():
                found = True
                
                # Verificar se arquivo tem comentário de cabeçalho (conforme scaffolder)
                try:
                    content = source_file.read_text(encoding='utf-8', errors='ignore').strip()
                    if not content:
                        issues.append(ValidationIssue(
                            file_path=str(source_file),
                            issue_type="empty_source_file",
                            description=f"Arquivo fonte {source['name']} está vazio",
                            expected=f"Arquivo deve ter comentário de cabeçalho e {source['description']}",
                            actual="Arquivo vazio",
                            severity="HIGH"
                        ))
                        continue
                    
                    # Para arquivos .tsx/.ts/.js, verificar comentário de cabeçalho
                    if source_file.suffix in ['.tsx', '.ts', '.js', '.jsx']:
                        lines = content.split('\n')[:5]  # Primeiras 5 linhas
                        comment_found = any(
                            line.strip().startswith('/*') or 
                            line.strip().startswith('//') or
                            line.strip().startswith('*')
                            for line in lines
                        )
                        
                        if not comment_found:
                            issues.append(ValidationIssue(
                                file_path=str(source_file),
                                issue_type="missing_source_comment",
                                description=f"Arquivo {source['name']} sem comentário de cabeçalho",
                                expected="Arquivo deve começar com comentário explicando propósito (conforme scaffolder)",
                                actual="Comentário de cabeçalho não encontrado",
                                severity="MEDIUM"
                            ))
                
                except Exception:
                    pass
                break
        
        if not found:
            issues.append(ValidationIssue(
                file_path=f"{frontend_dir}/{source['patterns'][0]}",
                issue_type="missing_source_file",
                description=f"Arquivo fonte obrigatório não encontrado: {source['name']}",
                expected=f"Arquivo {source['name']} deve existir ({source['description']})",
                actual="Arquivo não existe",
                severity="HIGH"
            ))
    
    # Verificar estrutura de diretórios src/
    src_dir = frontend_dir / 'src'
    if not src_dir.exists():
        issues.append(ValidationIssue(
            file_path=str(src_dir),
            issue_type="missing_src_directory",
            description="Diretório src/ não encontrado no frontend",
            expected="Diretório src/ deve conter código fonte da aplicação",
            actual="Diretório src/ não existe",
            severity="HIGH"
        ))
    else:
        # Verificar subdiretórios recomendados
        recommended_dirs = ['components', 'pages', 'hooks', 'utils', 'types']
        missing_dirs = []
        for dir_name in recommended_dirs:
            if not (src_dir / dir_name).exists():
                missing_dirs.append(dir_name)
        
        if len(missing_dirs) > 3:  # Se mais da metade estão faltando
            issues.append(ValidationIssue(
                file_path=str(src_dir),
                issue_type="incomplete_src_structure",
                description=f"Estrutura src/ incompleta - faltam diretórios: {', '.join(missing_dirs)}",
                expected="Diretório src/ deve ter estrutura organizada (components, pages, hooks, utils, types)",
                actual=f"Faltam diretórios: {', '.join(missing_dirs)}",
                severity="MEDIUM"
            ))
    
    return issues if issues else None

def validate_docker_complete_configuration():
    '''Valida configuração Docker completa conforme Blueprint Arquitetural.'''
    issues = []
    
    # Arquivos Docker obrigatórios
    docker_files = [
        {
            'patterns': ['docker-compose.yml', 'docker-compose.yaml'],
            'name': 'docker-compose',
            'description': 'Orquestração de containers',
            'severity': 'HIGH'
        },
        {
            'patterns': ['.dockerignore'],
            'name': '.dockerignore',
            'description': 'Exclusões para build Docker',
            'severity': 'MEDIUM'
        },
        {
            'patterns': ['docker-compose.dev.yml', 'docker-compose.development.yml'],
            'name': 'docker-compose.dev',
            'description': 'Configuração Docker para desenvolvimento',
            'severity': 'MEDIUM'
        },
        {
            'patterns': ['docker-compose.prod.yml', 'docker-compose.production.yml'],
            'name': 'docker-compose.prod',
            'description': 'Configuração Docker para produção',
            'severity': 'MEDIUM'
        }
    ]
    
    for docker_config in docker_files:
        found = False
        for pattern in docker_config['patterns']:
            docker_file = Path('.') / pattern
            if docker_file.exists():
                found = True
                
                # Verificar se arquivo não está vazio
                try:
                    content = docker_file.read_text(encoding='utf-8', errors='ignore').strip()
                    if not content:
                        issues.append(ValidationIssue(
                            file_path=str(docker_file),
                            issue_type="empty_docker_config",
                            description=f"Arquivo Docker {docker_config['name']} está vazio",
                            expected=f"Arquivo deve conter configuração para {docker_config['description']}",
                            actual="Arquivo vazio",
                            severity=docker_config['severity']
                        ))
                    else:
                        # Validações específicas por tipo
                        if 'docker-compose' in pattern and 'version:' not in content:
                            issues.append(ValidationIssue(
                                file_path=str(docker_file),
                                issue_type="invalid_docker_compose",
                                description=f"docker-compose.yml sem especificação de versão",
                                expected="Arquivo deve ter 'version:' especificado",
                                actual="Versão não encontrada",
                                severity="MEDIUM"
                            ))
                        
                        if pattern == '.dockerignore':
                            # Verificar entradas importantes no .dockerignore
                            important_ignores = ['node_modules', '.git', '*.pyc', '__pycache__', '.env']
                            missing_ignores = [ig for ig in important_ignores if ig not in content]
                            if len(missing_ignores) > 2:
                                issues.append(ValidationIssue(
                                    file_path=str(docker_file),
                                    issue_type="incomplete_dockerignore",
                                    description=f".dockerignore incompleto - faltam: {', '.join(missing_ignores)}",
                                    expected="Deve incluir exclusões importantes (node_modules, .git, *.pyc, etc.)",
                                    actual=f"Faltam: {', '.join(missing_ignores)}",
                                    severity="MEDIUM"
                                ))
                
                except Exception:
                    issues.append(ValidationIssue(
                        file_path=str(docker_file),
                        issue_type="unreadable_docker_config",
                        description=f"Arquivo Docker {docker_config['name']} não pode ser lido",
                        expected="Arquivo legível",
                        actual="Erro ao ler arquivo",
                        severity=docker_config['severity']
                    ))
                break
        
        if not found and docker_config['severity'] == 'HIGH':
            issues.append(ValidationIssue(
                file_path=docker_config['patterns'][0],
                issue_type="missing_docker_config",
                description=f"Arquivo Docker obrigatório não encontrado: {docker_config['name']}",
                expected=f"Arquivo {docker_config['name']} deve existir ({docker_config['description']})",
                actual="Arquivo não existe",
                severity=docker_config['severity']
            ))
    
    return issues if issues else None

def validate_specific_directory_structure():
    '''Valida estruturas específicas de diretórios conforme Blueprint.'''
    issues = []
    
    # Diretórios específicos obrigatórios para projeto Django
    backend_dirs = [
        {
            'patterns': ['**/backend/static/', '**/static/', 'iabank/backend/static/'],
            'name': 'static/',
            'description': 'Arquivos estáticos do Django',
            'severity': 'MEDIUM'
        },
        {
            'patterns': ['**/backend/media/', '**/media/', 'iabank/backend/media/'],
            'name': 'media/',
            'description': 'Upload de arquivos de usuários',
            'severity': 'MEDIUM'
        },
        {
            'patterns': ['**/logs/', 'logs/', 'backend/logs/'],
            'name': 'logs/',
            'description': 'Diretório para logs da aplicação',
            'severity': 'MEDIUM'
        },
        {
            'patterns': ['**/config/', 'config/', 'backend/config/'],
            'name': 'config/',
            'description': 'Configurações por ambiente',
            'severity': 'MEDIUM'
        }
    ]
    
    # Verificar diretórios backend
    for dir_config in backend_dirs:
        found = False
        for pattern in dir_config['patterns']:
            matches = list(Path('.').glob(pattern))
            if matches and any(match.is_dir() for match in matches):
                found = True
                break
        
        if not found and dir_config['severity'] == 'HIGH':
            issues.append(ValidationIssue(
                file_path=dir_config['name'],
                issue_type="missing_required_directory",
                description=f"Diretório obrigatório não encontrado: {dir_config['name']}",
                expected=f"Diretório {dir_config['name']} deve existir ({dir_config['description']})",
                actual="Diretório não existe",
                severity=dir_config['severity']
            ))
    
    # Validar estrutura de migrations Django por app
    django_apps = ['core', 'customers', 'finance', 'operations']  # Apps do Blueprint
    
    for app_name in django_apps:
        migrations_patterns = [
            f'**/backend/src/*/{app_name}/migrations/',
            f'**/src/*/{app_name}/migrations/',
            f'**/{app_name}/migrations/'
        ]
        
        migrations_found = False
        for pattern in migrations_patterns:
            matches = list(Path('.').glob(pattern))
            if matches and any(match.is_dir() for match in matches):
                migrations_found = True
                migrations_dir = matches[0]
                
                # Verificar se tem __init__.py
                init_file = migrations_dir / '__init__.py'
                if not init_file.exists():
                    issues.append(ValidationIssue(
                        file_path=str(init_file),
                        issue_type="missing_migrations_init",
                        description=f"Arquivo __init__.py faltante em migrations do app {app_name}",
                        expected="Arquivo __init__.py deve existir em diretório migrations",
                        actual="Arquivo __init__.py não encontrado",
                        severity="MEDIUM"
                    ))
                break
        
        if not migrations_found:
            issues.append(ValidationIssue(
                file_path=f"{app_name}/migrations/",
                issue_type="missing_migrations_directory",
                description=f"Diretório migrations não encontrado para app {app_name}",
                expected=f"App {app_name} deve ter diretório migrations/",
                actual="Diretório migrations não existe",
                severity="MEDIUM"
            ))
    
    # Validar estrutura de configurações por ambiente
    config_patterns = ['config/', 'settings/', '**/config/', '**/settings/']
    config_found = False
    
    for pattern in config_patterns:
        matches = list(Path('.').glob(pattern))
        if matches and any(match.is_dir() for match in matches):
            config_found = True
            config_dir = matches[0]
            
            # Verificar arquivos de configuração por ambiente
            env_configs = ['development.py', 'production.py', 'testing.py']
            missing_configs = []
            
            for env_config in env_configs:
                if not (config_dir / env_config).exists():
                    missing_configs.append(env_config)
            
            if len(missing_configs) > 1:  # Se mais de um arquivo estiver faltando
                issues.append(ValidationIssue(
                    file_path=str(config_dir),
                    issue_type="incomplete_environment_configs",
                    description=f"Configurações de ambiente incompletas - faltam: {', '.join(missing_configs)}",
                    expected="Deve ter configurações para development, production, testing",
                    actual=f"Faltam: {', '.join(missing_configs)}",
                    severity="MEDIUM"
                ))
            break
    
    return issues if issues else None

def validate_ide_configuration_files():
    '''Valida arquivos de configuração IDE para desenvolvimento.'''
    issues = []
    
    # Configurações IDE importantes
    ide_configs = [
        {
            'patterns': ['.vscode/settings.json'],
            'name': '.vscode/settings.json',
            'description': 'Configurações do VS Code',
            'severity': 'MEDIUM'
        },
        {
            'patterns': ['.vscode/launch.json'],
            'name': '.vscode/launch.json', 
            'description': 'Configurações de debug do VS Code',
            'severity': 'MEDIUM'
        },
        {
            'patterns': ['.vscode/extensions.json'],
            'name': '.vscode/extensions.json',
            'description': 'Extensões recomendadas do VS Code',
            'severity': 'MEDIUM'
        },
        {
            'patterns': ['.editorconfig'],
            'name': '.editorconfig',
            'description': 'Configurações de formatação universal',
            'severity': 'MEDIUM'
        }
    ]
    
    # Verificar arquivos de configuração IDE
    for ide_config in ide_configs:
        found = False
        for pattern in ide_config['patterns']:
            config_file = Path('.') / pattern
            if config_file.exists():
                found = True
                
                # Verificar se arquivo não está vazio
                try:
                    content = config_file.read_text(encoding='utf-8', errors='ignore').strip()
                    if not content:
                        issues.append(ValidationIssue(
                            file_path=str(config_file),
                            issue_type="empty_ide_config",
                            description=f"Arquivo IDE {ide_config['name']} está vazio",
                            expected=f"Arquivo deve conter configuração para {ide_config['description']}",
                            actual="Arquivo vazio",
                            severity=ide_config['severity']
                        ))
                    else:
                        # Validações específicas por tipo
                        if 'settings.json' in pattern:
                            try:
                                import json
                                settings = json.loads(content)
                                # Verificar configurações importantes
                                important_settings = [
                                    'python.defaultInterpreter',
                                    'editor.formatOnSave',
                                    'files.trimTrailingWhitespace'
                                ]
                                missing_settings = [s for s in important_settings if s not in settings]
                                if len(missing_settings) > 1:
                                    issues.append(ValidationIssue(
                                        file_path=str(config_file),
                                        issue_type="incomplete_vscode_settings",
                                        description=f"Configurações VS Code incompletas - faltam: {', '.join(missing_settings)}",
                                        expected="Deve incluir configurações importantes de formatação e Python",
                                        actual=f"Faltam: {', '.join(missing_settings)}",
                                        severity="MEDIUM"
                                    ))
                            except json.JSONDecodeError:
                                issues.append(ValidationIssue(
                                    file_path=str(config_file),
                                    issue_type="invalid_vscode_settings",
                                    description="settings.json contém JSON inválido",
                                    expected="JSON válido",
                                    actual="Erro de sintaxe JSON",
                                    severity="MEDIUM"
                                ))
                        
                        if 'extensions.json' in pattern:
                            try:
                                import json
                                extensions = json.loads(content)
                                # Verificar extensões importantes
                                important_extensions = [
                                    'ms-python.python',
                                    'bradlc.vscode-tailwindcss',
                                    'esbenp.prettier-vscode'
                                ]
                                if 'recommendations' not in extensions:
                                    issues.append(ValidationIssue(
                                        file_path=str(config_file),
                                        issue_type="missing_extension_recommendations",
                                        description="extensions.json sem seção 'recommendations'",
                                        expected="Deve ter array 'recommendations' com extensões",
                                        actual="Seção recommendations não encontrada",
                                        severity="MEDIUM"
                                    ))
                            except json.JSONDecodeError:
                                issues.append(ValidationIssue(
                                    file_path=str(config_file),
                                    issue_type="invalid_extensions_json",
                                    description="extensions.json contém JSON inválido",
                                    expected="JSON válido",
                                    actual="Erro de sintaxe JSON",
                                    severity="MEDIUM"
                                ))
                        
                        if '.editorconfig' in pattern:
                            # Verificar configurações importantes no .editorconfig
                            important_configs = ['indent_style', 'end_of_line', 'charset']
                            missing_configs = [c for c in important_configs if c not in content]
                            if len(missing_configs) > 1:
                                issues.append(ValidationIssue(
                                    file_path=str(config_file),
                                    issue_type="incomplete_editorconfig",
                                    description=f".editorconfig incompleto - faltam: {', '.join(missing_configs)}",
                                    expected="Deve incluir indent_style, end_of_line, charset",
                                    actual=f"Faltam: {', '.join(missing_configs)}",
                                    severity="MEDIUM"
                                ))
                
                except Exception:
                    issues.append(ValidationIssue(
                        file_path=str(config_file),
                        issue_type="unreadable_ide_config",
                        description=f"Arquivo IDE {ide_config['name']} não pode ser lido",
                        expected="Arquivo legível",
                        actual="Erro ao ler arquivo",
                        severity=ide_config['severity']
                    ))
                break
    
    # Verificar se ao menos .editorconfig existe (mais universal)
    has_editor_config = any((Path('.') / pattern).exists() for pattern in ['.editorconfig'])
    has_any_ide_config = any((Path('.') / config['patterns'][0]).exists() for config in ide_configs)
    
    if not has_editor_config and not has_any_ide_config:
        issues.append(ValidationIssue(
            file_path=".editorconfig",
            issue_type="no_ide_configuration",
            description="Nenhuma configuração IDE encontrada",
            expected="Ao menos .editorconfig deve existir para formatação consistente",
            actual="Nenhum arquivo de configuração IDE encontrado",
            severity="MEDIUM"
        ))
    
    return issues if issues else None

def validate_security_best_practices():
    '''Valida configurações de segurança e boas práticas.'''
    issues = []
    
    # 1. Validar .env.example completo
    env_example_file = Path('.') / '.env.example'
    if env_example_file.exists():
        try:
            content = env_example_file.read_text(encoding='utf-8', errors='ignore')
            
            # Variáveis de segurança obrigatórias
            required_security_vars = [
                'SECRET_KEY',
                'DATABASE_URL', 
                'DEBUG',
                'ALLOWED_HOSTS',
                'CORS_ALLOWED_ORIGINS',
                'JWT_SECRET_KEY'
            ]
            
            missing_vars = [var for var in required_security_vars if var not in content]
            if missing_vars:
                issues.append(ValidationIssue(
                    file_path=str(env_example_file),
                    issue_type="incomplete_env_example",
                    description=f".env.example incompleto - faltam: {', '.join(missing_vars)}",
                    expected="Deve incluir todas as variáveis de segurança críticas",
                    actual=f"Faltam: {', '.join(missing_vars)}",
                    severity="HIGH"
                ))
            
            # Verificar se valores não são reais (devem ser placeholders)
            dangerous_patterns = ['password123', 'admin', 'root', 'secret']
            for pattern in dangerous_patterns:
                if pattern.lower() in content.lower():
                    issues.append(ValidationIssue(
                        file_path=str(env_example_file),
                        issue_type="dangerous_env_values",
                        description=f".env.example contém valores perigosos: {pattern}",
                        expected="Deve usar apenas placeholders, não valores reais",
                        actual=f"Valor perigoso encontrado: {pattern}",
                        severity="MEDIUM"
                    ))
        
        except Exception:
            pass
    
    # 2. Validar configurações de segurança Django
    settings_patterns = [
        '**/backend/src/*/settings.py',
        '**/src/*/settings.py',
        '**/settings.py'
    ]
    
    for pattern in settings_patterns:
        matches = list(Path('.').glob(pattern))
        for settings_file in matches:
            if settings_file.exists():
                try:
                    content = settings_file.read_text(encoding='utf-8', errors='ignore')
                    
                    # Verificar configurações de segurança críticas
                    security_checks = [
                        ('SECURE_SSL_REDIRECT', 'Redirecionamento SSL'),
                        ('SECURE_BROWSER_XSS_FILTER', 'Filtro XSS'),
                        ('SECURE_CONTENT_TYPE_NOSNIFF', 'Content Type Nosniff'),
                        ('X_FRAME_OPTIONS', 'Proteção contra clickjacking'),
                        ('CORS_ALLOWED_ORIGINS', 'CORS configurado')
                    ]
                    
                    missing_security = []
                    for setting, description in security_checks:
                        if setting not in content:
                            missing_security.append(f"{setting} ({description})")
                    
                    if len(missing_security) > 2:
                        issues.append(ValidationIssue(
                            file_path=str(settings_file),
                            issue_type="missing_security_settings",
                            description=f"Configurações de segurança Django faltantes: {len(missing_security)} itens",
                            expected="Deve incluir configurações de segurança críticas",
                            actual=f"Faltam: {', '.join(missing_security[:3])}...",
                            severity="HIGH"
                        ))
                    
                    # Verificar se DEBUG não está hardcoded como True
                    if 'DEBUG = True' in content and 'env(' not in content:
                        issues.append(ValidationIssue(
                            file_path=str(settings_file),
                            issue_type="hardcoded_debug_true",
                            description="DEBUG hardcoded como True em settings.py",
                            expected="DEBUG deve vir de variável de ambiente",
                            actual="DEBUG = True hardcoded",
                            severity="HIGH"
                        ))
                    
                    # Verificar SECRET_KEY
                    if 'SECRET_KEY' in content and 'env(' not in content and 'SECRET_KEY =' in content:
                        issues.append(ValidationIssue(
                            file_path=str(settings_file),
                            issue_type="hardcoded_secret_key",
                            description="SECRET_KEY hardcoded em settings.py",
                            expected="SECRET_KEY deve vir de variável de ambiente",
                            actual="SECRET_KEY hardcoded",
                            severity="HIGH"
                        ))
                
                except Exception:
                    pass
                break
    
    # 3. Validar .gitignore para segurança
    gitignore_file = Path('.') / '.gitignore'
    if gitignore_file.exists():
        try:
            content = gitignore_file.read_text(encoding='utf-8', errors='ignore')
            
            # Arquivos/diretórios sensíveis que devem estar no .gitignore
            sensitive_patterns = [
                '.env',
                '*.key',
                '*.pem',
                'secrets/',
                '.vscode/settings.json' if '.vscode/' not in content else None
            ]
            
            missing_security = [p for p in sensitive_patterns if p and p not in content]
            if missing_security:
                issues.append(ValidationIssue(
                    file_path=str(gitignore_file),
                    issue_type="missing_security_gitignore",
                    description=f".gitignore sem exclusões de segurança: {', '.join(missing_security)}",
                    expected="Deve excluir arquivos sensíveis (.env, *.key, etc.)",
                    actual=f"Faltam: {', '.join(missing_security)}",
                    severity="MEDIUM"
                ))
        
        except Exception:
            pass
    
    # 4. Verificar se não há arquivos sensíveis commitados
    sensitive_files = ['.env', 'id_rsa', '*.key', 'secrets.json']
    for pattern in sensitive_files:
        matches = list(Path('.').glob(f'**/{pattern}'))
        for sensitive_file in matches:
            if sensitive_file.exists():
                issues.append(ValidationIssue(
                    file_path=str(sensitive_file),
                    issue_type="sensitive_file_committed",
                    description=f"Arquivo sensível pode estar no repositório: {sensitive_file.name}",
                    expected="Arquivos sensíveis devem estar no .gitignore",
                    actual=f"Arquivo sensível encontrado: {sensitive_file.name}",
                    severity="HIGH"
                ))
    
    return issues if issues else None

def validate_code_quality_configuration():
    '''Valida configurações de qualidade de código (linting, formatting, etc.).'''
    issues = []
    
    # Configurações de qualidade Python
    python_quality_configs = [
        {
            'patterns': ['.pylintrc', 'pylintrc', 'pyproject.toml'],
            'name': 'pylint configuration',
            'description': 'Configuração do Pylint',
            'severity': 'MEDIUM',
            'check_content': 'tool.pylint'
        },
        {
            'patterns': ['mypy.ini', '.mypy.ini', 'pyproject.toml'],
            'name': 'mypy configuration',
            'description': 'Configuração do MyPy para tipagem',
            'severity': 'MEDIUM',
            'check_content': 'mypy'
        },
        {
            'patterns': ['.coverage', '.coveragerc', 'pyproject.toml'],
            'name': 'coverage configuration',
            'description': 'Configuração de cobertura de testes',
            'severity': 'MEDIUM',
            'check_content': 'coverage'
        }
    ]
    
    # Verificar configurações Python
    for config in python_quality_configs:
        found = False
        for pattern in config['patterns']:
            config_file = Path('.') / pattern
            if config_file.exists():
                try:
                    content = config_file.read_text(encoding='utf-8', errors='ignore')
                    # Para pyproject.toml, verificar se tem seção específica
                    if pattern == 'pyproject.toml':
                        if config['check_content'] in content:
                            found = True
                    else:
                        found = True
                    
                    if found and not content.strip():
                        issues.append(ValidationIssue(
                            file_path=str(config_file),
                            issue_type="empty_quality_config",
                            description=f"Arquivo de qualidade {config['name']} está vazio",
                            expected=f"Arquivo deve conter {config['description']}",
                            actual="Arquivo vazio",
                            severity=config['severity']
                        ))
                except Exception:
                    pass
                if found:
                    break
    
    # Configurações de qualidade JavaScript/TypeScript
    frontend_quality_configs = [
        {
            'patterns': ['.eslintrc.js', '.eslintrc.json', '.eslintrc.ts', 'eslint.config.js'],
            'name': 'ESLint configuration',
            'description': 'Configuração do ESLint',
            'severity': 'MEDIUM'
        },
        {
            'patterns': ['.prettierrc', '.prettierrc.json', '.prettierrc.js', 'prettier.config.js'],
            'name': 'Prettier configuration',
            'description': 'Configuração do Prettier',
            'severity': 'MEDIUM'
        }
    ]
    
    # Buscar diretório frontend primeiro
    frontend_dir = None
    for pattern in ['**/frontend/', '**/web/', '**/client/']:
        matches = list(Path('.').glob(pattern))
        for match in matches:
            if match.is_dir() and (match / 'package.json').exists():
                frontend_dir = match
                break
        if frontend_dir:
            break
    
    # Se não encontrou diretório específico, procurar na raiz
    if not frontend_dir and Path('.').glob('package.json'):
        frontend_dir = Path('.')
    
    if frontend_dir:
        for config in frontend_quality_configs:
            found = False
            for pattern in config['patterns']:
                config_file = frontend_dir / pattern
                if config_file.exists():
                    found = True
                    try:
                        content = config_file.read_text(encoding='utf-8', errors='ignore').strip()
                        if not content:
                            issues.append(ValidationIssue(
                                file_path=str(config_file),
                                issue_type="empty_frontend_quality_config",
                                description=f"Arquivo {config['name']} está vazio",
                                expected=f"Arquivo deve conter {config['description']}",
                                actual="Arquivo vazio",
                                severity=config['severity']
                            ))
                    except Exception:
                        pass
                    break
    
    # Verificar pre-commit hooks
    precommit_configs = ['.pre-commit-config.yaml', '.pre-commit-config.yml']
    precommit_found = False
    
    for pattern in precommit_configs:
        precommit_file = Path('.') / pattern
        if precommit_file.exists():
            precommit_found = True
            try:
                content = precommit_file.read_text(encoding='utf-8', errors='ignore')
                
                # Verificar se tem hooks essenciais
                essential_hooks = ['trailing-whitespace', 'end-of-file-fixer', 'black', 'flake8']
                missing_hooks = [hook for hook in essential_hooks if hook not in content]
                
                if len(missing_hooks) > 2:
                    issues.append(ValidationIssue(
                        file_path=str(precommit_file),
                        issue_type="incomplete_precommit_hooks",
                        description=f"Pre-commit hooks incompletos - faltam: {', '.join(missing_hooks)}",
                        expected="Deve incluir hooks essenciais (trailing-whitespace, black, flake8)",
                        actual=f"Faltam: {', '.join(missing_hooks)}",
                        severity="MEDIUM"
                    ))
            except Exception:
                pass
            break
    
    # Verificar se há pelo menos algumas configurações de qualidade
    has_python_quality = any((Path('.') / pattern).exists() for config in python_quality_configs for pattern in config['patterns'])
    has_frontend_quality = False
    if frontend_dir:
        has_frontend_quality = any((frontend_dir / pattern).exists() for config in frontend_quality_configs for pattern in config['patterns'])
    
    if not has_python_quality and not has_frontend_quality and not precommit_found:
        issues.append(ValidationIssue(
            file_path="quality-configs",
            issue_type="no_quality_configuration",
            description="Nenhuma configuração de qualidade de código encontrada",
            expected="Deve ter ao menos configurações básicas de linting/formatting",
            actual="Nenhuma configuração de qualidade encontrada",
            severity="MEDIUM"
        ))
    
    return issues if issues else None

def validate_readme_md():
    '''Valida existência de README.md.'''
    issues = []
    
    doc_paths = list(Path('.').rglob('**/README.md'))
    if not doc_paths:
        # Tentar variações case-insensitive
        alt_paths = list(Path('.').rglob('**/readme.md'))
        if not alt_paths:
            issues.append(ValidationIssue(
                file_path="README.md",
                issue_type="missing_documentation",
                description="Documentação essencial não encontrada: README.md",
                expected="Arquivo deve existir na raiz do projeto",
                actual="Arquivo não existe",
                severity="MEDIUM"
            ))
    
    return issues if issues else None

def validate_license():
    '''Valida existência de LICENSE.'''
    issues = []
    
    doc_paths = list(Path('.').rglob('**/LICENSE'))
    if not doc_paths:
        # Tentar variações case-insensitive
        alt_paths = list(Path('.').rglob('**/license'))
        if not alt_paths:
            issues.append(ValidationIssue(
                file_path="LICENSE",
                issue_type="missing_documentation",
                description="Documentação essencial não encontrada: LICENSE",
                expected="Arquivo deve existir na raiz do projeto",
                actual="Arquivo não existe",
                severity="MEDIUM"
            ))
    
    return issues if issues else None

def validate_changelog_md():
    '''Valida existência de CHANGELOG.md.'''
    issues = []
    
    doc_paths = list(Path('.').rglob('**/CHANGELOG.md'))
    if not doc_paths:
        # Tentar variações case-insensitive
        alt_paths = list(Path('.').rglob('**/changelog.md'))
        if not alt_paths:
            issues.append(ValidationIssue(
                file_path="CHANGELOG.md",
                issue_type="missing_documentation",
                description="Documentação essencial não encontrada: CHANGELOG.md",
                expected="Arquivo deve existir na raiz do projeto",
                actual="Arquivo não existe",
                severity="MEDIUM"
            ))
    
    return issues if issues else None

def validate_contributing_md():
    '''Valida existência de CONTRIBUTING.md.'''
    issues = []
    
    doc_paths = list(Path('.').rglob('**/CONTRIBUTING.md'))
    if not doc_paths:
        # Tentar variações case-insensitive
        alt_paths = list(Path('.').rglob('**/contributing.md'))
        if not alt_paths:
            issues.append(ValidationIssue(
                file_path="CONTRIBUTING.md",
                issue_type="missing_documentation",
                description="Documentação essencial não encontrada: CONTRIBUTING.md",
                expected="Arquivo deve existir na raiz do projeto",
                actual="Arquivo não existe",
                severity="MEDIUM"
            ))
    
    return issues if issues else None

def validate_readme_content_specific():
    '''Valida README.md COMPLETO conforme Blueprint seção 9 (certeza absoluta).'''
    issues = []
    
    readme_paths = list(Path('.').rglob('**/README.md'))
    if not readme_paths:
        return None  # Já validado em outra regra
    
    readme_file = readme_paths[0]
    content = readme_file.read_text(encoding='utf-8', errors='ignore')
    
    # Estrutura EXATA esperada do Blueprint seção 9
    expected_blueprint_structure = [
        # Título e badges obrigatórios
        '# IABANK',
        '[![Status]',
        '[![CI/CD]', 
        '[![License]',
        
        # Seções estruturais obrigatórias 
        '## Sobre o Projeto',
        'Sistema de gestão de empréstimos',
        'plataforma Web SaaS',
        'multi-tenant',
        
        '## Stack Tecnológica',
        '**Backend:** Python',
        '**Frontend:** React',
        '**Banco de Dados:** PostgreSQL',
        '**Cache & Fila de Tarefas:** Redis, Celery',
        '**Containerização:** Docker',
        
        '## Como Começar',
        '### Pré-requisitos',
        'Docker e Docker Compose',
        'Node.js e pnpm',
        'Python e Poetry',
        
        '### Instalação e Execução',
        'git clone',
        '.env.example',
        'docker-compose up',
        'http://localhost:5173',
        'http://localhost:8000/api/',
        
        '## Como Executar os Testes',
        'docker-compose exec backend',
        'pytest'
    ]
    
    # Validação CRÍTICA: elementos essenciais
    critical_missing = []
    important_missing = []
    
    critical_elements = [
        '# IABANK', '## Sobre o Projeto', '## Stack Tecnológica', 
        '## Como Começar', 'Docker', 'docker-compose'
    ]
    
    important_elements = [
        'Python', 'React', 'PostgreSQL', 'Redis', 'git clone',
        'pytest', '[![', 'multi-tenant', 'SaaS'
    ]
    
    # Verificar elementos críticos
    for element in critical_elements:
        if element not in content:
            critical_missing.append(element)
    
    # Verificar elementos importantes
    for element in important_elements:
        if element not in content:
            important_missing.append(element)
    
    # Reportar ausências críticas
    for missing in critical_missing:
        issues.append(ValidationIssue(
            file_path=str(readme_file),
            issue_type="missing_critical_readme_element",
            description=f"Elemento CRÍTICO ausente no README: {missing}",
            expected=f"Elemento '{missing}' é OBRIGATÓRIO conforme Blueprint seção 9",
            actual="Elemento crítico não encontrado",
            severity="HIGH"
        ))
    
    # Reportar ausências importantes (completude)
    if len(important_missing) > 3:
        issues.append(ValidationIssue(
            file_path=str(readme_file),
            issue_type="incomplete_readme_content",
            description=f"README incompleto: {len(important_missing)} elementos Blueprint ausentes",
            expected="Conteúdo completo do Blueprint seção 9 deve estar presente",
            actual=f"Faltam elementos: {', '.join(important_missing[:3])}...",
            severity="MEDIUM"
        ))
    
    # Validar estrutura de seções (ordem e hierarquia)
    lines = content.split('\n')
    h1_found = any(line.startswith('# ') for line in lines)
    h2_count = sum(1 for line in lines if line.startswith('## '))
    
    if not h1_found:
        issues.append(ValidationIssue(
            file_path=str(readme_file),
            issue_type="missing_main_title",
            description="README sem título principal (# IABANK)",
            expected="Título principal '# IABANK' conforme Blueprint",
            actual="Nenhum título H1 encontrado",
            severity="HIGH"
        ))
    
    if h2_count < 4:  # Mínimo de seções esperadas
        issues.append(ValidationIssue(
            file_path=str(readme_file),
            issue_type="insufficient_readme_sections",
            description=f"README com poucas seções: {h2_count} encontradas",
            expected="Mínimo 4 seções principais conforme Blueprint",
            actual=f"Apenas {h2_count} seções H2 encontradas",
            severity="MEDIUM"
        ))
    
    return issues if issues else None

def validate_Dockerfile():
    '''Valida arquivo Docker: Dockerfile.'''
    issues = []
    
    docker_paths = list(Path('.').rglob('**/Dockerfile'))
    if not docker_paths:
        issues.append(ValidationIssue(
            file_path="Dockerfile",
            issue_type="missing_docker_file",
            description="Arquivo Docker não encontrado: Dockerfile",
            expected="Arquivo deve existir para containerização",
            actual="Arquivo não existe",
            severity="MEDIUM"
        ))
    
    return issues if issues else None

def validate_development_quality_tools():
    '''Valida ferramentas de qualidade de código.'''
    issues = []
    
    # Verificar pre-commit
    precommit_paths = list(Path('.').rglob('**/.pre-commit-config.yaml'))
    if not precommit_paths:
        issues.append(ValidationIssue(
            file_path=".pre-commit-config.yaml",
            issue_type="missing_precommit_config",
            description="Configuração pre-commit não encontrada",
            expected="Arquivo .pre-commit-config.yaml deve existir",
            actual="Arquivo não existe",
            severity="MEDIUM"
        ))
    
    # Verificar gitignore
    gitignore_paths = list(Path('.').rglob('**/.gitignore'))
    if not gitignore_paths:
        issues.append(ValidationIssue(
            file_path=".gitignore",
            issue_type="missing_gitignore",
            description="Arquivo .gitignore não encontrado",
            expected="Arquivo .gitignore deve existir",
            actual="Arquivo não existe",
            severity="HIGH"
        ))
    
    return issues if issues else None

def validate_python_files_docstrings():
    '''Valida QUALIDADE de docstrings conforme instruções scaffolder (certeza absoluta).'''
    issues = []
    
    # Tipos de arquivos Python que devem ter docstrings obrigatórias
    python_file_types = ['views.py', 'services.py', 'serializers.py', 'urls.py', 'apps.py', 'models.py']
    
    for file_type in python_file_types:
        python_files = list(Path('.').rglob(f'**/{file_type}'))
        # Filtrar apenas arquivos em apps Django (têm __init__.py no diretório)
        django_files = [f for f in python_files if (f.parent / '__init__.py').exists()]
        
        for python_file in django_files:
            if python_file.exists():
                content = python_file.read_text(encoding='utf-8', errors='ignore').strip()
                
                # Extrair docstring de módulo
                lines = content.split('\n')
                docstring_content = None
                docstring_found = False
                
                for i, line in enumerate(lines):
                    line = line.strip()
                    if line.startswith(chr(34)*3) or line.startswith(chr(39)*3):
                        docstring_found = True
                        # Extrair conteúdo completo da docstring
                        quote_type = chr(34)*3 if line.startswith(chr(34)*3) else chr(39)*3
                        docstring_start = i
                        docstring_lines = []
                        
                        # Encontrar fim da docstring
                        for j in range(i, len(lines)):
                            if quote_type in lines[j] and j > i:
                                docstring_lines = lines[docstring_start:j+1]
                                break
                        
                        if docstring_lines:
                            docstring_content = '\n'.join(docstring_lines)
                        break
                    elif (not line.startswith('from ') and 
                          not line.startswith('import ') and 
                          not line.startswith('#') and
                          line):
                        break  # Chegou ao código, parar de procurar
                
                # VALIDAÇÃO 1: Existência da docstring
                if not docstring_found:
                    issues.append(ValidationIssue(
                        file_path=str(python_file),
                        issue_type="missing_python_docstring",
                        description=f"Arquivo Python sem docstring de módulo: {python_file.name}",
                        expected="Docstring obrigatória conforme prompt scaffolder: 'explique seu propósito na arquitetura'",
                        actual="Docstring de módulo não encontrada",
                        severity="HIGH"
                    ))
                    continue
                
                # VALIDAÇÃO 2: Qualidade e adequação da docstring
                if docstring_content:
                    # Palavras-chave que devem aparecer para explicar propósito arquitetural
                    purpose_keywords = [
                        'módulo', 'app', 'aplicação', 'sistema', 'componente',
                        'gerencia', 'controla', 'define', 'implementa', 'contém'
                    ]
                    
                    architecture_keywords = [
                        'arquitetura', 'estrutura', 'framework', 'Django', 'modelo',
                        'view', 'serializer', 'service', 'API', 'endpoint'
                    ]
                    
                    docstring_lower = docstring_content.lower()
                    
                    # Verificar se explica propósito
                    has_purpose = any(keyword in docstring_lower for keyword in purpose_keywords)
                    has_architecture_context = any(keyword in docstring_lower for keyword in architecture_keywords)
                    
                    # Verificar tamanho mínimo (deve ser descritiva)
                    word_count = len(docstring_content.split())
                    
                    if word_count < 5:
                        issues.append(ValidationIssue(
                            file_path=str(python_file),
                            issue_type="insufficient_docstring_content",
                            description=f"Docstring muito curta em {python_file.name}: {word_count} palavras",
                            expected="Docstring deve explicar propósito na arquitetura conforme scaffolder",
                            actual=f"Apenas {word_count} palavras, insuficiente",
                            severity="MEDIUM"
                        ))
                    
                    if not has_purpose and not has_architecture_context:
                        issues.append(ValidationIssue(
                            file_path=str(python_file),
                            issue_type="inadequate_docstring_content",
                            description=f"Docstring inadequada em {python_file.name}: não explica propósito arquitetural",
                            expected="Docstring deve explicar 'seu propósito na arquitetura' conforme prompt scaffolder",
                            actual="Docstring não menciona propósito ou contexto arquitetural",
                            severity="MEDIUM"
                        ))
                
                # VALIDAÇÃO 3: Posicionamento correto (primeiro elemento após imports)
                non_import_lines = [line for line in lines if line.strip() and 
                                  not line.strip().startswith('from ') and 
                                  not line.strip().startswith('import ') and
                                  not line.strip().startswith('#')]
                
                if non_import_lines and not non_import_lines[0].strip().startswith(chr(34)*3):
                    if not non_import_lines[0].strip().startswith(chr(39)*3):
                        issues.append(ValidationIssue(
                            file_path=str(python_file),
                            issue_type="misplaced_docstring",
                            description=f"Docstring mal posicionada em {python_file.name}",
                            expected="Docstring deve ser primeiro elemento após imports",
                            actual="Docstring não está no início do código",
                            severity="MEDIUM"
                        ))
    
    return issues if issues else None

def validate_detailed_frontend_structure():
    '''Valida estrutura frontend COMPLETA conforme Blueprint seção 4 (certeza absoluta).'''
    issues = []
    
    # Buscar diretório frontend
    frontend_src = None
    for src_path in Path('.').rglob('**/src/'):
        parent = src_path.parent
        if (parent / 'package.json').exists():
            frontend_src = src_path
            break
    
    if not frontend_src:
        issues.append(ValidationIssue(
            file_path="frontend/src/",
            issue_type="missing_frontend_directory",
            description="Diretório frontend/src/ não encontrado",
            expected="Estrutura frontend completa conforme Blueprint seção 4",
            actual="Diretório frontend não existe",
            severity="CRITICAL"
        ))
        return issues
    
    # Estrutura EXATA esperada do Blueprint seção 4
    expected_structure = {
        'app/': [
            # Configuração global da aplicação (providers, store, router, styles)
        ],
        'pages/': [
            # Componentes de página, que compõem layouts a partir das features
        ],
        'features/': [
            # Funcionalidades de negócio (ex: loan-list, customer-form)
            'loan-list/', 'customer-form/'
        ],
        'entities/': [
            # Componentes e lógica de entidades de negócio (ex: LoanCard, CustomerAvatar)
        ],
        'shared/': [
            'api/',      # Configuração do cliente Axios/Fetch global
            'config/',   # Constantes, configurações de ambiente
            'lib/',      # Funções utilitárias, helpers, hooks genéricos
            'ui/'        # Biblioteca de componentes de UI puros (Button, Input, Table)
        ]
    }
    
    # Validar estrutura principal obrigatória
    for main_dir in expected_structure.keys():
        dir_path = frontend_src / main_dir
        if not dir_path.exists():
            issues.append(ValidationIssue(
                file_path=str(dir_path),
                issue_type="missing_frontend_main_directory",
                description=f"Diretório principal ausente: {main_dir}",
                expected=f"Diretório '{main_dir}' é OBRIGATÓRIO conforme Blueprint seção 4",
                actual="Diretório principal não existe",
                severity="HIGH"
            ))
        else:
            # Validar subdiretórios específicos para shared/
            if main_dir == 'shared/' and expected_structure[main_dir]:
                for sub_dir in expected_structure[main_dir]:
                    sub_path = dir_path / sub_dir
                    if not sub_path.exists():
                        issues.append(ValidationIssue(
                            file_path=str(sub_path),
                            issue_type="missing_frontend_sub_directory",
                            description=f"Subdiretório shared ausente: {sub_dir}",
                            expected=f"Subdiretório shared/{sub_dir} conforme Blueprint",
                            actual="Subdiretório não existe",
                            severity="MEDIUM"
                        ))
    
    # Validar arquivos React principais (se existem e têm comentários)
    main_files = ['App.tsx', 'main.tsx', 'index.tsx']
    for main_file in main_files:
        file_path = frontend_src / main_file
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            # Verificar se é apenas arquivo com comentário (escopo scaffolder)
            lines = content.strip().split('\n')[:5]
            has_substantial_content = any(
                line.strip() and 
                not line.strip().startswith('//') and 
                not line.strip().startswith('/*') and
                not line.strip().startswith('*') and
                not line.strip().startswith('import') and
                not line.strip().startswith('export')
                for line in lines
            )
            
            # Para scaffolder, arquivos devem ter principalmente comentários
            if has_substantial_content:
                # Isso é bom - mas vamos verificar se ainda tem comentário
                has_comment = any(
                    line.strip().startswith('//') or 
                    line.strip().startswith('/*') or
                    line.strip().startswith('*')
                    for line in lines
                )
                
                if not has_comment:
                    issues.append(ValidationIssue(
                        file_path=str(file_path),
                        issue_type="missing_react_header_comment",
                        description=f"Arquivo React principal sem comentário: {main_file}",
                        expected="Comentário de cabeçalho conforme prompt scaffolder",
                        actual="Nenhum comentário encontrado",
                        severity="MEDIUM"
                    ))
    
    return issues if issues else None

def validate_scaffolder_prompt_compliance():
    '''Valida conformidade REAL com agv-scaffolder (ZERO implementação).'''
    issues = []
    
    # REGRA 1: Arquivos de código devem ter APENAS docstring
    critical_files = ['models.py', 'views.py', 'services.py', 'serializers.py']
    
    for file_type in critical_files:
        python_files = list(Path('.').rglob(f'**/{file_type}'))
        django_files = [f for f in python_files if (f.parent / '__init__.py').exists()]
        
        for python_file in django_files:
            if python_file.exists():
                content = python_file.read_text(encoding='utf-8', errors='ignore')
                lines = content.strip().split('\n')
                
                # Validar se tem APENAS docstring conforme agv-scaffolder
                non_empty_lines = [line for line in lines if line.strip()]
                
                if not non_empty_lines:
                    continue
                
                # Deve começar com docstring
                first_line = non_empty_lines[0].strip()
                if not (first_line.startswith('"""') or first_line.startswith("'''")):
                    issues.append(ValidationIssue(
                        file_path=str(python_file),
                        issue_type="missing_scaffold_docstring",
                        description=f"Arquivo {file_type} deve começar apenas com docstring",
                        expected="APENAS docstring de módulo conforme agv-scaffolder",
                        actual="Arquivo não começa com docstring ou contém código",
                        severity="HIGH"
                    ))
                    continue
                
                # Encontrar fim da docstring
                quote_type = '"""' if first_line.startswith('"""') else "'''"
                docstring_end = -1
                
                for i, line in enumerate(lines):
                    if quote_type in line and i > 0:
                        docstring_end = i
                        break
                
                # CRÍTICO: Verificar se há QUALQUER código após docstring  
                if docstring_end != -1:
                    remaining_lines = lines[docstring_end + 1:]
                    code_after_docstring = [
                        line.strip() for line in remaining_lines 
                        if line.strip() and not line.strip().startswith('#')
                    ]
                    
                    if code_after_docstring:
                        issues.append(ValidationIssue(
                            file_path=str(python_file),
                            issue_type="excessive_implementation_for_scaffold",
                            description=f"Arquivo {file_type} contém código além da docstring",
                            expected="APENAS docstring conforme agv-scaffolder - ZERO implementação",
                            actual=f"Arquivo contém {len(code_after_docstring)} linhas de código proibido",
                            severity="HIGH"
                        ))
    
    # REGRA 2: README conforme Blueprint seção 9 (NÃO hardcoded)
    readme_paths = list(Path('.').rglob('**/README.md'))
    if readme_paths:
        content = readme_paths[0].read_text(encoding='utf-8', errors='ignore')
        
        # Elementos REAIS do Blueprint seção 9 (não hardcoded)
        blueprint_elements = [
            '# IABANK',
            'Sistema de gestão de empréstimos',
            '## Stack Tecnológica',
            'Docker',
            '### Instalação e Execução',  # NÃO 'setup'
            'docker-compose up',
            '## Como Executar os Testes'
        ]
        
        missing_elements = [elem for elem in blueprint_elements if elem not in content]
        
        if missing_elements:
            issues.append(ValidationIssue(
                file_path=str(readme_paths[0]),
                issue_type="missing_blueprint_readme_elements",
                description=f"README não segue Blueprint seção 9: {len(missing_elements)} elementos ausentes",
                expected="README conforme Blueprint seção 9 exato",
                actual=f"Elementos ausentes: {', '.join(missing_elements[:3])}...",
                severity="MEDIUM"
            ))
    
    # REGRA 3: Estrutura de testes deve existir mas sem implementação
    test_dirs = list(Path('.').rglob('**/tests/'))
    if not test_dirs:
        issues.append(ValidationIssue(
            file_path="tests/",
            issue_type="missing_test_structure",
            description="Estrutura de testes não encontrada",
            expected="Scaffolder deve criar estrutura de testes conforme Blueprint",
            actual="Nenhum diretório tests/ encontrado",
            severity="MEDIUM"
        ))
    
    return issues if issues else None

class BlueprintArquiteturalIabankScaffoldValidator:
    """Validador especializado para scaffold completo (Alvo 0)."""

    SEVERITY_WEIGHTS = {
        "CRITICAL": 15,
        "HIGH": 8,
        "MEDIUM": 2,
        "LOW": 1
    }

    CATEGORY_WEIGHTS = {
        "STRUCTURE": 1.0,
        "CONTENT": 1.5,
        "MODELS": 2.0,
        "DEPENDENCIES": 1.2,
        "API": 1.3
    }

    def __init__(self):
        self.validation_methods = [
            "validate_directory_structure",
            "validate_gitignore_content",
            "validate_pyproject_content",
            "validate_precommit_config_content",
            "validate_env_example_file",
            "validate_content_settings_py",
            "validate_content_models_py",
            "validate_content_pyproject_toml",
            "validate_dependency_django",
            "validate_dependency_djangorestframework",
            "validate_dependency_psycopg2_binary",
            "validate_django_settings_advanced",
            "validate_multi_tenancy_implementation",
            "validate_all_blueprint_models",
            "validate_model_files_docstrings",
            "validate_django_apps_structure",
            "validate_github_actions_pipeline",
            "validate_complete_test_structure",
            "validate_django_core_files",
            "validate_frontend_dependencies_complete",
            "validate_backend_dependencies_complete",
            "validate_frontend_core_files",
            "validate_docker_complete_configuration",
            "validate_specific_directory_structure",
            "validate_ide_configuration_files",
            "validate_security_best_practices",
            "validate_code_quality_configuration",
            "validate_readme_md",
            "validate_license",
            "validate_changelog_md",
            "validate_contributing_md",
            "validate_readme_content_specific",
            "validate_Dockerfile",
            "validate_development_quality_tools",
            "validate_python_files_docstrings",
            "validate_detailed_frontend_structure",
            "validate_scaffolder_prompt_compliance",
        ]

        self.rule_categories = {
            "validate_directory_structure": "STRUCTURE",
            "validate_gitignore_content": "CONTENT",
            "validate_pyproject_content": "CONTENT",
            "validate_precommit_config_content": "CONTENT",
            "validate_env_example_file": "STRUCTURE",
            "validate_content_settings_py": "CONTENT",
            "validate_content_models_py": "CONTENT",
            "validate_content_pyproject_toml": "CONTENT",
            "validate_dependency_django": "DEPENDENCIES",
            "validate_dependency_djangorestframework": "DEPENDENCIES",
            "validate_dependency_psycopg2_binary": "DEPENDENCIES",
            "validate_django_settings_advanced": "CONTENT",
            "validate_multi_tenancy_implementation": "MODELS",
            "validate_all_blueprint_models": "MODELS",
            "validate_model_files_docstrings": "CONTENT",
            "validate_django_apps_structure": "STRUCTURE",
            "validate_github_actions_pipeline": "STRUCTURE",
            "validate_complete_test_structure": "STRUCTURE",
            "validate_django_core_files": "STRUCTURE",
            "validate_frontend_dependencies_complete": "DEPENDENCIES",
            "validate_backend_dependencies_complete": "DEPENDENCIES",
            "validate_frontend_core_files": "STRUCTURE",
            "validate_docker_complete_configuration": "STRUCTURE",
            "validate_specific_directory_structure": "STRUCTURE",
            "validate_ide_configuration_files": "CONTENT",
            "validate_security_best_practices": "CONTENT",
            "validate_code_quality_configuration": "CONTENT",
            "validate_readme_md": "CONTENT",
            "validate_license": "CONTENT",
            "validate_changelog_md": "CONTENT",
            "validate_contributing_md": "CONTENT",
            "validate_readme_content_specific": "CONTENT",
            "validate_Dockerfile": "STRUCTURE",
            "validate_development_quality_tools": "STRUCTURE",
            "validate_python_files_docstrings": "CONTENT",
            "validate_detailed_frontend_structure": "STRUCTURE",
            "validate_scaffolder_prompt_compliance": "CONTENT",
        }

    def validate(self) -> ValidationResults:
        """Executa todas as validações e retorna os resultados."""
        issues = []
        total_checks = len(self.validation_methods)
        failed_validations = 0
        categories = {"STRUCTURE": 0, "CONTENT": 0, "MODELS": 0, "DEPENDENCIES": 0, "API": 0}

        print(f"Executando {total_checks} validações especializadas...")
        print("Níveis: STRUCTURE | CONTENT | MODELS | DEPENDENCIES | API")
        print("-" * 80)

        for method_name in self.validation_methods:
            try:
                method = globals()[method_name]
                result = method()

                category = self.rule_categories.get(method_name, "STRUCTURE")
                print(f"[{category:12}] {method_name}", end="")

                if result:
                    failed_validations += 1
                    if isinstance(result, list):
                        issues.extend(result)
                        categories[category] += len(result)
                        print(f" FALHOU: {len(result)} problemas")
                    else:
                        issues.append(result)
                        categories[category] += 1
                        print(" FALHOU: 1 problema")
                else:
                    print(" OK")

            except Exception as e:
                failed_validations += 1
                issues.append(ValidationIssue(
                    file_path="validator",
                    issue_type="validation_error",
                    description=f"Erro na validação {method_name}: {str(e)}",
                    expected="Validação deve executar sem erros",
                    actual=f"Erro: {str(e)}",
                    severity="CRITICAL"
                ))
                print(f" ERRO: {str(e)}")

        passed_checks = total_checks - failed_validations
        score = self._calculate_score(total_checks, failed_validations, issues)

        return ValidationResults(
            total_checks=total_checks,
            passed_checks=passed_checks,
            failed_checks=failed_validations,
            issues=issues,
            score=score,
            categories=categories
        )

    def _calculate_score(self, total_checks: int, failed_validations: int, issues: List[ValidationIssue]) -> float:
        """Calcula score baseado na severidade e categoria dos problemas."""
        if failed_validations == 0:
            return 100.0

        total_penalty = 0
        for issue in issues:
            severity_weight = self.SEVERITY_WEIGHTS.get(issue.severity, 1)
            category_weight = 1.0

            if "model" in issue.issue_type.lower():
                category_weight = self.CATEGORY_WEIGHTS["MODELS"]
            elif "content" in issue.issue_type.lower() or "config" in issue.issue_type.lower():
                category_weight = self.CATEGORY_WEIGHTS["CONTENT"]
            elif "api" in issue.issue_type.lower():
                category_weight = self.CATEGORY_WEIGHTS["API"]
            elif "dependency" in issue.issue_type.lower():
                category_weight = self.CATEGORY_WEIGHTS["DEPENDENCIES"]
            else:
                category_weight = self.CATEGORY_WEIGHTS["STRUCTURE"]

            penalty = severity_weight * category_weight
            total_penalty += penalty

        base_score = ((total_checks - failed_validations) / total_checks) * 100
        penalty_factor = min(total_penalty / (failed_validations * 10), 0.5)
        final_score = max(0, base_score - (base_score * penalty_factor))

        return round(final_score, 2)

    def generate_report(self, results: ValidationResults) -> str:
        """Gera relatório detalhado dos resultados."""
        report = []
        report.append("=" * 100)
        report.append(f"RELATÓRIO DE VALIDAÇÃO - VALIDADOR ESPECIALIZADO PARA SCAFFOLD COMPLETO (ALVO 0)")
        report.append("=" * 100)
        report.append(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Validador: BlueprintArquiteturalIabankScaffoldValidator")
        report.append("")
        report.append("RESULTADOS:")
        report.append(f"├─ Total de Verificações: {results.total_checks}")
        report.append(f"├─ Aprovadas: {results.passed_checks}")
        report.append(f"├─ Reprovadas: {results.failed_checks}")
        report.append(f"└─ Score Final: {results.score}%")
        report.append("")

        # Análise por categoria
        report.append("ANÁLISE POR CATEGORIA:")
        for category, count in results.categories.items():
            status = "FALHOU" if count > 0 else "OK"
            report.append(f"|- {status} {category:12}: {count} problemas")
        report.append("")

        # Status
        if results.score >= 90:
            report.append("STATUS: EXCELENTE")
        elif results.score >= 85:
            report.append("STATUS: APROVADO")
        elif results.score >= 70:
            report.append("STATUS: NECESSITA MELHORIAS")
        else:
            report.append("STATUS: REJEITADO")

        report.append("")

        if results.issues:
            # Agrupar por severidade
            critical_issues = [i for i in results.issues if i.severity == "CRITICAL"]
            high_issues = [i for i in results.issues if i.severity == "HIGH"]
            medium_issues = [i for i in results.issues if i.severity == "MEDIUM"]
            low_issues = [i for i in results.issues if i.severity == "LOW"]

            if critical_issues:
                report.append("PROBLEMAS CRÍTICOS:")
                report.append("-" * 60)
                for i, issue in enumerate(critical_issues, 1):
                    report.append(f"{i}. {issue.description}")
                    report.append(f"   Arquivo: {issue.file_path}")
                    report.append(f"   Esperado: {issue.expected}")
                    report.append(f"   Encontrado: {issue.actual}")
                    report.append("")

            if high_issues:
                report.append("PROBLEMAS DE ALTA PRIORIDADE:")
                report.append("-" * 60)
                for i, issue in enumerate(high_issues, 1):
                    report.append(f"{i}. {issue.description}")
                    report.append(f"   Arquivo: {issue.file_path}")
                    report.append("")

            if medium_issues:
                report.append("PROBLEMAS DE MÉDIA PRIORIDADE:")
                report.append("-" * 60)
                for i, issue in enumerate(medium_issues, 1):
                    report.append(f"{i}. {issue.description}")
                    report.append("")

            if low_issues:
                report.append("PROBLEMAS DE BAIXA PRIORIDADE:")
                report.append("-" * 60)
                for i, issue in enumerate(low_issues, 1):
                    report.append(f"{i}. {issue.description}")
                    report.append("")

        report.append("=" * 100)
        return "\n".join(report)

def main():
    """Função principal do validador."""
    import os
    import sys
    
    # Configurar encoding para Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    validator = BlueprintArquiteturalIabankScaffoldValidator()
    results = validator.validate()

    # Gerar e exibir relatório
    report = validator.generate_report(results)
    print()
    
    # Exibir relatório com tratamento de encoding
    try:
        print(report)
    except UnicodeEncodeError:
        # Fallback para encoding seguro
        safe_report = report.encode('utf-8', errors='replace').decode('utf-8')
        print(safe_report)

    # Salvar resultados em JSON
    results_file = Path(r"agv-outputs\resultados\results_scaffold_20250902_180223.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)
    results_file.write_text(
        json.dumps(results.to_dict(), indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f"\nRelatório detalhado salvo em: {results_file}")

    return 0 if results.score >= 75 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)