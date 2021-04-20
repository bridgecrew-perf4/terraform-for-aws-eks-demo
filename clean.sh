#!/bin/bash

echo "-----Deleting the deployed microservices using kubectl--------"
echo "-----First, delete Api-Server Service----"
kubectl delete -f eks-deploy/kubernetes/api-server-mainfest.yaml

echo "-----Second, delete backend Service------"
kubectl delete -f eks-deploy/kubernetes/backend-mainfest.yaml

echo "----Deletion completed!!!-------"