import Settings as appsetting

def login_client(login_object):
    filter_condition = lambda obj: obj['username'] == login_object['username']
    logged_user_data=appsetting.filter_objects(filter_condition)
    if(logged_user_data):
         return False
    
    # Update Login Date for user
    to_update_object={'username': login_object['username'],'ipaddress':"('0.0.0.0',4455)"}
    appsetting.update_client_info(to_update_object)
    
    return True
   