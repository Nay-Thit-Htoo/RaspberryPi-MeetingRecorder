import json
from datetime import datetime

# Define appsettings.json file path
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

# Update User Login Date
def update_user_info(update_user_data):
    org_data=read_setting_data()
    if(not org_data):
       return
    org_client_data=org_data['clients']
    for obj in org_client_data:
        if obj.get('usercode')==update_user_data['usercode']:
            new_obj={'login_date':str(datetime.now())}
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

# Check Chairman User Already Exist or Not
def check_chairman_user_exist_appsetting(usertype):   
    print(f'[User Login Service]: [Check Chairman] : {usertype}')
    config_filter=lambda obj: (obj['usertype']).lower() == usertype.lower()
    config_result=filter_objects(config_filter)       
    if(config_result):
      print(f"Chairman user Already Exist already exist in settings")
      return True
    return False

# Filter App Setting Data    
def filter_objects(filter_condition):
    org_setting_data=read_setting_data()
    filtered_objects = [obj for obj in org_setting_data['clients'] if filter_condition(obj)]
    if(len(filtered_objects)>0):
         filtered_objects[0]['upload_file_path']=org_setting_data['upload_file_path']
         return filtered_objects[0]     
    return filtered_objects
   
def user_login(login_user_data):
    print(f'[User Login Service] : Login Request : {login_user_data}')
    config_filter=lambda obj: (obj['usercode']).lower() == login_user_data['usercode'].lower()
    config_result=filter_objects(config_filter)
    if(config_result):
         return {
            "message": "User Already Used",
            "message_code": "fail"            
          }
    else:
        user_type=login_user_data['usertype']       
        if(user_type.lower()=="chairman" and check_chairman_user_exist_appsetting(user_type)):
            return {
                "message": "Chairman User Already Exist in Server",
                "message_code": "fail"
            }
        else :
            newuser_obj={
                "usercode": login_user_data['usercode'],
                "login_date":str(datetime.now()),
                "usertype": login_user_data['usertype'],
                "message":"Login Success",
                "message_code":"success",
                "is_recording": "false"                                   
            }            
            add_new_appsetting(newuser_obj)
            config_filter=lambda obj: (obj['usercode']).lower() == login_user_data['usercode'].lower()
            return filter_objects(config_filter)
 
# Remove Login User after UI Close 
def remove_login_user(login_user_data):
    org_data=read_setting_data()
    if(not org_data):
       return
    org_client_data=org_data['clients']
    for obj in org_client_data:
        if obj.get('usercode')==login_user_data['usercode']:            
            org_client_data.remove(obj)
            break
    org_data['clients']=org_client_data
    write_all_appsetting(org_data) 
    
# Remove All Login User Information after Server Restart
def remove_all_login_user():
    org_data=read_setting_data()
    if(not org_data):
       return  
    org_data['clients']=[]
    write_all_appsetting(org_data) 

# Main function to demonstrate the process
# def main():  
#     #remove_all_login_user()
#     # to_update_object={'usercode': 'aungaung','ipaddress':"('0.0.0.0',4455)"}
#     # update_client_info(to_update_object)
        
#     # Read the app setting data
#     # appsetting_data = read_setting_data()
#     # print("Original App Settings:")
#     # print(json.dumps(appsetting_data, indent=4))
    
#     # login_userdata={
#     #     "usercode": '345623791',             
#     #     "type": 'client',
#     #  }
#     # print("User Login:")
#     # print(json.dumps(user_login(login_userdata), indent=4))

#     login_userdata={
#         "usercode": '345623791',             
#         "usertype": 'client',
#      }
#     print("Remove Logged User:")
#     print(json.dumps(remove_login_user(login_userdata), indent=4))
 
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