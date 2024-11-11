from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
from Enum.usertype import UserType
from audio_recorder import AudioRecorder
import client_server_service as clientservice
import socket
import threading
import json

from Enum.actiontype import ActionType
import file_upload_service
from meeting_vote_configuration import MeetingVoteConfiguration
import meeting_vote_service

class MeetingRecord(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 
        self.logged_user_info=None      
        self.audio_record_service=None 

        main_frame=tk.Frame(self,relief='raised')
        main_frame.pack(padx=0,pady=0)  

        # Font Style for Label
        title_font=tkFont.Font(family="Helvetica", size=14, weight="bold")
        label_font=tkFont.Font(family="Helvetica", size=12)    
        button_font=tkFont.Font(family="Helvetica", size=12)  
        label_sm_font=tkFont.Font(family="Helvetica", size=11)   
         
        # Meeting Vote Result
        self.meeting_vote_result_frame=tk.Frame(main_frame)    
        self.meeting_vote_result_frame.pack(fill='x',pady=(0,10))          

        self.meeting_title_label = tk.Label(self.meeting_vote_result_frame,bg="#45474B",fg='white',font=title_font)
        self.meeting_title_label.pack(padx=5, pady=(10,0))
        self.meeting_title_label.pack_forget()
        
        # Region Like Frame
        self.like_frame=tk.Frame(self.meeting_vote_result_frame,bg="#45474B")        
        self.like_frame.pack(side="left",padx=5, pady=(0,0),expand=True)
        self.like_frame.pack_forget()
        
        self.like_count_number = tk.Label(self.like_frame,bg="#45474B",text="0",fg='white',font=title_font) 
        self.like_count_number.pack(side="top",padx=5)       
        self.like_count_number.pack_forget()

        self.like_count_label = tk.Label(self.like_frame,bg="#45474B",text="Like",fg='#F4CE14',font=label_font)
        self.like_count_label.pack(side="top",padx=5)       
        self.like_count_label.pack_forget()

        self.unlike_frame=tk.Frame(self.meeting_vote_result_frame,bg="#45474B") 
        self.unlike_frame.pack(side="right",padx=5, pady=5,expand=True)       
        self.unlike_frame.pack_forget()

        self.unlike_count_number = tk.Label(self.unlike_frame,bg="#45474B",text="0",fg='white',font=title_font)        
        self.unlike_count_number.pack(side="top",padx=5)
        self.unlike_count_number.pack_forget()

        self.unlike_count_label = tk.Label(self.unlike_frame,bg="#45474B",text="Unlike",fg='#F4CE14',font=label_font)  
        self.unlike_count_label.pack(side="top",padx=5)      
        self.unlike_count_label.pack_forget()

        # Create Image and Show on Label
        self.image = Image.open("Assets/mic.png")
        self.photo = ImageTk.PhotoImage(self.image)       
        self.image_label = tk.Label(main_frame, image=self.photo)
        self.image_label.pack(padx=5, pady=5)
        
        self.meeting_status_label = tk.Label(main_frame,fg='Black',font=label_font)
        self.meeting_status_label.pack(padx=5, pady=5) 

        record_frame=tk.Frame(main_frame)
        record_frame.pack(padx=60,pady=5)  

        #start & stop buttons
        self.startBtn=tk.Button(record_frame,text="Discuss",bg="#121212", fg="white",width=15,height=2,font=button_font,command=self.start_recording)
        self.startBtn.pack(side=tk.LEFT,padx=5, pady=5)
        self.startBtn.config(state='disabled')

        self.stopBtn=tk.Button(record_frame,text="Stop",bg="#DEE3E2", fg="black",width=15,height=2,font=button_font,command=self.stop_recording)
        self.stopBtn.pack(side=tk.LEFT,padx=5, pady=5)    
        self.stopBtn.config(state='disabled') 
       
        self.client_like_btn=tk.Button(record_frame,text="Like",bg="#525CEB", fg="white",width=15,height=2,font=button_font,command=self.give_meeting_vote_like)
        self.client_like_btn.pack(side=tk.LEFT,padx=5, pady=5)
        self.client_like_btn.pack_forget()

        self.client_unlike_btn=tk.Button(record_frame,text="Unlike",bg="#1AACAC", fg="white",width=15,height=2,font=button_font,command=self.give_meeting_vote_unlike)
        self.client_unlike_btn.pack(side=tk.LEFT,padx=5, pady=5)    
        self.client_unlike_btn.pack_forget()
        
        other_actions_frame=tk.Frame(main_frame)
        other_actions_frame.pack(padx=60,pady=5)  

        self.muteBtn=tk.Button(other_actions_frame,text="Mute All",bg="#7C00FE", fg="white",width=15,height=2,font=button_font,command=self.mute_action)
        self.muteBtn.pack(side=tk.LEFT,padx=5, pady=5)    
        self.muteBtn.pack_forget()  

        self.freeDiscussBtn=tk.Button(other_actions_frame,text="Free Discuss",bg="#433878", fg="white",width=16,height=2,font=button_font,command=self.free_disucss_action)
        self.freeDiscussBtn.pack(side=tk.LEFT,padx=5, pady=5)    
        self.freeDiscussBtn.pack_forget() 

        self.startVoteBtn=tk.Button(other_actions_frame,text="Meeting Vote",bg="#1A4D2E", fg="white",width=16,height=2,font=button_font,command=self.meeting_start_vote_btn_click)
        self.startVoteBtn.pack(side=tk.LEFT,padx=5, pady=5)   
        self.startVoteBtn.pack_forget()         
    
    #Show Meeting Vote Frame
    def show_meeting_vote_info(self,meeting_vote_title):      
        self.logged_user_info=clientservice.read_clientInfo()
        meeting_vote_obj={"usercode":self.logged_user_info['usercode'],
                    "usertype":self.logged_user_info['usertype'],
                    "actiontype":ActionType.START_MEETING_VOTE.name                      
                    }
        print(f"[Meeting Record][Start Meeting Vote] : {meeting_vote_obj}")
        self.start_client(meeting_vote_obj)
        self.startVoteBtn.config(text="Stop Vote") 
        self.meeting_vote_result_frame.config(bg="#45474B")
        self.meeting_vote_result_frame.pack(fill='x',pady=(0,40),side="top")  
        self.meeting_title_label.pack(padx=5, pady=(10,0)) 
        self.meeting_title_label.config(text=meeting_vote_title)
        self.like_frame.pack(side="left",padx=5, pady=(0,0),expand=True)
        self.like_count_number.pack(side="top",padx=5)
        self.like_count_number.config(text=0)
        self.like_count_label.pack(side="top",padx=5)
        self.unlike_frame.pack(side="right",padx=5, pady=5,expand=True)
        self.unlike_count_number.pack(side="top",padx=5)
        self.unlike_count_number.config(text=0)
        self.unlike_count_label.pack(side="top",padx=5)

    # Stop Meeting Vote Btn Click
    def stop_meeting_vote_btn_click(self):
        current_logged_user_type=self.logged_user_info['usertype']
        if(current_logged_user_type==UserType.CHAIRMAN.value):
            self.upload_meeting_vote_result_to_server()
            self.hide_meeting_vote_info()
            self.logged_user_info=clientservice.read_clientInfo()
            meeting_vote_obj={"usercode":self.logged_user_info['usercode'],
                        "usertype":self.logged_user_info['usertype'],
                        "actiontype":ActionType.STOP_MEETING_VOTE.name                      
                        }
            print(f"[Meeting Record][Stop Meeting Vote] : {meeting_vote_obj}")
            self.start_client(meeting_vote_obj)

    #Hide Meeting Vote Frame
    def hide_meeting_vote_info(self): 
        for widget in self.meeting_vote_result_frame.winfo_children():
          widget.pack_forget() 

    # Meeting Start Vote Btn Click
    def meeting_start_vote_btn_click(self): 
      if(self.startVoteBtn.cget("text")=='Meeting Vote'):    
         MeetingVoteConfiguration(self)        
      else:
         self.startVoteBtn.config(text="Meeting Vote")
         self.stop_meeting_vote_btn_click()
         meeting_vote_service.reset_meeting_vote_result()
   
    # Upload Meeting Vote Result to File Server
    def upload_meeting_vote_result_to_server(self):
        current_logged_user=self.logged_user_info
        print(f"[Meeting Record]:[Meeting Vote Result File Upload]")
        current_logged_user['usercode']=f"Meeting_Vote_Result_{datetime.now().strftime('%d_%m_%Y')}"
        vote_result_file_path="Meeting_Vote_Result"
        print(f'[Meeting Record]:[Vote Result File Path] {vote_result_file_path}')
        vote_result_file_upload_thread = threading.Thread(target=file_upload_service.file_upload_to_server, args=(vote_result_file_path,current_logged_user))
        vote_result_file_upload_thread.start() 

    # Show Client Meeting Vote Btn
    def show_client_meeting_vote_btn(self):         
        current_logged_user_type=self.logged_user_info['usertype']
        if(current_logged_user_type.lower()==UserType.CLIENT.value):
            self.client_like_btn.pack(side=tk.LEFT,padx=5, pady=5)
            self.client_unlike_btn.pack(side=tk.LEFT,padx=5, pady=5)
    
    # Hide Client Meeting Vote Btn
    def hide_client_meeting_vote_btn(self):       
        current_logged_user_type=self.logged_user_info['usertype']
        if(current_logged_user_type.lower()==UserType.CLIENT.value):  
            self.client_like_btn.pack_forget()
            self.client_unlike_btn.pack_forget()
            
    # Update Meeting Vote Count
    def update_meeting_voute_count(self):
        meeting_title=self.meeting_title_label.cget("text")
        if(meeting_title):
            meeting_vote_result=meeting_vote_service.get_meeting_vote_result_by_title(meeting_title)
            if(meeting_vote_result):
                meeting_vote_result=meeting_vote_result[0]
                self.like_count_number.config(text=meeting_vote_result['like'])
                self.unlike_count_number.config(text=meeting_vote_result['unlike'])
            else:
                self.like_count_number.config(text=0)
                self.unlike_count_number.config(text=0)

    # Client Give Meeting Vote ( Like )
    def give_meeting_vote_like(self):
        self.client_like_btn.pack_forget()
        self.client_unlike_btn.pack_forget()
        meeting_vote_obj={"usercode":self.logged_user_info['usercode'],
                "usertype":self.logged_user_info['usertype'],
                "actiontype":ActionType.LIKE_MEETING_VOTE.name                      
                }
        self.start_client(meeting_vote_obj)
        print(f"[Meeting Record][Give Meeting Vote(Like)] : {meeting_vote_obj}")
    
    # Client Give Meeting Vote ( UnLike )
    def give_meeting_vote_unlike(self):
        self.client_like_btn.pack_forget()
        self.client_unlike_btn.pack_forget()
        meeting_vote_obj={"usercode":self.logged_user_info['usercode'],
                "usertype":self.logged_user_info['usertype'],
                "actiontype":ActionType.UNLIKE_MEETING_VOTE.name                      
                }
        self.start_client(meeting_vote_obj)
        print(f"[Meeting Record][Give Meeting Vote(UnLike)] : {meeting_vote_obj}")
    
    # start recording
    def start_recording(self): 
     if(self.startBtn.cget("text").lower()=='discuss'):       
        meeting_record_obj={"usercode":self.logged_user_info['usercode'],
                        "usertype":self.logged_user_info['usertype'],
                        "actiontype":ActionType.START_RECORD.name                      
                        }        
        # Get Meeting Status & Confirm Dialog for Discussion
        meeting_status=self.meeting_status_label.cget('text')
        if(meeting_status is not None and meeting_status !=""):
            if(self.logged_user_info['usertype'].lower()==UserType.CLIENT.value):                
                discuss_result = messagebox.askyesno("Request for Discussion", f'Do you want to join Discussion?')
                if discuss_result: 
                    self.startBtn.config(text="Please Wait...")
                    meeting_record_obj["actiontype"]=ActionType.DISCUSS_REQUEST.name 
                else:
                    return               
        print(f"[Meeting Record][Start Record] : {meeting_record_obj}")
        self.start_client(meeting_record_obj)
    
    #start meeting
    def start_meeting(self):       
        self.logged_user_info=clientservice.read_clientInfo()
        meeting_record_obj={"usercode":self.logged_user_info['usercode'],
                    "usertype":self.logged_user_info['usertype'],
                    "actiontype":ActionType.START_MEETING.name                      
                    }
        print(f"[Meeting Record][Start Meeting] : {meeting_record_obj}")
        self.start_client(meeting_record_obj)
    
    #stop meeting
    def stop_meeting(self): 
        meeting_record_obj={"usercode":self.logged_user_info['usercode'],
                    "usertype":self.logged_user_info['usertype'],
                    "actiontype":ActionType.STOP_MEETING.name                      
                    }
        print(f"[Meeting Record][Stop Meeting] : {meeting_record_obj}")
        self.start_client(meeting_record_obj)        

    #free Discuss Action
    def free_disucss_action(self):      
        free_discuss_btn_txt=self.freeDiscussBtn.cget("text").lower().replace(" ","")
        self.logged_user_info=clientservice.read_clientInfo()
        free_discuss_obj={"usercode":self.logged_user_info['usercode'],
                    "usertype":self.logged_user_info['usertype'],
                    "actiontype":ActionType.START_FREE_DISCUSS.name                      
                    }               
        if(free_discuss_btn_txt=='freediscuss'):  
          meeting_status=self.meeting_status_label.cget('text')
          if(self.startBtn.cget("text").lower()=='discuss' and meeting_status==""):
             print(f"[Meeting Record][Start Free Discuss] : {free_discuss_obj}")
             free_discuss_obj['actiontype']=ActionType.START_FREE_DISCUSS.name
             self.freeDiscussBtn.config(text="Stop Free Discuss")
             self.freeDiscussBtn.config(bg="#FF8343")
        else:
            print(f"[Meeting Record][Stop Free Discuss] : {free_discuss_obj}")
            free_discuss_obj['actiontype']=ActionType.STOP_FREE_DISCUSS.name
            self.freeDiscussBtn.config(text="Free Discuss")
            self.freeDiscussBtn.config(bg="#1A4D2E")
    
        self.start_client(free_discuss_obj)
        
    # stop recording
    def stop_recording(self):
       if(self.startBtn.cget("text").lower() =='discussing'):      
            self.meeting_status_label.config(text="")
            self.logged_user_info=clientservice.read_clientInfo()
            meeting_record_obj={"usercode":self.logged_user_info['usercode'],
                    "usertype":self.logged_user_info['usertype'],
                    "actiontype":ActionType.STOP_RECORD.name                      
                    }   
            print(f"[Meeting Record][Stop Record] : {meeting_record_obj}")
            self.start_client(meeting_record_obj)       
    
    # Receive Message via Client Socket
    def receive_messages(self,client_socket):
        print(f"Meeting Record][Receive Message]: {client_socket}")
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"[Meeting Record][Receive Message Reply From Server] : {message}")
                response_message=json.loads(message.replace("'", '"')) 
                print(f"[Meeting Record][Action Type]: {response_message['actiontype']}") 
                action_type=response_message['actiontype']  
             
                # Filter Action Type              
                if(action_type==ActionType.START_MEETING.name): 
                   self.start_meeting_action()
                elif(action_type==ActionType.STOP_MEETING.name): 
                  self.stop_meeting_action()
                elif(action_type==ActionType.START_RECORD.name or action_type==ActionType.ACCESS_DISCUSS.name): 
                   self.change_meeting_status_after_startrecord(response_message)                 
                elif(action_type==ActionType.OPEN_RECORD.name):                   
                    self.open_meeting_record_page(response_message)
                elif(action_type==ActionType.STOP_RECORD.name):
                  self.clear_meeting_status_enable_buttons()
                  if(self.logged_user_info['usercode']==response_message['usercode']):
                        self.stop_audio_record()                   
                elif(action_type==ActionType.DISCUSS_REQUEST.name):            
                   self.check_discuss_request_confirmation(response_message)
                elif(action_type==ActionType.REJECT_DISCUSS.name):            
                   self.reject_discuss(response_message)       
                elif(action_type==ActionType.MUTE_ALL.name):
                  self.change_action_status_after_mute(response_message)       
                elif(action_type==ActionType.START_FREE_DISCUSS.name):          
                    clientservice.update_free_discuss_status(True)
                elif(action_type==ActionType.STOP_FREE_DISCUSS.name):          
                    clientservice.update_free_discuss_status(False)
                elif(action_type==ActionType.START_MEETING_VOTE.name):          
                    self.show_client_meeting_vote_btn()
                elif(action_type==ActionType.STOP_MEETING_VOTE.name):          
                    self.hide_client_meeting_vote_btn()
                elif(action_type==ActionType.LIKE_MEETING_VOTE.name):          
                    meeting_vote_service.update_vote_result(self.meeting_title_label.cget("text"),True)
                    self.update_meeting_voute_count()
                elif(action_type==ActionType.UNLIKE_MEETING_VOTE.name):          
                    meeting_vote_service.update_vote_result(self.meeting_title_label.cget("text"),False)
                    self.update_meeting_voute_count()
                                  
            except Exception as err:
                print(f"[Meeting Record]:[Exception Error] : {err}")                
                break
            except ConnectionAbortedError as connError:
               print(f"[Meeting Record]:[Connection Aborted Error] : {connError}")                
               break 
 
    # Start Meeting
    def start_meeting_action(self):
        current_logged_user_type=self.logged_user_info['usertype']
        self.startBtn.config(state='normal')
        self.stopBtn.config(state='normal')
        if(current_logged_user_type.lower()=="chairman"):            
            self.muteBtn.pack(side=tk.LEFT,padx=5, pady=5)
            self.freeDiscussBtn.pack(side=tk.LEFT,padx=5, pady=5)
            self.startVoteBtn.pack(side=tk.LEFT,padx=5, pady=5)
 
    # Stop Meeting 
    def stop_meeting_action(self):
        self.startBtn.config(state='disabled')
        self.stopBtn.config(state='disabled')                   
        self.muteBtn.pack_forget()
        self.freeDiscussBtn.pack_forget()
        self.startVoteBtn.pack_forget()
        self.client_like_btn.pack_forget()
        self.client_unlike_btn.pack_forget()
        self.stop_meeting_vote_btn_click()
        self.change_recording_icon_status_to_original()
        self.stop_audio_record()

    # Mute Btn
    def mute_action(self):   
        meeting_status=self.meeting_status_label.cget('text')
        if(meeting_status is not None and meeting_status !="" and self.logged_user_info["usertype"].lower()=="chairman"):    
            meeting_record_obj={"usercode":self.logged_user_info['usercode'],
                    "usertype":self.logged_user_info['usertype'],
                    "actiontype":ActionType.MUTE_ALL.name                      
                    }
            print(f"[Meeting Record][Mute All] : {meeting_record_obj}")
            self.start_client(meeting_record_obj)

    # Change Meeting Status and Disable or Enable Start and Stop Buttons 
    def change_meeting_status_after_startrecord(self,response):
       print(f"[Meeting Recording][Meeting Status]: {response}")
       if(response['is_starting_meeting']=="true"): 
            self.startBtn.config(state='normal')
            self.stopBtn.config(state='normal')        
            if(response['message']!=""):
                new_image = Image.open("Assets/recording-mic.png")
                new_image_tk = ImageTk.PhotoImage(new_image)

                self.image_label.config(image=new_image_tk)
                self.image_label.image = new_image_tk
                self.meeting_status_label.config(text=f"{response['message']} recording......")
                  
                if(self.logged_user_info['usercode']==response['usercode']):
                    self.startBtn.config(state='disabled') 
                    self.startBtn.config(text="Discussing")
                    self.start_audio_record()  
      
    # Audio Record Start
    def start_audio_record(self):
        self.audio_record_service=AudioRecorder(self.logged_user_info)
        self.audio_record_service.start_recording()

    # Audio Record Stop
    def stop_audio_record(self):        
        if(self.audio_record_service is None):
             self.audio_record_service=AudioRecorder(self.logged_user_info)
        self.audio_record_service.stop_recording()        
        self.audio_record_service.terminate()
    
    # Create Folder After PageLoaded
    def open_meeting_record_page(self,response):
        print(f"[Meeting Record][Open Record]: {response}")
        if("message_code" in response):
            if(response['message_code']=="fail"):
                messagebox.showerror("Folder Creation Message",response['message'])
                self.clear_meeting_status_enable_buttons()                   
            elif(response['message_code']=="success"):
                self.change_meeting_status_after_startrecord(response)
      
    # Change to Mic Icon and Meeting Status
    def change_recording_icon_status_to_original(self):
        new_image = Image.open("Assets/mic.png")
        new_image_tk = ImageTk.PhotoImage(new_image)

        self.image_label.config(image=new_image_tk)
        self.image_label.image = new_image_tk

        self.meeting_status_label.config(text="")
        self.startBtn.config(text="Discuss") 

   # Clean meeting status and enable start & stop buttons
    def clear_meeting_status_enable_buttons(self):
        self.change_recording_icon_status_to_original()
        self.startBtn.config(state='normal')
        self.stopBtn.config(state='normal')
        
    # Function to send messages to the server
    def send_messages(self,client_socket,client_message): 
        print(f"[Meeting Record][Send Client Message] : {client_message}")
        recipient_ip = socket.gethostbyname(socket.gethostname())
        full_message=f"{recipient_ip}: {client_message}"
        client_socket.send(full_message.encode('utf-8'))
    
    # Set up client socket
    def start_client(self,client_message):
        self.logged_user_info=clientservice.read_clientInfo()
        logged_user_server_ip=self.logged_user_info['server_ip']
        logged_user_server_port=int(self.logged_user_info['server_port']) 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
        client_socket.connect((logged_user_server_ip, logged_user_server_port))        

        # Start threads for receiving and sending messages
        receive_msg_thread = threading.Thread(target=self.receive_messages,args=(client_socket,),daemon=True)
        receive_msg_thread.start()    
        
        empty_obj={"usercode":self.logged_user_info['usercode'],"usertype": self.logged_user_info['usertype'],"actiontype":ActionType.OPEN_RECORD.name}
        client_message=client_message if (client_message is not None) else empty_obj
        send_mesg_thread = threading.Thread(target=self.send_messages, args=(client_socket, client_message,))
        send_mesg_thread.start()
     
    # Check and Request Confirmation for Discussion
    def check_discuss_request_confirmation(self,response):
        print(f"[Meeting Record][Show Confirm Dialog by Chairman]:{response}")
        current_user_type=self.logged_user_info['usertype']
        if(current_user_type is not None and current_user_type.lower()=="chairman"):
            record_user_lst=response['recording_users']        
            request_user_code=response['usercode']
            discuss_obj={"usercode":request_user_code,"usertype": self.logged_user_info['usertype'],"actiontype":ActionType.ACCESS_DISCUSS.name,"recording_users":record_user_lst}
            if(record_user_lst is None or (len(record_user_lst)>0 and not (request_user_code in record_user_lst))):
                confirm_msg=f"Do you want to allow {response['usercode']} for Discussion?"
                confrim_result = messagebox.askyesno("Request for Discussion",confirm_msg)
                discuss_obj["actiontype"]=ActionType.ACCESS_DISCUSS.name if(confrim_result) else ActionType.REJECT_DISCUSS.name
            self.start_client(discuss_obj)
    
    # Reject Result Show
    def reject_discuss(self,response):
        if(response['usercode']==self.logged_user_info['usercode']):
          messagebox.showinfo("Reject Message","You can't join current Discussoin")   
    
    # Change Chairman Mute Label
    def change_chairman_mute_meeting_status(self):
       if(self.startBtn.cget("text").lower() in 'discussing'): 
            self.meeting_status_label.config(text=f"{self.logged_user_info['usercode']} recording......")  
       
    # Change Status after mute 
    def change_action_status_after_mute(self,response): 
        user_type=self.logged_user_info['usertype']   
        record_user_lst=response['recording_users'] 
        if(record_user_lst is not None and (len(record_user_lst)>0)):
            new_image = Image.open("Assets/recording-mic.png")
            new_image_tk = ImageTk.PhotoImage(new_image)

            self.image_label.config(image=new_image_tk)
            self.image_label.image = new_image_tk
            
            recording_users=", ".join(record_user_lst)
            self.meeting_status_label.config(text=f"{recording_users} recording......")
        else:
            new_image = Image.open("Assets/mic.png")
            new_image_tk = ImageTk.PhotoImage(new_image)

            self.image_label.config(image=new_image_tk)
            self.image_label.image = new_image_tk
            self.meeting_status_label.config(text="")

        if(user_type.lower()==UserType.CLIENT.value):
            self.startBtn.config(state='normal')
            self.stopBtn.config(state='normal')
            self.startBtn.config(text="Discuss")
            self.stop_audio_record()
       
    # On Show 
    def on_show(self):     
        self.logged_user_info=clientservice.read_clientInfo()
        self.controller.change_window_title(self.logged_user_info["usercode"])
        socket_thread = threading.Thread(target=self.start_client,args=(None,), daemon=True)
        socket_thread.start()