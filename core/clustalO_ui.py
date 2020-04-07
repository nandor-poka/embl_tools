__name__ = 'clustalO_ui'
import ipywidgets as widgets
from IPython.display import display
import subprocess
from time import sleep
import re
import os
from ipyfilechooser import FileChooser
clustalo_cmd = 'python3 embl_client/clustalo.py '
style = {'description_width': 'initial'}

#Defining UI elements / widgets
app_label = widgets.Label(value='EMBL-Tools ClustalO webservice')

# Widgets for mandatory information
mandatory_label = widgets.Label(value='Mandatory options')
email_input = widgets.Text(value='', placeholder='email address (mandatory)', description='Email (mandatory):',style = style )

sequence_type = widgets.Dropdown(
    options = [('DNA','dna'), ('RNA', 'rna'),('Protein', 'protein')],
    value='dna',
    description='Sequence type:',
    style = style
)
#seq_file_input = widgets.Text(description = 'Sequence file path',style = style, disabled = False)
seq_file_input = FileChooser('./', title = 'Sequence file path',style = style, disabled = False)
seq_file_input.use_dir_icons = True
submit = widgets.Button(description='Submit',disabled=False, button_style='', tooltip='Submit job',style = style, icon='check')
output = widgets.Output(layout={'border': '1px solid black'})

# Widgets for optional options
optional_label = widgets.Label(value='Extra options')
output_file_name = widgets.Text(description = 'Save result as: ',style = style, disabled = False)


#Callback for the submitbutton
@output.capture()
def submit_job(b):
    if not check_email():
        return
    if not check_file():
        return
    
    command = prepare_command()
    print("submitting job:" +command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    jobid = out.decode('UTF-8').split('\n')[0]
    print(out.decode('UTF-8'))
    
    proc = subprocess.Popen([clustalo_cmd + ' --status --jobid '+ jobid], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print(out.decode('UTF-8'))
    status = out.decode('UTF-8').split('\n')[1]
    print ('Jobid: '+jobid)
    
    while status == 'RUNNING':
        sleep(5)
        proc = subprocess.Popen([clustalo_cmd + ' --status --jobid '+ jobid], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        status = out.decode('UTF-8').split('\n')[1]
        print (status)
    
    fetch_result(jobid)
    
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

output.capture()
def check_file():
    file_path = seq_file_input.selected
    if file_path and os.path.isfile(file_path) and os.access(file_path, os.R_OK):
        return True
    else:
        print("Either the file is missing or not readable")
        return False

def prepare_command():
    command = clustalo_cmd + '--email '+email_input.value + ' --stype ' +sequence_type.value + ' --sequence ' + seq_file_input.selected  
    command += ' --asyncjob'
    return command

def append_outfile(cmd):
    command = cmd
    if output_file_name.value:
        command += ' --outfile '+ output_file_name.value
    else:
        command += ' --outfile ' + jobid
    return command

def fetch_result(jobid):
    command = clustalo_cmd + ' --polljob --jobid '+ jobid
    command = append_outfile(command)
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print (out.decode('UTF-8'))

submit.on_click(submit_job)
mandatory_options = widgets.VBox([mandatory_label, email_input, sequence_type, seq_file_input, submit])
optional_options = widgets.VBox([optional_label, output_file_name])
center_container = widgets.HBox([mandatory_options, optional_options])

app_layout = widgets.AppLayout(
    header= app_label,
    left=None,
    center = center_container,
    right= None,
    footer = output
)

display(app_layout)