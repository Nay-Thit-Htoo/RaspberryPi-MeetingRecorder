import json

# Read the JSON configuration file
def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

# Update the JSON data
def update_config(configObj, new_object):
    if(not check_exist_config(configObj,new_object['name'])):
        configObj['clients'].append(new_object)
    return configObj

# Write the updated data back to the file
def write_config(file_path, configObj):
    with open(file_path, 'w') as file:
        json.dump(configObj, file, indent=4)

# Check already exist or not in appsettings
def check_exist_config(configObj,clientName):   
    config_filter=lambda obj: obj['name'] == clientName
    config_result=filter_objects(configObj['clients'], config_filter)    
    if(config_result):
      print(f"IP Address already exist in settings")
      return True
    return False
    

def filter_objects(configObj, filter_condition):
    filtered_objects = [obj for obj in configObj if filter_condition(obj)]
    return filtered_objects
    
# Main function to demonstrate the process
def main():
    file_path = 'Settings/appsettings.json'
    
    # Read the config
    config = read_config(file_path)
    print("Original App Settings:")
    print(json.dumps(config, indent=4))
    
    # Update the config
    new_object = {"name": '192.168.1.10',"type": "client"}
    updated_config = update_config(config, new_object)
    
    # Write the updated config back to the file
    write_config(file_path, updated_config)
    
    # Print the updated config
    print("\nOriginal App Settings:")
    print(json.dumps(updated_config, indent=4))    

    # Filter with ip address name
    filter_condition = lambda obj: obj['name'] == '192.168.1.23'
    filtered_objects = filter_objects(updated_config['clients'], filter_condition)
    
    # Print the filtered objects
    print("\nFiltered App Settings:")
    print(json.dumps(filtered_objects, indent=4))
    print(filtered_objects[0]['name'])

if __name__ == "__main__":
    main()