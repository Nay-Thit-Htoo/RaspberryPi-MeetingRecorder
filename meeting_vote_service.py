from datetime import datetime
import json

# Define appsettings.json file path
file_path = 'Meeting_Vote_Result/meeting_vote_result.json'

# Read Meeting Vote Result
def read_meeting_vote():
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

# Update Meeting Vote Result
def update_vote_result(meeting_title,is_like):
    print(f"Update Meeting Result : {meeting_title}")
    org_data=read_meeting_vote() 
    if(not org_data):
       return
    org_meeting_result_data=org_data['meeting_vote_result']
    for obj in org_meeting_result_data:
        if obj.get('title')==meeting_title:
            like_count=obj['like']
            unLike_count=obj['unlike']
            if(is_like):
                 like_count=like_count+1
            else:
                 unLike_count=unLike_count+1
            new_obj={'like':like_count,'unlike':unLike_count}
            obj.update(new_obj)
            break   
    org_data['meeting_vote_result']=org_meeting_result_data
    write_all_meeting_vote_result(org_data) 

# Add New Meeting Vote Result
def add_new_meeting_vote(meeting_title):
   if(not get_meeting_vote_result_by_title(meeting_title)):
        org_vote_data=read_meeting_vote() 
        vote_obj={
            "title": meeting_title,
            "created_date": datetime.now().strftime("%d-%m-%Y"),
            "like":0,
            "unlike":0
        }    
        org_vote_data['meeting_vote_result'].append(vote_obj)
        write_all_meeting_vote_result(org_vote_data)
        return vote_obj
          
# Get Meeting Vote Result
def get_meeting_vote_result_by_title(meeting_title):
   config_filter=lambda obj: (obj['title']) == meeting_title
   return filter_objects(config_filter)
   
# Filter Meeting Vote Result 
def filter_objects(filter_condition):
    org_vote_result=read_meeting_vote()
    filtered_objects = [obj for obj in org_vote_result['meeting_vote_result'] if filter_condition(obj)]
    return filtered_objects

# Write All Client Information
def write_all_meeting_vote_result(vote_result):
    with open(file_path, 'w') as file:
        json.dump(vote_result, file, indent=4)   

# Reset All Meeting Vote Result
def reset_meeting_vote_result():
    org_meeting_vote_result=read_meeting_vote()
    if(org_meeting_vote_result is not None):
        org_meeting_vote_result['meeting_vote_result']=[]
        write_all_meeting_vote_result(org_meeting_vote_result)   

# Main function to demonstrate the process
# def main(): 
#     # Add Meeting Vote Result 
#     #add_new_meeting_vote("Testing Meeting Vote 2")

#     # Update Meeting Vote Result
#     #update_vote_result("Testing Meeting Vote 2",False)

#     # Get Meeting Vote Result
#     # meeting_vote_result=get_meeting_vote_result_by_title("Testing Meeting Vote 2")
#     # print(f'[Meeting Result]:{meeting_vote_result['like']}')

#     # Read the meeting vote
#     vote_result = read_meeting_vote()
#     print("Original Meeting Vote Result:")
#     print(json.dumps(vote_result, indent=4))

# if __name__ == "__main__":
#     main()


