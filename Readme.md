# Terraform for AWS EKS Cluster

## Requirements
The list of the resources to be created to run a AWS EKS Cluster inside a custom virtual private network include:

1. VPC
2. Internet Gateway associated with VPC
3. Subnets(private and public) inside VPC
4. Availability zone which is used to create our subnets(Optional)
5. Route Table inside VPC (CIDR Block) that directs internet-bound traffic to the internet gateway
6. Route table association(CIDR Block subest of VPC CIDR Block) with subnets(private and public)
7. Security groups inside VPC to attach with woker node groups
8. Tags attached to resources to track them. 
9. To define node groups(pools) ec2 instace type, number, ami,etc
10. ELB instance inside our public subnet 

## Network Configuration Diagram
![alt text](https://github.com/limbuu/terraform-for-aws-eks-demo/blob/main/images/network-diagram-eks.png)

## Prerequisties
* [Terraform CLI](https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/aws-get-started)
* [Kubectl CLI](https://kubernetes.io/docs/tasks/tools/) 
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
* [An AWS Account](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all)

## Installation(For Linux)
1. Install latest terraform CLI:

    First, dowload the pre-compiled [binary package](https://www.terraform.io/downloads.html) or any appropiate package from the source. Now, unzip and move it to `/usr/local/bin` path.
    ```
    $ unzip terraform.zip
    $ mv ~/Downloads/terraform /usr/local/bin/
    ```
    Verify the installation:
    ```
    $ terraform -help
    ```
2. Install kubectl CLI:

    First, download latest binary as follows:
    ```
    $ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    ```
    Now, to validate the binary, download the checksum file as:
    ```
    $ curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"

    ```
    Validate the kubectl binary against checksum file:
    ```
    $ echo "$(<kubectl.sha256) kubectl" | sha256sum --check
    ```

    Now, install the kubectl cli as follows:
    ```
    $ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    ```
    Verify the installation:
    ```
    $ echo "$(<kubectl.sha256) kubectl" | sha256sum --check
    ```

3. Install AWS CLI V2:

    To install latest version of AWS CLI, use commands as follows:
    ```
    $ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    $ unzip awscliv2.zip
    $ sudo ./aws/install
    ```
3. Create an AWS account:

    Now, create an aws account following [link](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all).We will use the secret credentials of this aws account to interact with AWS Services.

4. Use AWS credentials:

    There are two ways to use aws credentials. 

    First is, directly using with terraform files which exposes the credentials when files are shared or pushed to pubic repositories. 
    ```
        provider "aws" {
            access_key = "AKIAIOSFODNN7EXAMPLE"
            secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
            region = "us-west-2"
        }
    ```
    Therefore, to avoid such situation we will configure basic AWS CLI settings to interact with AWS.
    ```
    $ aws configure --profile terraform-user
    AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
    AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    Default region name [None]: us-west-2
    Default output format [None]: json

    ```
    The configuration process stores your credentials with a profile name in a file at ~/.aws/credentials. Now, use this profile with terraform files:
    ```
        provider "aws" {
            profile = "terraform-user"
            region = "us-west-2"
        }
    ```

## Terraform Steps
1. Clone the Repo

    First, clone the repo `terraform-for-aws-eks-demo` and go to terraform directory while contains `terraform configuration` files.
    ```
    $ git clone https://github.com/limbuu/terraform-for-aws-eks-demo.git
    $ cd terraform-for-aws-eks-demo
    $ cd eks-deploy/terraform
    ```
2. Check Configuration 

    The set of files with `.tf` extension is used to describe infrastructure in Terraform, which is called Terraform `configuration`. 
    ```
    $ tree
    .
    ├── eks-cluster.tf
    ├── kubernetes.tf
    ├── outputs.tf
    ├── security-groups.tf
    ├── versions.tf
    └── vpc.tf
    ```
Terraform Files:

    * vpc.tf contains vpc and subnet configration with provider(aws here) to be provisioned and associated to the eks-cluster.
    * security-groups.tf contains security groups configuration with ingress/egress rules to be associated with the cluster and workernodes.
    * eks-cluster contains the resource configuration of eks-cluster like name, vpc, subnets, workernodes, nodetype, security groups, etc.
    * kubernetes.tf contains kubernetes provider to be used for eks-cluster creation/management.
    * versions.tf contains different provisioners used by the Terraform their source and versions.
    * outputs.tf contains resource configuration values we want to display for visualtization.

Blocks in Terraform Files: 

    * terraform {} block contains Terraform settings, including provisioner settings.
    * provider {} block configures the specific provider/plugin (aws here) settings to provision/manage your resources.
    * resource {} blocks define different component of your infrastucture.
    * module {} block allows to group resources together that can be use many times later as template. 
    * tags {} block defined attach tags to that resource when provisioned.

3. Initialize Directory 
    
    Now, initialize the `terraform` directory with `terraform init` to download and install the provider which is `aws` here in hidden directory `.terraform`.
    ```
    $ terraform init
    ```
    Now, make sure the configuration is syntatically valid before creating the infrastructure:
    ```
    $ terraform validate
    Success! The configuration is valid.

4. Create Infrastructure

    Now, apply the configuration using command `terraform apply` to create the infrastructure from the configuration file.
    ```
    $ terraform apply 
    ```

5. Inspect State
    
    After applying configuration, Terraform stores the properties and values of the newly created infrastructure in a file `terraform.tfstate`, such that it can update or destroy those resources whenever needed. You can inspect the current state running command:

    ```
    $ terraform show
    ```

6. Cofigure kubectl

    Now that you've provisioned your EKS cluster, you need to configure kubectl. Run the following command to retrieve the access credentials for your cluster and automatically configure kubectl.
    ```
    $ aws eks --region $(terraform output -raw region) update-kubeconfig --name $(terraform output -raw cluster_name)
    ```


7. Destrory Infrastructure

    The `terraform destroy` command destroys the infrastruce resources created using Terraform configuration. 
    ```
    $ terraform destroy 
    ```

## Microservice Deployment 
1. Deploy Microservice Workloads
    In `microservice` directory there are two services: `api-server service` and `backend service` where api-server is internet facing and backned-service is not and is accesibe through api-server only. 

    Now, deploy the kubernetes deployments of the services using script as follows: 
    ```
    $ cd terraform-for-aws-eks-demo/
    $ chmod +x deploy.sh
    $ ./deploy.sh
    ```
2. Access EKS deployed workloads

    ```
    ## deployment
    $ kubectl get deploy 
    NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
    api-server-deployment   1/1     1            1           1m
    backend-deployment      1/1     1            1           1m

    ## pods
    $ kubectl get pods
    NAME                                     READY   STATUS    RESTARTS   AGE
    api-server-deployment-555497f94d-rx6nc   1/1     Running   0          1m
    backend-deployment-77c5dd79b7-tsscl      1/1     Running   0          1m

    ## services
    $ kubectl get svc
    NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP                                                               PORT(S)        AGE
    api-server-service   LoadBalancer   172.20.73.188   a9c0ec602bc8a40a39e0dff95e1d7136-1469137643.us-east-1.elb.amazonaws.com   80:32284/TCP   1m
    backend-service      ClusterIP      172.20.64.180   <none>                                                                    80/TCP         1m
    kubernetes           ClusterIP      172.20.0.1      <none>                                                                    443/TCP        3m
    ```
    Now, verify the externel-ip associated with `api-server-service` to make sure it is working:
    ```
    $ telnet a9c0ec602bc8a40a39e0dff95e1d7136-1469137643.us-east-1.elb.amazonaws.com 80
    Trying 52.3.138.153...
    Connected to a9c0ec602bc8a40a39e0dff95e1d7136-1469137643.us-east-1.elb.amazonaws.com.
    Escape character is '^]'.
    ```
    Finally, check apis of `apis-server`in paths:
    ```
    1. a9c0ec602bc8a40a39e0dff95e1d7136-1469137643.us-east-1.elb.amazonaws.com
    2. a9c0ec602bc8a40a39e0dff95e1d7136-1469137643.us-east-1.elb.amazonaws.com/health
    ```
    And, then of `backend-server` service in following paths:
    ```
    1. a9c0ec602bc8a40a39e0dff95e1d7136-1469137643.us-east-1.elb.amazonaws.com/backend
    2. a9c0ec602bc8a40a39e0dff95e1d7136-1469137643.us-east-1.elb.amazonaws.com/backend/health
    ```

3. Delete Deployments

    Now, destroy the kubernetes deployments of the services using script as follows: 
    ```
    $ chmod +x clean.sh
    $ ./clean.sh
    ```
