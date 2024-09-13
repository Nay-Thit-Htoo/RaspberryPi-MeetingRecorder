import json

# Define appsettings.json file path
file_path = 'clientinfo.json'

# Read Client Information
def read_clientInfo():
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

# Update Client Information
def update_clientInfo(new_object):
    org_setting_data=read_clientInfo() 
    org_setting_data["upload_file_path"]=new_object["upload_file_path"]    
    org_setting_data["usercode"]=new_object["usercode"]
    org_setting_data["usertype"]=new_object["usertype"]   
    write_all_clientInfo(org_setting_data)
    return org_setting_data

# Update Client Information
def update_serverInfo(new_object):
    print(f"Update Sever Information : {new_object}")
    org_setting_data=read_clientInfo() 
    org_setting_data["server_ip"]=new_object["server_ip"]
    org_setting_data["server_port"]=new_object["server_port"]   
    write_all_clientInfo(org_setting_data)
    return org_setting_data

# Write All Client Information
def write_all_clientInfo(app_setting_data):
    with open(file_path, 'w') as file:
        json.dump(app_setting_data, file, indent=4)   

