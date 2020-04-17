__name__ = 'clustalO_ui'
import ipywidgets as widgets
from IPython.display import display
import subprocess, re, os, json
from time import sleep
from ipyfilechooser import FileChooser


clustalo_cmd = 'python3 embl_client/clustalo.py '
style = {'description_width': 'initial'}
fixed_width_layout = widgets.Layout(width='50%', min_width='50%',max_width='50%')

# Checking if settings file exists and reading contents for default values to use.
settings = None
initLog = ''
if os.path.exists('./settings.json'):
    with open('./settings.json', 'r') as settingsFile:
        settingsData = settingsFile.read()
        settingsFile.close()
        settings = json.loads(settingsData)
    initLog += "Settings loaded.\n"
    for setting in settings:
        initLog += settings[setting]+'\n'
    if not os.path.exists(settings['outdir']):
        initLog += 'Default output directory does not exists. Attempting to create it.\n'
        try:
            os.makedirs(settings['outdir'])
            initLog += settings['outdir'] + ' is created.\n'
        except Exception as exception:
            print (type(exception), exception)
else:
    initLog += 'No settings file found.\n'

# Defining UI elements / widgets
app_label = widgets.Label(value='EMBL-Tools ClustalO webservice')

# Widgets for mandatory information
mandatory_label = widgets.Label(value='Mandatory options')
email_input = widgets.Text(value= settings['email'] if settings['email'] != None else '', placeholder='email address (mandatory)', description='Email (mandatory):',style = style )

sequence_type = widgets.Dropdown(
    options = [('DNA','dna'), ('RNA', 'rna'),('Protein', 'protein')],
    value='dna',
    description='Sequence type:',
    style = style
)

seq_file_input = FileChooser('./', title = 'Sequence file',style = style, disabled = False)
seq_file_input.use_dir_icons = True
submit = widgets.Button(description='Submit',disabled=False, button_style='', tooltip='Submit job',style = style, icon='check')
output = widgets.Output(layout={'border': '1px solid black'})

# Widgets for optional options
optional_label = widgets.Label(value='Extra options')
output_file_name = widgets.Text(description = 'Save result as: ',style = style, disabled = False)
output_dir = FileChooser(settings['outdir'] if settings['outdir'] != None else '.', title = 'Save output to',style = style, disabled = False)
output_dir.default_path = settings['outdir'] if settings['outdir'] != None else '.'

with output:
    print(initLog)

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
    print ('Jobid: '+jobid)
    
    proc = subprocess.Popen([clustalo_cmd + ' --status --jobid '+ jobid], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print(out.decode('UTF-8'))
    status = out.decode('UTF-8').split('\n')[1]
   
    
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
    email_match = re.match(r".*@.*\..*", email_input.value)
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

def append_outfile(cmd, jobid):
    command = cmd
    outfile_str = None;
    if output_dir.selected_path:
        outfile_str = output_dir.selected_path
    else:
        outfile_str = output_dir.default_path
        
    if output_file_name.value:
        outfile_str += '/'+ output_file_name.value
    else:
        outfile_str += '/'+ jobid
        
    return command + ' --outfile '+ outfile_str

def fetch_result(jobid):
    command = clustalo_cmd + ' --polljob --jobid '+ jobid
    command = append_outfile(command, jobid)
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print (out.decode('UTF-8'))


        
submit.on_click(submit_job)
mandatory_options = widgets.VBox([mandatory_label, email_input, sequence_type, seq_file_input, submit])
optional_options = widgets.VBox([optional_label, output_file_name,output_dir])
center_container = widgets.HBox([mandatory_options, optional_options])
mandatory_options.layout = fixed_width_layout
optional_options.layout = fixed_width_layout
app_layout = widgets.AppLayout(
    header= app_label,
    left=None,
    center = center_container,
    right= None,
    footer = None
)

display(app_layout)
display(output)