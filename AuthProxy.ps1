$proxyAddress = "10.10.10.10:8080"
$username = "domain\test1"
$password = "password2"

$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($username, $securePassword)

$proxy = New-Object System.Net.WebProxy($proxyAddress, $true)
$proxy.Credentials = $credential

# Example usage - replace with your own code
$webClient = New-Object System.Net.WebClient
$webClient.Proxy = $proxy
$webClient.DownloadString("https://www.example.com")
