import json
from datetime import datetime

# Define server_setting.json file path
file_path = 'server_setting.json'

# Read App Setting Data
def read_setting_data():
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

# Add New App Setting Data
def add_new_appsetting(new_object):
    org_setting_data=read_setting_data() 
    if(not check_exist_appsetting(new_object['usercode'])):
        org_setting_data['clients'].append(new_object)
    write_all_appsetting(org_setting_data)
    return org_setting_data

# Write All App Setting Data
def write_all_appsetting(app_setting_data):
    with open(file_path, 'w') as file:
        json.dump(app_setting_data, file, indent=4)   

# Update App Setting Data
def update_client_info(update_client_data):
    org_data=read_setting_data()
    if(not org_data):
       return
    org_client_data=org_data['clients']
    for obj in org_client_data:
        if obj.get('usercode')==update_client_data['usercode']:
            new_obj={'ipaddress':update_client_data['ipaddress'],'login_date':str(datetime.now())}
            obj.update(new_obj)
            break
    org_data['clients']=org_client_data
    write_all_appsetting(org_data) 

# Check already exist or not in appsettings
def check_exist_appsetting(usercode):   
    config_filter=lambda obj: (obj['usercode']).lower() == usercode.lower()
    config_result=filter_objects(config_filter)       
    if(config_result):
      print(f"User Already Exist already exist in settings")
      return True
    return False

# Filter App Setting Data    
def filter_objects(filter_condition):
    org_setting_data=read_setting_data()
    filtered_objects = [obj for obj in org_setting_data['clients'] if filter_condition(obj)]
    return filtered_objects

# Get Current Recording User
def get_current_recording_user():    
    org_setting_data=read_setting_data()
    recording_filter=lambda obj: obj['is_recording'] == "true"
    current_recording_user = [obj for obj in org_setting_data['clients'] if recording_filter(obj)]
    return current_recording_user

# Get Is Starting Meeting
def get_meeting_status():    
    org_setting_data=read_setting_data()
    return org_setting_data['is_starting_meeting']

# Update Meeting Record Person
def update_recording_client_info(update_client_data,is_start_recording,is_mute_all=False):
    org_data=read_setting_data()
    if(not org_data):
       return
    org_client_data=org_data['clients']
    for obj in org_client_data:
        if is_mute_all:
            new_obj={'is_recording':"false"}
            obj.update(new_obj)
        elif obj.get('usercode')==update_client_data['usercode']:            
            new_obj={'is_recording':"true"} if(is_start_recording) else {'is_recording':"false"}
            obj.update(new_obj)
            break 
        
    org_data['clients']=org_client_data
    write_all_appsetting(org_data) 

# Update Meeting Record Person
def update_meeting_status(is_start_meeting):
    org_data=read_setting_data()
    if(not org_data):
       return
    org_data['is_starting_meeting']=is_start_meeting
    write_all_appsetting(org_data) 


# Update Background Image
def update_background_image_path(background_img_path):
    org_data=read_setting_data()
    if(not org_data):
       return
    org_data['background_image']=background_img_path
    write_all_appsetting(org_data) 

# Filter App Setting Data    
def clean_clients():
    org_setting_data=read_setting_data()
    if(org_setting_data is not None):
        org_setting_data['clients']=[]
        write_all_appsetting(org_setting_data)   
   
# Update Server Info
def update_server_info(updated_server_obj):
    org_data=read_setting_data()
    if(not org_data):
       return
    org_data["server_port_number"]=int(updated_server_obj["server_port_number"])
    org_data["server_share_folder_path"]=updated_server_obj["server_share_folder_path"]
    org_data["server_share_folder_name"]=updated_server_obj["server_share_folder_name"]
    org_data["server_user_name"]=updated_server_obj["server_user_name"]
    org_data["server_password"]=updated_server_obj["server_password"]
    write_all_appsetting(org_data)

# Main function to demonstrate the process
def main():  
    # to_update_object={'usercode': 'aungaung','ipaddress':"('0.0.0.0',4455)"}
    # update_client_info(to_update_object)
        
    # Read the app setting data
    appsetting_data = read_setting_data()
    print("Original Server Settings:")
    print(json.dumps(appsetting_data, indent=4))
    

    # Add new app setting data
    # new_appsetting_data={
    #         "usercode": "aungaung2",
    #         "password": "123",
    #         "type": "client",
    #         "login_date": "2024-08-30 14:23:30.601087",
    #         "ipaddress": "('192.168.29.2',3223)"
    #     }
    # add_new_appsetting(new_appsetting_data)





    # Update the config
    # new_object = {"name": '192.168.1.10',"type": "client"}
    # updated_config = update_config(config, new_object)
    
    # Write the updated config back to the file
    #write_config(updated_config)
    
    # Print the updated config
    # print("\nOriginal App Settings:")
    # print(json.dumps(updated_config, indent=4))    

    # Filter with ip address name
    # filter_condition = lambda obj: obj['name'] == '192.168.1.23'
    # filtered_objects = filter_objects(updated_config['clients'], filter_condition)
    
    # Print the filtered objects
    #print("\nFiltered App Settings:")
    #print(json.dumps(filtered_objects, indent=4))
    #print(filtered_objects[0]['name'])

if __name__ == "__main__":
    main()