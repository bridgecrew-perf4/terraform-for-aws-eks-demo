#!/bin/bash

echo "-----Start deploying the microservices using kubectl--------"
echo "-----First, deploy Api-Server Service----"
kubectl apply -f eks-deploy/kubernetes/api-server-mainfest.yaml

echo "-----Second, deploy backend Service------"
kubectl apply -f eks-deploy/kubernetes/backend-mainfest.yaml

echo "----Deployment completed!!!-------"