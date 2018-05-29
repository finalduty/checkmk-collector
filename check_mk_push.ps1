# Powershell script to collect the output of the Check_MK agent and push it into the Collector API
# Add a Task Scheduler entry to run this every minute or less

$hostname = "ExampleName"
$collector_uri = "http://1.1.1.1:8080/collector/api/v0.1/hosts/"

# Capture output of Check_MK agent
$psi = New-object System.Diagnostics.ProcessStartInfo
$psi.CreateNoWindow = $true
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.FileName = "C:\Program Files (x86)\check_mk\check_mk_agent.exe"
$psi.Arguments = @("test")
$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi
[void]$process.Start()
$output = $process.StandardOutput.ReadToEnd()
$process.WaitForExit()

# Convert to Base64
$Bytes = [System.Text.Encoding]::UTF8.GetBytes($output)
$EncodedText =[Convert]::ToBase64String($Bytes)

# PUT JSON encoded result
$JSON = @{
  "hostname" = ${hostname}
  "status_data" = ${EncodedText}
}
Invoke-RestMethod -Uri "${collector_uri}${hostname}" -Method Put -Body $(ConvertTo-Json ${JSON}) -ContentType 'application/json'
