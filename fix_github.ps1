# fix_github.ps1
Write-Host "🚀 Fixing SR Fashion GitHub Repository" -ForegroundColor Yellow

# Go to your project folder
cd C:\Users\SR\Desktop\BusyWinApp

# 1. First, export fresh data from BusyWin
Write-Host "📊 Exporting fresh data from BusyWin..." -ForegroundColor Cyan
python export_items.py

# 2. Copy the new index.html to root
Write-Host "📝 Copying new POS interface..." -ForegroundColor Cyan
Copy-Item .\templates\index.html .\index.html -Force

# 3. Add all files to git
Write-Host "📦 Adding files to Git..." -ForegroundColor Cyan
git add .
git add -f index.html items.json

# 4. Commit the changes
Write-Host "💾 Committing changes..." -ForegroundColor Cyan
git commit -m "Complete POS system update with dark theme and wholesale prices"

# 5. Push to GitHub
Write-Host "☁️ Pushing to GitHub..." -ForegroundColor Cyan
git push origin master --force

Write-Host "✅ Done! Wait 2-3 minutes and visit:" -ForegroundColor Green
Write-Host "https://srfashoinned.github.io/SR-Psd/" -ForegroundColor Yellow