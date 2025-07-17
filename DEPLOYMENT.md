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
<summary><strong>Option 2: AWS Lambda + API Gateway (Serverless)</strong></summary>

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

#### 4. Set Up API Gateway
Create a new HTTP API Gateway.
Integrate it with your Lambda function. 

#### 5. Test the Endpoint
You'll get a public URL from API Gateway (e.g., `https://xxxxxx.execute-api.<region>.amazonaws.com/`). 
Test with `/docs` or `/predict` endpoints. 

</details>

---

### 📝 Notes 

- **Choose only one deployment option** based on your needs.   
  - EC2 is more flexible and suitable for running the full stack (including MLflow). 
  - Lambda + API Gateway is more scalable and cost-effective for serving the inference API only. 
- For production, consider using managed services for logging, monitoring, and secrets management. 
- For advanced use cases, you can also explore ECS/Fargate or Kubernetes (see To-Do list). 

---

# Deployment Guide - NYC Taxi Duration Prediction (Lambda + API Gateway)

This guide covers the deployment of the NYC Taxi Duration Prediction service to both development and production environments using AWS Lambda with container images and API Gateway.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │───▶│   Lambda        │───▶│   FastAPI App   │
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
   - API Gateway
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

**API Gateway Permissions:**
- `apigateway:CreateRestApi`
- `apigateway:GetRestApis`
- `apigateway:GetResources`
- `apigateway:CreateResource`
- `apigateway:PutMethod`
- `apigateway:PutIntegration`
- `apigateway:CreateDeployment`

### GitHub Secrets Setup

Add the following secrets to your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

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
   
   # Check API Gateway
   aws apigateway get-rest-apis --query 'items[?name==`Taxi Prediction API - Dev`]'
   ```

4. **Test Development Environment**
   ```bash
   # Get API Gateway URL
   API_ID=$(aws apigateway get-rest-apis --query 'items[?name==`Taxi Prediction API - Dev`].id' --output text)
   API_URL="https://$API_ID.execute-api.us-east-1.amazonaws.com/dev"
   
   # Health check
   curl $API_URL/health
   
   # Prediction test
   curl -X POST $API_URL/predict \
     -H "Content-Type: application/json" \
     -d '{"PULocationID": 1, "DOLocationID": 2, "trip_distance": 5.0}'
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

3. **Verify Production Deployment**
   ```bash
   # Check Lambda function
   aws lambda get-function --function-name taxi-prediction-prod
   
   # Check API Gateway
   aws apigateway get-rest-apis --query 'items[?name==`Taxi Prediction API - Prod`]'
   ```

4. **Test Production Environment**
   ```bash
   # Get API Gateway URL
   API_ID=$(aws apigateway get-rest-apis --query 'items[?name==`Taxi Prediction API - Prod`].id' --output text)
   API_URL="https://$API_ID.execute-api.us-east-1.amazonaws.com/prod"
   
   # Health check
   curl $API_URL/health
   
   # Prediction test
   curl -X POST $API_URL/predict \
     -H "Content-Type: application/json" \
     -d '{"PULocationID": 1, "DOLocationID": 2, "trip_distance": 5.0}'
   ```

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

### API Gateway Management

```bash
# Create API Gateway REST API
API_ID=$(aws apigateway create-rest-api --name "Taxi Prediction API - Dev" --description "Development API for taxi duration prediction" --query 'id' --output text)

# Get root resource ID
ROOT_ID=$(aws apigateway get-resources --rest-api-id $API_ID --query 'items[?path==`/`].id' --output text)

# Create /predict resource
PREDICT_RESOURCE_ID=$(aws apigateway create-resource --rest-api-id $API_ID --parent-id $ROOT_ID --path-part "predict" --query 'id' --output text)

# Create /health resource
HEALTH_RESOURCE_ID=$(aws apigateway create-resource --rest-api-id $API_ID --parent-id $ROOT_ID --path-part "health" --query 'id' --output text)

# Create POST method for /predict
aws apigateway put-method \
  --rest-api-id $API_ID \
  --resource-id $PREDICT_RESOURCE_ID \
  --http-method POST \
  --authorization-type NONE

# Create GET method for /health
aws apigateway put-method \
  --rest-api-id $API_ID \
  --resource-id $HEALTH_RESOURCE_ID \
  --http-method GET \
  --authorization-type NONE

# Create Lambda integration for /predict
aws apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $PREDICT_RESOURCE_ID \
  --http-method POST \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:$AWS_ACCOUNT_ID:function:taxi-prediction-dev/invocations

# Create Lambda integration for /health
aws apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $HEALTH_RESOURCE_ID \
  --http-method GET \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:$AWS_ACCOUNT_ID:function:taxi-prediction-dev/invocations

# Add Lambda permission for API Gateway
aws lambda add-permission \
  --function-name taxi-prediction-dev \
  --statement-id apigateway-dev \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:us-east-1:$AWS_ACCOUNT_ID:$API_ID/*/*/*"

# Deploy API
aws apigateway create-deployment --rest-api-id $API_ID --stage-name dev
```

## 📊 Monitoring and Logging

### CloudWatch Logs

```bash
# View Lambda function logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/taxi-prediction"

# Get log streams
aws logs describe-log-streams --log-group-name "/aws/lambda/taxi-prediction-dev" --order-by LastEventTime --descending

# Get log events
aws logs get-log-events --log-group-name "/aws/lambda/taxi-prediction-dev" --log-stream-name "log-stream-name"
```

### Lambda Function Monitoring

