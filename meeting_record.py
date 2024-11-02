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

class MeetingRecord(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 
        self.logged_user_info=None      
        self.audio_record_service=None 

        main_frame=tk.Frame(self,relief='raised')
        main_frame.pack(padx=50,pady=10)  

        # Font Style for Label
        title_font=tkFont.Font(family="Helvetica", size=14, weight="bold")
        label_font=tkFont.Font(family="Helvetica", size=12)    
        button_font=tkFont.Font(family="Helvetica", size=12)  
        label_sm_font=tkFont.Font(family="Helvetica", size=11)   
        # Create Image and Show on Label
        self.image = Image.open("Assets/mic.png")
        self.photo = ImageTk.PhotoImage(self.image)       
        self.image_label = tk.Label(main_frame, image=self.photo)
        self.image_label.pack(padx=5, pady=5)
        
        self.meeting_status_label = tk.Label(main_frame,fg='Black',font=label_font)
        self.meeting_status_label.pack(padx=5, pady=5) 

        #start & stop buttons
        self.startBtn=tk.Button(main_frame,text="Discuss",bg="#121212", fg="white",width=15,height=2,font=button_font,command=self.start_recording)
        self.startBtn.pack(side=tk.LEFT,padx=5, pady=5)
        self.startBtn.config(state='disabled')

        self.stopBtn=tk.Button(main_frame,text="Stop",bg="#DEE3E2", fg="black",width=15,height=2,font=button_font,command=self.stop_recording)
        self.stopBtn.pack(side=tk.LEFT,padx=5, pady=5)    
        self.stopBtn.config(state='disabled')    
        
        self.muteBtn=tk.Button(main_frame,text="Mute All",bg="#7C00FE", fg="white",width=15,height=2,font=button_font,command=self.mute_action)
        self.muteBtn.pack(side=tk.LEFT,padx=5, pady=5)    
        self.muteBtn.pack_forget()        
  
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
                  user_type=response_message['usertype']
                  if(user_type.lower()!=UserType.CHAIRMAN.value):  
                      self.change_chairman_mute_meeting_status()                                   
                      self.stop_audio_record() 
                  else:
                       self.change_action_status_after_mute_for_client(response_message)
                
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
 
    # Stop Meeting 
    def stop_meeting_action(self):
        self.startBtn.config(state='disabled')
        self.stopBtn.config(state='disabled')                   
        self.muteBtn.pack_forget()
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
    def change_action_status_after_mute_for_client(self,response): 
        self.startBtn.config(state='normal')
        self.stopBtn.config(state='normal')
        self.startBtn.config(text="Discuss")
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
            

    # On Show 
    def on_show(self):     
        self.logged_user_info=clientservice.read_clientInfo()
        self.controller.change_window_title(self.logged_user_info["usercode"])
        socket_thread = threading.Thread(target=self.start_client,args=(None,), daemon=True)
        socket_thread.start()