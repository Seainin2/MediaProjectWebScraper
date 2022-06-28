#!usr/bin/env
Write-host "Waiting for cloudformation to be created. will take a few minutes"
$StackId = (aws cloudformation create-stack --stack-name dbstack --template-body file://template.json --capabilities CAPABILITY_NAMED_IAM  | ConvertFrom-Json).StackId
write-host "Cloud Initiated please wait while rds is created, may take up to 20 minutes"
aws cloudformation wait stack-create-complete --stack-name dbstack
aws rds wait db-instance-available --db-instance-identifier sqldatabase

Write-host "Creating pyodbc driver layer"
$Layer = (aws lambda publish-layer-version --layer-name pyodbclayer --zip-file fileb://pyodbc-layer.zip --compatible-runtimes python3.7 | ConvertFrom-Json)

Write-host "Adding .Zip to lambda function"
aws lambda update-function-code --function-name lambdaSNSFromRDS --zip-file fileb://function.zip

Write-host "Getting latest pyodbc layer"
$LayerArn = (aws lambda list-layer-versions --layer-name pyodbclayer | ConvertFrom-Json)

Write-host "Adding layer to lambda"
aws lambda update-function-configuration --function-name lambdaSNSFromRDS --layers $LayerArn.LayerVersions.LayerVersionArn[0]


#-get route table id
$RouteTableId = (aws ec2 describe-route-tables | ConvertFrom-Json).RouteTables.RouteTableId
#-get internet gateway id
$InternetGatewayId = (aws ec2 describe-internet-gateways | ConvertFrom-Json).InternetGateways.InternetGatewayId
Write-host "Adding Internet Gateway to RouteTable"
#-add route to route table//allow all connections to database instance
aws ec2 create-route --route-table-id $RouteTableId --destination-cidr-block 0.0.0.0/0 --gateway-id $InternetGatewayId

#py -3 pythonsetup.py
#$db = (aws rds describe-db-instances | ConvertFrom-Json)

#aws lambda invoke --function--name LambdaSNSFromRDS --payload {"dbArn":"$db"}
#aws rds wait db-instance-available
#$db = (aws rds describe-db-instances | ConvertFrom-Json)

#$db.DBInstances[0].DBInstanceIdentifier

#$Topics = (aws sns list-topics | ConvertFrom-Json).Topics

#foreach ($topic in $Topics)
#{
#	Write-Host $topic.TopicArn
#}
#aws lambda delete-layer-version --layer-name $Layer.LayerArn --version-number $LayerArn.LayerVersions.Version[0]
#aws cloudformation delete-stack --stack-name dbstack
