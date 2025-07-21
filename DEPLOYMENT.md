### GitHub Secrets Setup

Add the following secrets to your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `EC2_SSH_KEY`: Your private SSH key (Needed only for EC2 Deployment)
   - `EC2_DEV_IP`: EC2 instance Dev IP Address (Needed only for EC2 Deployment) 
   - `EC2_PROD_IP`: EC2 instance Prod IP Address (Needed only for EC2 Deployment)

## 🚀 AWS Deployment Options 

You can deploy this project to AWS using one of two main options. **Choose the option that best fits your use case and expertise:** 

<details>
<summary><strong>Option 1: EC2 Deployment (Traditional VM)</strong></summary>

**Best for:**   
- Full control over the environment   
- Running both FastAPI and MLflow servers   
- Easier debugging and monitoring for beginners 

### Steps:

#### 1. Launch an EC2 Instance

1. **Go to AWS Console** → EC2 → Launch Instance
2. **Choose AMI**: Select "Ubuntu Server 22.04 LTS (HVM), SSD Volume Type"
3. **Instance Type**: Choose t3.medium or larger (recommended for ML workloads)
4. **Key Pair**: Create a new key pair or select an existing one (download the .pem file)
5. **Network Settings**: 
   - Create a new Security Group or use existing one
   - **Configure Security Group Rules** (see step 1.1 below)
6. **Storage**: Default 8GB is usually sufficient, increase if needed
7. **Launch Instance**

#### 1.1. Security Group Configuration

⚠️ **Security Warning**: The following ports should **NOT** be open to `0.0.0.0/0` (everywhere) in production. Instead, restrict access to your specific IP address or VPC.

**Inbound Rules to Add:**
- **SSH (Port 22)**: Your IP address only (`<your-ip>/32`)
- **HTTP (Port 80)**: Your IP address only (`<your-ip>/32`) 
- **Custom TCP (Port 8000)**: Your IP address only (`<your-ip>/32`) - FastAPI
- **Custom TCP (Port 5000)**: Your IP address only (`<your-ip>/32`) - MLflow

**To find your IP address**: Visit [whatismyipaddress.com](https://whatismyipaddress.com) and use that IP with `/32` suffix.

**Example Security Group Rules:**
```
Type        Protocol    Port Range    Source          Description
SSH         TCP         22           203.0.113.0/32   SSH access from my IP
HTTP        TCP         80           203.0.113.0/32   HTTP access from my IP  
Custom TCP  TCP         8000         203.0.113.0/32   FastAPI from my IP
Custom TCP  TCP         5000         203.0.113.0/32   MLflow from my IP
```

#### 2. SSH into the Instance
```sh 
# Make sure your key file has correct permissions
chmod 400 your-key-file.pem

# Connect to your Ubuntu instance
ssh -i your-key-file.pem ubuntu@<your-ec2-public-ip> 
``` 

#### 3. Install Docker & Docker Compose
```sh 
# Update package index
sudo apt update

# Install D 

#### 4. Clone the Repository & Set Up
```sh 
git clone https://github.com/yourusername/Taxi-Duration-Prediction.git 
cd Taxi-Duration-Prediction 
``` 

#### 5. Run the Application
```sh 
docker-compose up --build -d 
``` 

#### 6. Access the Services
- FastAPI: `http://<your-ec2-public-ip>:8000/docs` 
- MLflow: `http://<your-ec2-public-ip>:5000` 

</details>

<details>
<summary><strong>Option 2: AWS Lambda + Function URL (Serverless)</strong></summary>

**Best for:**   
- Cost efficiency (pay-per-use)   
- Automatic scaling   
- Deploying only the inference API (FastAPI) 

### Steps:

#### 1. Build a Lambda-Compatible Docker Image
Use the provided `Dockerfile.lambda` to build your image. 

```sh 
docker build -f Dockerfile.lambda -t taxi-prediction-lambda . 
``` 

#### 2. Push the Image to Amazon ECR
Create an ECR repository if you don't have one.
Authenticate Docker to ECR and push the image. 

```sh 
aws ecr create-repository --repository-name taxi-prediction-lambda 
aws ecr get-login-password | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com 
docker tag taxi-prediction-lambda:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/taxi-prediction-lambda:latest 
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/taxi-prediction-lambda:latest 
``` 

#### 3. Create a Lambda Function (Container Image)
In the AWS Console, create a new Lambda function using the ECR image. 

#### 4. Set Up Function URL
Create a Function URL

#### 5. Test the Endpoint
You'll get a public URL from (e.g., `https://<function_url>.<region>.amazonaws.com/`). 
Test with `/predict` endpoints. 


This guide covers the deployment of the NYC Taxi Duration Prediction service to both development and production environments using AWS Lambda with container images and Function URL.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Function URL  │──▶│   Lambda        │───▶│   FastAPI App   │
│                 │    │   Container     │    │   (Mangum)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CloudWatch    │    │   CloudWatch    │    │   Model         │
│   Logs          │    │   Logs          │    │   Artifacts     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Environment Separation

- **Development Environment**: Single Lambda function, debug logging, 1024MB memory
- **Production Environment**: Single Lambda function, info logging, 2048MB memory

## 🚀 Prerequisites

### AWS Account Setup

1. **AWS CLI Configuration**
   ```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, and default region
   ```

2. **Required AWS Services**
   - Amazon ECR (Elastic Container Registry)
   - AWS Lambda
   - CloudWatch Logs
   - IAM (for roles and policies)

### IAM Roles and Permissions

The CI/CD pipeline automatically creates the necessary IAM roles, but you can also create them manually if needed.

#### Required IAM Role: `lambda-execution-role`

This role is used by both development and production Lambda functions.

**Trust Policy (allows Lambda to assume the role):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**Custom Policy (`lambda-custom-policy`):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "lambda:InvokeFunction"
      ],
      "Resource": "*"
    }
  ]
}
```

#### Manual IAM Role Creation

If you need to create the IAM role manually, run these commands:

```bash
# Get your AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create the role
aws iam create-role \
  --role-name lambda-execution-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }'

