#!/bin/bash

# Retrieve the secret from Parameter Store
export DJANGO_SECRET_KEY=$(aws ssm get-parameter --name "/myapp/DJANGO_SECRET_KEY" --with-decryption --query Parameter.Value --output text)

# Execute the main container command
exec "$@"