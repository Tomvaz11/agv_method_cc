@echo off
echo ===== Preparando ambiente para trabalhar =====
echo.

echo 0. Verificando se o repositorio Git esta configurado...
git remote -v | findstr "origin" > nul
if %errorlevel% neq 0 (
    echo Configurando o repositorio remoto...
    git remote add origin https://github.com/Tomvaz11/agv_method_cc.git
)

echo 1. Mudando para o branch master...
git checkout master 2>nul
if %errorlevel% neq 0 (
    echo Branch master nao existe localmente. Criando branch master...
    git checkout -b master
)

echo 2. Obtendo a versao mais recente do codigo...
git pull origin master --allow-unrelated-histories 2>nul
if %errorlevel% neq 0 (
    echo NOTA: Nao foi possivel obter a versao mais recente.
    echo Isso e normal se este for o primeiro uso ou se o repositorio remoto estiver vazio.
)
echo.

echo ===== PRONTO PARA TRABALHAR! =====
echo Voce esta trabalhando no branch master do projeto AGV Method CC.
echo Faca suas alteracoes e depois execute o script "atualizar-github.bat"
echo.
pause
