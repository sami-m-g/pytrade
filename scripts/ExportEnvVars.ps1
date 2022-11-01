Get-ChildItem (Get-Location) |
    Where-Object {-not $_.PsIsContainer -and $_.Name -eq ".env"} |
    Get-Content |
    ForEach-Object {
        $key, $value = $_.split('=', 2);
        Invoke-Expression "`$env:$key='$value'"
    }