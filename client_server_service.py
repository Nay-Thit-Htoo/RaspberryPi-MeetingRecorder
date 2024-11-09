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
    print(f"Update Client Information : {new_object}")
    org_setting_data=read_clientInfo() 
    org_setting_data["server_share_folder_name"]=new_object["server_share_folder_name"] 
    org_setting_data["server_user_name"]=new_object["server_user_name"]   
    org_setting_data["server_password"]=new_object["server_password"]   
    org_setting_data["usercode"]=new_object["usercode"]
    org_setting_data["usertype"]=new_object["usertype"] 
    write_all_clientInfo(org_setting_data)
    return org_setting_data

# Update Background Image
def update_background_image(image_path):
    print(f"Update Background Image : {image_path}")
    org_setting_data=read_clientInfo()
    org_setting_data["background_image"]=image_path
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

# update free discuss
def update_free_discuss_status(is_start_free_disucss):
     print(f"Update Free Discuss Status : {is_start_free_disucss}")
     org_setting_data=read_clientInfo() 
     if(is_start_free_disucss):
       org_setting_data['is_free_discuss']="true"
     else:
       org_setting_data['is_free_discuss']="false"
     write_all_clientInfo(org_setting_data)         
          
# Write All Client Information
def write_all_clientInfo(app_setting_data):
    with open(file_path, 'w') as file:
        json.dump(app_setting_data, file, indent=4)   


