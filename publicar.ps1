# publicar.ps1 — Autentica no GitHub, cria repositório e faz push
# Execute: clique direito > "Executar com PowerShell"

$machinePath = [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
$userPath    = [System.Environment]::GetEnvironmentVariable("PATH", "User")
$env:PATH    = "$machinePath;$userPath"

$REPO_NAME = "dashboard-pp-colaboradores"
$REPO_DESC = "Dashboard PP Colaboradores V2 - FarmaNello"

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  FarmaNello — Publicar Dashboard no GitHub" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Etapa 1: Login GitHub
Write-Host "ETAPA 1: Login no GitHub" -ForegroundColor Yellow
Write-Host "Uma janela do navegador vai abrir. Autorize o acesso." -ForegroundColor Gray
Write-Host ""
gh auth login --web --git-protocol https

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Login falhou. Tente novamente." -ForegroundColor Red
    Read-Host "Pressione Enter para fechar"
    exit 1
}

Write-Host ""
Write-Host "Login realizado com sucesso!" -ForegroundColor Green
Write-Host ""

# Etapa 2: Criar repositório privado
Write-Host "ETAPA 2: Criando repositório privado '$REPO_NAME'..." -ForegroundColor Yellow
gh repo create $REPO_NAME --private --description $REPO_DESC --source . --remote origin --push

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Repositório pode já existir. Tentando adicionar remote e fazer push..." -ForegroundColor Yellow
    $username = (gh api user --jq '.login')
    git remote remove origin 2>$null
    git remote add origin "https://github.com/$username/$REPO_NAME.git"
    git push -u origin master
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  SUCESSO! Código publicado no GitHub." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

$username = (gh api user --jq '.login')
Write-Host "Repositório: https://github.com/$username/$REPO_NAME" -ForegroundColor Cyan
Write-Host ""
Write-Host "PRÓXIMO PASSO: Configure o deploy no Render." -ForegroundColor Yellow
Write-Host "Siga as instruções em: PROJETOS\dashboard_pp_colaboradores\DEPLOY.md" -ForegroundColor Yellow
Write-Host ""
Read-Host "Pressione Enter para fechar"
