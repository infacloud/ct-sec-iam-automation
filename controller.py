import os
def run_terraform(region,role_name,proivder_url):    
    os.system("terraform init")
    os.system("terraform plan -var region={region} -var role_name={role_name} -var provider_url={proivder_url}")
    os.system(f"terraform apply -auto-approve -var region={region} -var role_name={role_name} -var provider_url={proivder_url}")
    return

if __name__ == "__main__":
    run_terraform("us-west-2","test_oidc2","https://oidc.eks.us-west-2.amazonaws.com/id/ADCA690CEA55CB775B15DE0CDBCBC0E3")