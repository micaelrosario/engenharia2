param(
    [Parameter(ValueFromRemainingArguments=$true)]
    $ExtraArgs
)

# Se você usa um virtualenv, ative-o antes de rodar (opcional):
# .\.venv\Scripts\Activate.ps1

# Executa pytest passando argumentos extras recebidos
python -m pytest @ExtraArgs
