__name__ = 'clustal_ui'
import ipywidgets as widgets
from IPython.display import display
import subprocess
from time import sleep
import re
import os
clustalo_cmd = 'python3 ../embl_client/clustalo.py '
style = {'description_width': 'initial'}

#Defining UI elements / widgets
app_label = widgets.Label(value='EMBL-Tools ClustalO webservice')
email_input = widgets.Text(value='', placeholder='email address (mandatory)', description='Email (mandatory):',style = style )

sequence_type = widgets.Dropdown(
    options = [('DNA','dna'), ('RNA', 'rna'),('Protein', 'protein')],
    value='dna',
    description='Sequence type:',
    style = style
)

seq_file_input = widgets.Text(description = 'Sequence file path',style = style, disabled = False)

submit = widgets.Button(description='Submit',disabled=False, button_style='', tooltip='Submit job',style = style, icon='check')

output = widgets.Output(layout={'border': '1px solid black'})

#Callback for the submitbutton
@output.capture()
def submit_job(b):
    if not check_email():
        return
    if not check_file():
        return
    proc = subprocess.Popen([clustalo_cmd + ' --email '+email_input.value+' --stype '+sequence_type.value+' --sequence '+ seq_file_input.value+' --asyncjob'], 
                            stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    jobid = out.decode("UTF-8").split('\n')[0]
    
    proc = subprocess.Popen([clustalo_cmd + ' --status --jobid '+ jobid], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    status = out.decode("UTF-8").split('\n')[1]
    print ('Jobid: '+jobid)
    while status == 'RUNNING':
        sleep(5)
        proc = subprocess.Popen([clustalo_cmd + ' --status --jobid '+ jobid], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        status = out.decode("UTF-8").split('\n')[1]
        print (status)
    proc = subprocess.Popen([clustalo_cmd + ' --polljob --jobid '+ jobid + ' --outfile '+ jobid], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print (out.decode("UTF-8"))
    
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
    file_path = seq_file_input.value
    if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
        return True
    else:
        print("Either the file is missing or not readable")
        return False
    
submit.on_click(submit_job)

center_container = widgets.HBox([email_input, seq_file_input, sequence_type, submit])

app_layout = widgets.AppLayout(
    header= app_label,
    left=None,
    center = center_container,
    right= None,
    footer = output
)

#display(email_input)
#display(seq_file_input)
#display(sequence_type)
#display(submit)
#display(output)
display(app_layout)