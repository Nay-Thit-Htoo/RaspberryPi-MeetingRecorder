import settings as appsetting

def client_login(login_object):
    print(f'User Login With : {login_object}')
    filter_condition = lambda obj: obj['username'] == login_object['username'] and obj['password'] == login_object['password']
    logged_user_data=appsetting.filter_objects(filter_condition)
    if(not logged_user_data):
         print(f'User Data Not Found !')
         return False
    
    # Update Login Date for user
    to_update_object={'username': login_object['username'],'ipaddress':login_object['ipaddress']}    
    appsetting.update_client_info(to_update_object)
    print(f'Successfully Login!')
    print(f'Update User IP & Date After Login : {login_object}')
    
    return True

def create_new_client(client_object):    
     appsetting.add_new_appsetting(client_object)
   