# Create custom policy
aws iam put-role-policy \
  --role-name lambda-execution-role \
  --policy-name lambda-custom-policy \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ],
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "lambda:InvokeFunction"
        ],
        "Resource": "*"
      }
    ]
  }'
```

#### GitHub Actions IAM Permissions

The GitHub Actions workflow needs the following AWS permissions:

**IAM Permissions:**
- `iam:CreateRole`
- `iam:PutRolePolicy`
- `iam:GetRole`

**Lambda Permissions:**
- `lambda:CreateFunction`
- `lambda:UpdateFunctionCode`
- `lambda:GetFunction`
- `lambda:AddPermission`
- `lambda:WaitFunctionUpdated`

**ECR Permissions:**
- `ecr:CreateRepository`
- `ecr:DescribeRepositories`
- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:GetDownloadUrlForLayer`
- `ecr:BatchGetImage`
- `ecr:InitiateLayerUpload`
- `ecr:UploadLayerPart`
- `ecr:CompleteLayerUpload`
- `ecr:PutImage`


## 📋 Deployment Steps

### 1. Initial Setup

1. **Fork/Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/Taxi-Duration-Prediction.git
   cd Taxi-Duration-Prediction
   ```

2. **Update Configuration**
   - Update the AWS region in `.github/workflows/ci-cd.yml` if needed
   - Update your AWS account ID in the Lambda function ARNs (replace `ACCOUNT_ID` with your actual account ID)

3. **Install Dependencies**
   ```bash
   uv sync
   ```

### 2. Development Environment Deployment

1. **Create Development Branch**
   ```bash
   git checkout -b dev
   git push origin dev
   ```

2. **Trigger Development Deployment**
   - The CI/CD pipeline will automatically deploy to development when you push to the `dev` branch
   - Or manually trigger via GitHub Actions with environment set to "dev"

3. **Verify Deployment**
   ```bash
   # Check Lambda function
   aws lambda get-function --function-name taxi-prediction-dev
   
   ```

### 3. Production Environment Deployment

1. **Merge to Main Branch**
   ```bash
   git checkout main
   git merge dev
   git push origin main
   ```

2. **Production Deployment**
   - The CI/CD pipeline will automatically deploy to production when you push to the `main` branch
   - Or manually trigger via GitHub Actions with environment set to "prod"


## 🔧 Manual Deployment Commands

### ECR Repository Management

```bash
# Create ECR repository
aws ecr create-repository --repository-name taxi-duration-prediction-lambda

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push Lambda container
docker build -f Dockerfile.lambda -t taxi-duration-prediction-lambda .
docker tag taxi-duration-prediction-lambda:latest $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/taxi-duration-prediction-lambda:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/taxi-duration-prediction-lambda:latest
```

### Lambda Function Management

```bash
# Create Lambda function
aws lambda create-function \
  --function-name taxi-prediction-dev \
  --package-type Image \
  --code ImageUri=$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/taxi-duration-prediction-lambda:latest \
  --role arn:aws:iam::$AWS_ACCOUNT_ID:role/lambda-execution-role \
  --timeout 30 \
  --memory-size 1024 \
  --environment Variables="{APP_ENV=development,LOG_LEVEL=DEBUG}"

