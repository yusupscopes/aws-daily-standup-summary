#!/bin/bash

# Exit on error
set -e

# Default values
ENVIRONMENT="dev"
STACK_NAME="daily-standup-summary"
REGION="ap-southeast-1"  # Singapore region (close to WIB timezone)
PROFILE="ym3594216"      # Default AWS profile
EMAIL="yusupmaulana950@gmail.com"                 # Required email for SNS subscription

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --env)
      ENVIRONMENT="$2"
      shift 2
      ;;
    --region)
      REGION="$2"
      shift 2
      ;;
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --email)
      EMAIL="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(dev|staging|prod)$ ]]; then
  echo "Error: Environment must be 'dev', 'staging', or 'prod'"
  exit 1
fi

# Validate email
if [ -z "$EMAIL" ]; then
  echo "Error: Email address is required. Use --email parameter."
  echo "Usage: $0 --env <dev|staging|prod> --email <email> [--region <region>] [--profile <profile>]"
  exit 1
fi

# Set stack name with environment
STACK_NAME="${STACK_NAME}-${ENVIRONMENT}"

echo "Deploying to environment: $ENVIRONMENT"
echo "Stack name: $STACK_NAME"
echo "Region: $REGION"
echo "AWS Profile: $PROFILE"
echo "Notification Email: $EMAIL"

# Create S3 bucket for artifacts if it doesn't exist
BUCKET_NAME="${STACK_NAME}-artifacts"
echo "Ensuring S3 bucket exists: $BUCKET_NAME"
if ! aws s3api head-bucket --bucket "$BUCKET_NAME" --profile "$PROFILE" --region "$REGION" 2>/dev/null; then
  echo "Creating S3 bucket: $BUCKET_NAME"
  aws s3api create-bucket \
    --bucket "$BUCKET_NAME" \
    --region "$REGION" \
    --profile "$PROFILE" \
    --create-bucket-configuration LocationConstraint="$REGION"
fi

# Prepare Python dependencies
echo "Installing Python dependencies..."
rm -rf package
mkdir -p package
pip install -r requirements.txt --target ./package
cp -r app/* package/

# Package the CloudFormation template
echo "Packaging CloudFormation template..."
sam package \
  --template-file infra/template.yaml \
  --s3-bucket "$BUCKET_NAME" \
  --output-template-file packaged.yaml \
  --profile "$PROFILE" \
  --region "$REGION"

# Deploy the stack
echo "Deploying CloudFormation stack..."
sam deploy \
  --template-file packaged.yaml \
  --stack-name "$STACK_NAME" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    Environment="$ENVIRONMENT" \
    EmailAddress="$EMAIL" \
  --profile "$PROFILE" \
  --region "$REGION"

# Clean up
rm -rf package packaged.yaml

echo "Deployment completed successfully!"

# Get stack outputs
echo "Stack outputs:"
aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query 'Stacks[0].Outputs' \
  --output table \
  --profile "$PROFILE" \
  --region "$REGION"

echo "Note: Please check your email ($EMAIL) to confirm the SNS subscription." 