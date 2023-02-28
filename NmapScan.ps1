$target = Read-Host "Enter the target hostname or IP address"
$startPort = Read-Host "Enter the starting port number to scan"
$endPort = Read-Host "Enter the ending port number to scan"

# Convert start and end port to integers
$startPort = [int]$startPort
$endPort = [int]$endPort

Write-Host "Scanning ports $startPort to $endPort on $target..."

for ($port = $startPort; $port -le $endPort; $port++) {
    $socket = New-Object System.Net.Sockets.TcpClient
    $connection = $socket.BeginConnect($target, $port, $null, $null)
    Start-Sleep -Milliseconds 1000
    if ($connection.AsyncWaitHandle.WaitOne(1000,$false)) {
        Write-Host "Port $port is open"
    }
    else {
        Write-Host "Port $port is closed"
    }
    $socket.Close()
}
