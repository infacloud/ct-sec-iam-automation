import os
import json
import shutil
parent_dir = os.getcwd()
def run_terraform(req,bp):
    
    role_path = os.path.join("terraform",bp['role_name'])
    if(not os.path.exists(role_path)):
        #create folder, create main.tf and tfvars file
        os.mkdir(role_path)
        shutil.copy("main.tf", role_path)
        # shutil.copy("terraform.tfvars", role_path)
    os.chdir(role_path)

    with open("terraform.tfvars",'w') as varfile:
        varfile.write(f'region="{req["region"]}"\n')
        varfile.write(f'provider_url="{req["provider_url"]}"\n')
        varfile.write(f'ns_sa={json.dumps(bp["ns_sa"])}\n')
        varfile.write(f'role_name="{bp["role_name"]}"\n')
        varfile.write(f'policies={json.dumps(bp["policies"])}')

    os.system("terraform init")
    os.system(f"terraform import aws_iam_openid_connect_provider.oidc_provider arn:aws:iam::{req['account']}:oidc-provider/{req['provider_url'][8:]}")
    os.system(f"terraform import aws_iam_role.role {bp['role_name']}")
    # os.system(f"terraform plan")
    os.system(f"terraform apply -auto-approve")
    os.system(f"terraform output > out.txt")
    os.chdir(parent_dir)
    if(os.path.exists(os.path.join(role_path,'out.txt'))):
        with open(os.path.join(role_path,'out.txt'),'r') as outfile:
            resp = [line.rstrip() for line in outfile]
            return str(resp)
    else:
        return "Error. Please retry"
    # return "done"

if __name__ == "__main__":
    req = {
        "account":530774763960,
        "role_name":"test_oidc2",
        "proivder_url":"https://oidc.eks.us-west-2.amazonaws.com/id/ADCA690CEA55CB775B15DE0CDBCBC0E3",
        "region":"us-west-2",
        "ns_sa":["system:serviceaccount:abc:def","system:serviceaccount:abc:ggg"]
    }
    run_terraform(req)

# terraform import aws_iam_openid_connect_provider.oidc_provider arn:aws:iam::530774763960:oidc-provider/oidc.eks.us-west-2.amazonaws.com/id/ADCA690CEA55CB775B15DE0CDBCBC0E3
# terraform import aws_iam_role.role test_oidc