```bash
# Check function configuration
aws lambda get-function --function-name taxi-prediction-dev

# Check function metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=taxi-prediction-dev \
  --start-time $(date -d '1 hour ago' --iso-8601=seconds) \
  --end-time $(date --iso-8601=seconds) \
  --period 300 \
  --statistics Average
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

3. **API Gateway Issues**
   ```bash
   # Check API Gateway deployment
   aws apigateway get-deployments --rest-api-id $API_ID
   
   # Check integration
   aws apigateway get-integration --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method POST
   ```

4. **Cold Start Issues**
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
   - Verify API Gateway integration

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

## 💰 Cost Optimization

1. **Lambda Optimization**
   - Right-size memory allocation
   - Optimize container size
   - Use provisioned concurrency for predictable workloads

2. **API Gateway Optimization**
   - Use caching where appropriate
   - Monitor request counts
   - Consider API Gateway usage plans

3. **Monitoring Costs**
   - Set up CloudWatch billing alerts
   - Monitor Lambda execution times
   - Clean up unused resources

## 📈 Next Steps

1. **Advanced Monitoring**
   - Set up CloudWatch dashboards
   - Implement custom metrics
   - Add alerting

2. **CI/CD Enhancements**
   - Add blue-green deployments
   - Implement canary deployments
   - Add automated rollback

3. **Security Enhancements**
   - Add WAF protection
   - Implement API key management
   - Add request/response validation

4. **Performance Optimization**
   - Add caching layer (Redis/ElastiCache)
   - Implement CDN for static content
   - Add database connection pooling

5. **Advanced Features**
   - Add custom domain names
   - Implement API versioning
   - Add request/response transformation

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

### Running with SAM CLI

```bash
# Install SAM CLI
pip install aws-sam-cli

# Create sam template
cat > template.yaml << EOF
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  TaxiPredictionFunction:
    Type: AWS::Serverless::Function
    Properties:
      PackageType: Image
      MemorySize: 1024
      Timeout: 30
      Environment:
        Variables:
          APP_ENV: development
          LOG_LEVEL: DEBUG
    Metadata:
      Dockerfile: Dockerfile.lambda
      DockerContext: .
EOF

# Build and run locally
sam build
sam local start-api
```

---

For additional support or questions, please refer to the project documentation or create an issue in the repository. 

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **GitHub Repository** with the code
3. **AWS Credentials** configured as GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

## Required AWS Permissions

The GitHub Actions workflow needs the following AWS permissions:

### IAM Permissions
- `iam:CreateRole`
- `iam:PutRolePolicy`
- `iam:GetRole`
- `iam:AttachRolePolicy`

### Lambda Permissions
- `lambda:CreateFunction`
- `lambda:UpdateFunctionCode`
- `lambda:GetFunction`
- `lambda:AddPermission`
- `lambda:WaitFunctionUpdated`

### ECR Permissions
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

### API Gateway Permissions
- `apigateway:CreateRestApi`
- `apigateway:GetRestApis`
- `apigateway:GetResources`
- `apigateway:CreateResource`
- `apigateway:PutMethod`
- `apigateway:PutIntegration`
- `apigateway:CreateDeployment`

### CloudWatch Logs Permissions
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`

## IAM Roles Created Automatically

The CI/CD pipeline automatically creates the following IAM role:

### `lambda-execution-role`
This role is used by both dev and prod Lambda functions and includes:

**Trust Policy:**
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

## Manual IAM Role Creation (if needed)

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

## Deployment Process

### Automatic Deployment

1. **Push to dev branch** → Deploys to development environment
2. **Push to main branch** → Deploys to production environment
3. **Manual trigger** → Choose environment and action

### Manual Deployment

1. Go to GitHub Actions tab
2. Select "Deploy Taxi Prediction API" workflow
3. Click "Run workflow"
4. Choose:
   - **Environment**: `dev` or `prod`
   - **Action**: `deploy`, `test-only`, or `train-only`
   - **Force Deploy**: `true` to skip quality checks

## Architecture

```
Client Request → API Gateway → Lambda Function → Response
                     ↓
              Container Image (ECR)
                     ↓
              FastAPI + ML Model
```

### Components

1. **ECR Repositories**:
   - `taxi-duration-prediction-dev` (development)
   - `taxi-duration-prediction-prod` (production)

2. **Lambda Functions**:
   - `taxi-prediction-dev` (development)
   - `taxi-prediction-prod` (production)

3. **API Gateway**:
   - Separate APIs for dev and prod
   - Endpoints: `/health`, `/predict`

## Testing

### Health Check
```bash
curl https://your-api-id.execute-api.region.amazonaws.com/dev/health
```

### Prediction
```bash
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/dev/predict \
  -H "Content-Type: application/json" \
  -d '{"PULocationID": 1, "DOLocationID": 2, "trip_distance": 5.0}'
```

## Troubleshooting

### Common Issues

1. **IAM Role Error**: Ensure the `lambda-execution-role` exists and has proper permissions
2. **ECR Access Error**: Check that Lambda has ECR read permissions
3. **API Gateway Error**: Verify Lambda permissions for API Gateway invocation
4. **Cold Start**: First request may be slow due to container initialization

### Logs

- **Lambda Logs**: CloudWatch Logs `/aws/lambda/taxi-prediction-dev` or `/aws/lambda/taxi-prediction-prod`
- **API Gateway Logs**: CloudWatch Logs for API Gateway execution

## Cost Optimization

- **Lambda**: Pay per request (100ms increments)
- **API Gateway**: Pay per request
- **ECR**: Pay for storage and data transfer
- **CloudWatch**: Pay for logs storage and ingestion

## Security

- **No authentication** configured by default
- **CORS** enabled for all origins
- **Environment variables** for configuration
- **IAM roles** with minimal required permissions 