$email = Read-host "Please enter the email you wish to subscribe with"
$email

$endpoint = (aws rds describe-db-instances | ConvertFrom-Json).DBInstances[0].Endpoint.Address
$endpoint

Write-host "You will now be subscribed to games in the rds database, you will recive a message fromeach topic. this could take upto 3 minutes"

$temp = '{\"server\":\"'+$endpoint+'\",\"email\":\"'+$email+'\"}'
#$temp = '{"server":"${endpoint}","email":"${email}"}'

#$ExecutionContext.InvokeCommand.ExpandString($temp)

aws lambda invoke --function-name lambdaSNSFromRDS --cli-binary-format raw-in-base64-out --payload $temp response.json 
Write-Host "Demo Complete"