#!/usr/bin/env python3

import aws_cdk as cdk

from lambda_nat_gateway_cdk.lambda_nat_gateway_cdk_stack import LambdaNatGatewayCdkStack


app = cdk.App()
LambdaNatGatewayCdkStack(app, "lambda-nat-gateway-cdk")

app.synth()
