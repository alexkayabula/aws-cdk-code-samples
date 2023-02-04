import aws_cdk as core
import aws_cdk.assertions as assertions
from lambda_nat_gateway_cdk.lambda_nat_gateway_cdk_stack import LambdaNatGatewayCdkStack


def test_sqs_queue_created():
    app = core.App()
    stack = LambdaNatGatewayCdkStack(app, "lambda-nat-gateway-cdk")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = LambdaNatGatewayCdkStack(app, "lambda-nat-gateway-cdk")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
