__name__ = 'template_ui' #rename this to real module name
import ipywidgets as widgets
from IPython.display import display
import subprocess
from time import sleep
import re
import os

service_cmd ="python3 ../embl_client/service.py" # TODO replace service.py with real embl client python file name.
style = {'description_width': 'initial'}


#Defining UI elements / widgets
app_label = widgets.Label(value='EMBL-Tools Template webservice') # TODO replace with real application label text

# Widgets for mandatory information, starting with predefined label and email input
mandatory_label = widgets.Label(value='Mandatory options')
email_input = widgets.Text(value='', placeholder='email address (mandatory)', description='Email (mandatory):',style = style )

#add more widgets as you need below this line


# predefined submit and output
submit = widgets.Button(description='Submit',disabled=False, button_style='', tooltip='Submit job',style = style, icon='check')
output = widgets.Output(layout={'border': '1px solid black'})


# Widgets for optional options, add widgets as you need
optional_label = widgets.Label(value='Extra options')



# Mostly generic logic

#Callback for the submitbutton, TODO modify as needed
@output.capture()
def submit_job(b):
    if not check_email():
        return
    # add more checks here for early returns.
    
    command = prepare_command()
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    jobid = out.decode('UTF-8').split('\n')[0]
    
    proc = subprocess.Popen([service_cmd + ' --status --jobid '+ jobid], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    status = out.decode('UTF-8').split('\n')[1]
    print ('Jobid: '+jobid)
    
    while status == 'RUNNING':
        sleep(5)
        proc = subprocess.Popen([service_cmd + ' --status --jobid '+ jobid], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        status = out.decode('UTF-8').split('\n')[1]
        print (status)
    
    fetch_result()

# This can stay as is, checks if email is valid
@output.capture()
def check_email():
    if "".__eq__(email_input.value):
        print ("Email address is empty. Please fill in the email address field")
        return False
    email_match = re.match(r".*@*\..*", email_input.value)
    if email_match == None:
        print ("Email address is not valid. Please use <account_name>@<privder> format. Example: mail@example.com")
        return False
    return True

# modify as needed.
def prepare_command():
    command = service_cmd + '--email '+email_input.value # add more options as needed for the base command    
    command += ' --asyncjob'
    return command

# Util method to append correct outfile param
def append_outfile(cmd):
    command = cmd
    if output_file_name.value:
        command += ' --outfile '+ output_file_name.value
    else:
        command += ' --outfile ' + jobid
    return command

def fetch_result():
    command = service_cmd + ' --polljob --jobid '+ jobid
    command = append_outfile(command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print (out.decode('UTF-8'))

submit.on_click(submit_job)
                             
# Define layout                             
mandatory_options = widgets.VBox([mandatory_label, email_input, submit])
optional_options = widgets.VBox([optional_label])
center_container = widgets.HBox([mandatory_options, optional_options])

app_layout = widgets.AppLayout(
    header= app_label,
    left=None,
    center = center_container,
    right= None,
    footer = output
)

display(app_layout)