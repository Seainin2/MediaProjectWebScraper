Write host "Deleting layer as it was not created in the cloud fromation"
aws lambda delete-layer-version --layer-name $Layer.LayerArn --version-number $LayerArn.LayerVersions.Version[0]

$topics = ( aws sns list-topics | ConvertFrom-Json ).Topics
Foreach ($topic in $topics){
	aws sns delete-topic --topic-arn $topic.TopicArn
}
Write-host "Deleting dbstack"
aws cloudformation delete-stack --stack-name dbstack
aws cloudformation wait stack-delete-complete --stack-name dbstack
write-host "Deleted, GOODBYE"