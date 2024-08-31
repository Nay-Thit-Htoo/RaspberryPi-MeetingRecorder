import json
from datetime import datetime

# Define appsettings.json file path
file_path = 'Settings/appsettings.json'

# Read App Setting Data
def read_setting_data():
    try:
        with open(file_path, 'r') as file:
          config = json.load(file)
    except:
        print(f'{file_path} Not Found!')     
    return config

# Add New App Setting Data
def add_new_appsetting(new_object):
    org_setting_data=read_setting_data() 
    if(not check_exist_appsetting(new_object['username'])):
        org_setting_data['clients'].append(new_object)
    write_all_appsetting(org_setting_data)
    return org_setting_data

# Write All App Setting Data
def write_all_appsetting(app_setting_data):
    try:
        with open(file_path, 'w') as file:
         json.dump(app_setting_data, file, indent=4) 
    except:
        print(f'{file_path} Not Found!')  

# Update App Setting Data
def update_client_info(update_client_data):
    org_data=read_setting_data()
    if(not org_data):
       return False
    org_client_data=org_data['clients']
    for obj in org_client_data:
        if obj.get('username')==update_client_data['username']:
            new_obj={'ipaddress':update_client_data['ipaddress'],'login_date':str(datetime.now())}
            obj.update(new_obj)
            break
    org_data['clients']=org_client_data
    write_all_appsetting(org_data) 
    return True
    
# Check already exist or not in appsettings
def check_exist_appsetting(username):   
    config_filter=lambda obj: (obj['username']).lower() == username.lower()
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
   

# Main function to demonstrate the process
def main():  
    # to_update_object={'username': 'aungaung','ipaddress':"('0.0.0.0',4455)"}
    # update_client_info(to_update_object)
        
    # Read the app setting data
    appsetting_data = read_setting_data()
    print("Original App Settings:")
    print(json.dumps(appsetting_data, indent=4))
    

    # Add new app setting data
    # new_appsetting_data={
    #         "username": "aungaung2",
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