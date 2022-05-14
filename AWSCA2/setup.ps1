#!usr/bin/env


#aws lambda list-functions
#aws create layer
#aws add layer lambda
#aws lambda update-function-code --function-name lambdaSNSFromRDS --zip-file fileb://function.zip

#py -3 awsdb.py
#aws rds wait db-instance-available
#$db = (aws rds describe-db-instances | ConvertFrom-Json)

#$db.DBInstances[0].DBInstanceIdentifier

#$Topics = (aws sns list-topics | ConvertFrom-Json).Topics

#foreach ($topic in $Topics)
#{
#	Write-Host $topic.TopicArn
#}

