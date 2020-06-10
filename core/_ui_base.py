__name__ = '_ui_base' 
import ipywidgets as widgets
from IPython.display import display
import subprocess, re, os, json
from time import sleep
from ipyfilechooser import FileChooser

service_cmd =""
style = {'description_width': 'initial'}
default_widget_layout = {'width':'90%'}
fixed_width_layout = widgets.Layout(width='50%', min_width='50%',max_width='50%')

# Checking if settings file exists and reading contents for default values to use.
settings = None
initLog = ''
if os.path.exists('/home/biodatahub/private/.embl_tools/settings.json'):
    with open('/home/biodatahub/private/.embl_tools/settings.json', 'r') as settingsFile:
        settingsData = settingsFile.read()
        settingsFile.close()
        settings = json.loads(settingsData)
    initLog += "Settings loaded.\n"
    for setting in settings:
        initLog += setting +': '+settings[setting]+'\n'
    if not os.path.exists(settings['outdir']):
        initLog += 'Default output directory does not exists. Attempting to create it.\n'
        try:
            os.makedirs(settings['outdir'])
            initLog += settings['outdir'] + ' is created.\n'
        except Exception as exception:
            print (type(exception), exception)
else:
    initLog += 'No settings file found.\n'
    initLog += os.path.dirname(__file__)+'../settings.json'


#Defining UI elements / widgets
app_label = widgets.Label(value='') # TODO replace with real application label text

# Widgets for mandatory information, starting with predefined label and email input
mandatory_label = widgets.Label(value='Mandatory options')
email_input = widgets.Text(value= '' if settings== None else settings['email'], placeholder='email address (mandatory)', description='Email (mandatory):',style = style, layout = default_widget_layout)
seq_file_input = FileChooser('./', title = 'Sequence file',style = style, disabled = False)
seq_file_input.use_dir_icons = True

# predefined submit and output
submit = widgets.Button(description='Submit',disabled=False, button_style='', tooltip='Submit job',style = style, icon='check')

clearOutput_button = widgets.Button(description='Clear output',disabled=False, button_style='', tooltip='Clear output',style = style)

output = widgets.Output(layout={'border': '1px solid black'})


# Widgets for optional options, add widgets as you need
optional_label = widgets.Label(value='Extra options')
output_file_name = widgets.Text(description = 'Save result as: ',style = style, disabled = False, layout=default_widget_layout)
output_dir = FileChooser( '.' if settings == None else settings['outdir'] , title = 'Save output to',style = style, disabled = False)
output_dir.default_path = '.'if settings == None else settings['outdir'] 
with output:
    print(initLog)

# Mostly generic logic

#Callback for the submitbutton, TODO modify as needed
@output.capture()
def submit_job(button):
    if not run_checks():
        return
    # add more checks here for early returns.
    
    command = prepare_command()
    print('Executing: ', command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    jobid = out.decode('UTF-8').split('\n')[0]
    print('Jobid: '+jobid)
    proc = subprocess.Popen([service_cmd + ' --status --jobid '+ jobid], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    status = out.decode('UTF-8').split('\n')[1]
        
    while status == 'RUNNING':
        sleep(5)
        proc = subprocess.Popen([service_cmd + ' --status --jobid '+ jobid], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        status = out.decode('UTF-8').split('\n')[1]
        print (status)
    
    fetch_result(jobid)

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

@output.capture()
def check_file():
    file_path = seq_file_input.selected
    if file_path and os.path.isfile(file_path) and os.access(file_path, os.R_OK):
        return True
    else:
        print("Either the input file is missing or not readable")
        return False
def clear_output(button):
    output.clear_output()
    

# Should be overwritten by module.
def prepare_command():
    return command

# Util method to append correct outfile param
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
    command = service_cmd + ' --polljob --jobid '+ jobid
    command = append_outfile(command, jobid)
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print (out.decode('UTF-8'))

# Module template file overwrites this thus the final module can extend the number of checks applied.
def run_checks():
    return True

submit.on_click(submit_job)
clearOutput_button.on_click(clear_output)
                             
# Define layout                             
mandatory_options = widgets.VBox([mandatory_label, email_input, seq_file_input, submit, clearOutput_button])
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