# Update Lambda function
aws lambda update-function-code \
  --function-name taxi-prediction-dev \
  --image-uri $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/taxi-duration-prediction-lambda:latest
```

## 🔄 Scaling and Updates

### Lambda Configuration Updates

```bash
# Update memory allocation
aws lambda update-function-configuration \
  --function-name taxi-prediction-dev \
  --memory-size 2048

# Update timeout
aws lambda update-function-configuration \
  --function-name taxi-prediction-dev \
  --timeout 60

# Update environment variables
aws lambda update-function-configuration \
  --function-name taxi-prediction-dev \
  --environment Variables="{APP_ENV=development,LOG_LEVEL=DEBUG,NEW_VAR=value}"
```

### Auto Scaling (Built-in)

Lambda automatically scales based on demand:
- No manual scaling required
- Handles concurrent requests automatically
- Scales to zero when not in use

## 🛠️ Troubleshooting

### Common Issues

1. **Lambda Function Errors**
   ```bash
   # Check function logs
   aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/taxi-prediction"
   
   # Test function directly
   aws lambda invoke --function-name taxi-prediction-dev --payload '{"httpMethod":"GET","path":"/health"}' response.json
   ```

2. **Container Build Issues**
   ```bash
   # Test container locally
   docker build -f Dockerfile.lambda -t test-lambda .
   docker run -p 9000:8080 test-lambda
   
   # Test with curl
   curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"httpMethod":"GET","path":"/health"}'
   ```

3. **Cold Start Issues**
   - Increase memory allocation (faster CPU)
   - Use provisioned concurrency for production
   - Optimize container size

### Performance Issues

1. **High Latency**
   - Check Lambda memory allocation
   - Monitor cold start times
   - Consider provisioned concurrency

2. **High Error Rate**
   - Check CloudWatch logs
   - Monitor function metrics
   - Verify Function URL integration

## 🔒 Security Best Practices

1. **IAM Security**
   - Follow principle of least privilege
   - Use IAM roles instead of access keys
   - Regularly rotate credentials

2. **Container Security**
   - Scan images for vulnerabilities
   - Use minimal base images
   - Keep dependencies updated

3. **API Security**
   - Implement rate limiting
   - Use HTTPS for all communications
   - Add authentication/authorization

4. **Network Security**
   - Use VPC for Lambda if needed
   - Restrict outbound traffic
   - Use security groups

## 🔧 Local Development

### Running Locally with Docker

```bash
# Build the container
docker build -f Dockerfile.lambda -t taxi-prediction-local .

# Run locally
docker run -p 9000:8080 taxi-prediction-local

# Test locally
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"httpMethod":"GET","path":"/health"}'
```

</details>

---

### 📝 Notes 

- **Choose only one deployment option** based on your needs.   
  - EC2 is more flexible and suitable for running the full stack (including MLflow). 
  - Lambda + Function URL is more scalable and cost-effective for serving the inference API only. 
- For production, consider using managed services for logging, monitoring, and secrets management. 
- For advanced use cases, you can also explore ECS/Fargate or Kubernetes (see To-Do list). 

---