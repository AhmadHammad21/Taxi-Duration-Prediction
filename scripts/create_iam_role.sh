#!/bin/bash

# Script to create IAM role for Lambda execution
# Run this script if you encounter IAM role issues during deployment

set -e

echo "🔧 Creating IAM role for Lambda execution..."

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "📋 AWS Account ID: $ACCOUNT_ID"

# Check if role already exists
if aws iam get-role --role-name lambda-execution-role 2>/dev/null; then
    echo "✅ lambda-execution-role already exists"
else
    echo "🔄 Creating lambda-execution-role..."
    
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
    
    echo "✅ Created lambda-execution-role"
fi

# Create custom policy
echo "🔄 Creating custom policy for Lambda permissions..."

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

echo "✅ Created lambda-custom-policy"

# Verify the role
echo "🔍 Verifying role configuration..."
aws iam get-role --role-name lambda-execution-role --query 'Role.{RoleName:RoleName,Arn:Arn,AssumeRolePolicyDocument:AssumeRolePolicyDocument}' --output table

echo "✅ IAM role setup complete!"
echo "📋 Role ARN: arn:aws:iam::$ACCOUNT_ID:role/lambda-execution-role"
echo "🚀 You can now run the CI/CD pipeline" 