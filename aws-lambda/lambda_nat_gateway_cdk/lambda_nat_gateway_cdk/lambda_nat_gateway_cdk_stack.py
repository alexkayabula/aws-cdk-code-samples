from aws_cdk import (
    aws_ec2 as ec2,
    aws_lambda as _lambda,
    core
)

class MyVPCStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create VPC
        vpc = ec2.Vpc(
            self, "MyVPC",
            cidr="10.0.0.0/16",
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public"
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE,
                    name="Private"
                )
            ]
        )
        
        # Create Internet Gateway
        internet_gateway = ec2.InternetGateway(
            self, "InternetGateway",
            vpc=vpc
        )
        
        # Attach Internet Gateway to VPC
        vpc.connections.allow_to_internet(
            gateway=internet_gateway
        )
        
        # Get the public subnet
        public_subnet = vpc.public_subnets[0]
        
        # Create NAT Gateway
        nat_gateway = ec2.NatGateway(
            self, "NatGateway",
            vpc=vpc,
            subnet=public_subnet
        )
        
        # Get the private subnet
        private_subnet = vpc.private_subnets[0]
        
        # Create route table for private subnet
        private_route_table = ec2.RouteTable(
            self, "PrivateRouteTable",
            vpc=vpc,
            subnets=[private_subnet]
        )
        
        # Add route to NAT Gateway
        private_route_table.add_route(
            "PrivateRoute",
            destination_cidr_block="0.0.0.0/0",
            nat_gateway=nat_gateway
        )
        
        # Launch your function in the private subnet
        func = _lambda.Function(
            self, "MyFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda_code"),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE
            )
        )
        
        # Get the security group associated with the function
        security_group = func.connections.security_group

        # Allow outbound traffic
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(0),
            "Allow all outbound traffic"
        )
