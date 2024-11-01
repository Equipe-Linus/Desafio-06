$exclude = @("venv", "bot_sefaz_formulario.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "bot_sefaz_formulario.zip" -Force