# This scripts gets all VPC peering connections for all VPCs in all AWS accounts.
# It prints the VPC peering connection ID, requester VPC, accepter VPC, status and tags.
# It uses the AWS profiles defined in ~/.aws/credentials
# These profiles are aws sso profiles, but it can be used with any other profile.


import boto3

profiles = ["alef-qa", "alef-moe", "alef-us",
            "alef-gcc", "alef-ina", "alef-shared"]


for profile in profiles:

    # Session with aws profile.
    session = boto3.Session(profile_name=profile)
    # Create an EC2 client
    ec2 = session.client('ec2')

    # Get all VPCs
    response = ec2.describe_vpcs()

    # Loop over each VPC and get its VPC peering details
    print(profile)
    for vpc in response['Vpcs']:
        vpc_id = vpc['VpcId']

        # Get all VPC peering connections for this VPC
        peering_response = ec2.describe_vpc_peering_connections(
            Filters=[{'Name': 'accepter-vpc-info.vpc-id', 'Values': [vpc_id]}])

        # Loop over each VPC peering connection and print its details
        for peering in peering_response['VpcPeeringConnections']:
            print(
                f"VPC Peering Connection ID: {peering['VpcPeeringConnectionId']}")
            print(f"Requester VPC: {peering['RequesterVpcInfo']['VpcId']}")
            print(f"Accepter VPC: {peering['AccepterVpcInfo']['VpcId']}")
            print(f"Status: {peering['Status']['Code']}")
            tag_response = ec2.describe_tags(
                Filters=[{'Name': 'resource-id', 'Values': [peering['VpcPeeringConnectionId']]}])
            tags = {tag['Key']: tag['Value'] for tag in tag_response['Tags']}
            print(f"Tags: {tags}")
            print("------")
