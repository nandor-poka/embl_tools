__name__ = 'ncbiBlast_ui' 
import ipywidgets as widgets
from IPython.display import display
import subprocess, re, os, json
from time import sleep
from ipyfilechooser import FileChooser
import xml.etree.ElementTree as ET

# 'Global' variables used later
fixed_width_layout = widgets.Layout(width='50%', min_width='50%',max_width='50%')
service_cmd ="python3 embl_client/ncbiblast.py"
style = {'description_width': 'initial'}
blast_hints = { 'blastp': 'Mathces a protein query to a protein database.',
                'blastn': 'Matches a nucleotide query to a nucleotide query',
                'blastx':  'Compares a DNA query to a protein database, by translating the query sequence in the 6 possible frames,\n' 
                           +'and comparing each against the database (3 reading frames from each strand of the DNA) searching.',
                'tblastn': 'Compares a protein query to a DNA database, in the 6 possible frames of the database.',
                'tblastx': 'Compares the protein encoded in a DNA query to the protein encoded in a DNA database,\n'
                           +'in the 6*6 possible frames of both query and database sequences (Note that all the combinations of frames may have different scores).' }
database_options = []
database_hints = {}

databases_xml = ET.parse('core/ncbiBlast_databases.xml')
values = databases_xml.getroot().find('values');
for db in values:
    database_options.append((db.find('value').text, db.find('value').text))
    database_hints[db.find('value').text]=db.find('label').text

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
    
    
#Defining UI elements / widgets
app_label = widgets.Label(value='EMBL-Tools NCBI BLAST+ webservice') # TODO replace with real application label text

# Widgets for mandatory information, starting with predefined label and email input
mandatory_label = widgets.Label(value='Mandatory options')
email_input = widgets.Text(value='', placeholder='email address (mandatory)', description='Email (mandatory):',style = style )

    
#add more widgets as you need below this line
BLAST_program = widgets.Dropdown(
    options = [('blastp','blastp'), ('blastn', 'blastn'),
               ('blastx', 'blastx'),('tblastx', 'tblastx'),
               ('tblastn', 'tblastn')],
    value='blastp',
    description='BLAST program:',
    style = style
)

BLAST_program_hint = widgets.HTML(value= '<style>p{word-wrap: break-word}</style> <p>BLAST program description: '+blast_hints[BLAST_program.value]+' </p>')

sequence_type = widgets.Dropdown(
    options = [('DNA','dna'), ('RNA', 'rna'),('Protein', 'protein')],
    value='dna',
    description='Sequence type:',
    style = style
)

database_dropdown= widgets.Dropdown(
    options = database_options,
    value = database_options[0][1],
    description='Database to use:',
    style = style
)

database_hint = widgets.HTML(value= '<style>p{word-wrap: break-word}</style> <p>Database description: '+database_hints[database_dropdown.value]+' </p>')

seq_file_input = FileChooser('./', title = 'Sequence file',style = style, disabled = False)
seq_file_input.use_dir_icons = True

# predefined submit and output
submit = widgets.Button(description='Submit',disabled=False, button_style='', tooltip='Submit job',style = style, icon='check')
output = widgets.Output(layout={'border': '1px solid black'})
with output:
    print(initLog)

# Widgets  for optional options, add widgets as you need
optional_label = widgets.Label(value='Extra options')
output_file_name = widgets.Text(description = 'Save result as: ',style = style, disabled = False)
output_dir = FileChooser(settings['outdir'] if settings['outdir'] != None else '.', title = 'Save output to',style = style, disabled = False)
output_dir.default_path = settings['outdir'] if settings['outdir'] != None else '.'

# Mostly generic logic

#Callback for the submitbutton, TODO modify as needed
@output.capture()
def submit_job(b):
    if not check_email():
        return
    # add more checks here for early returns.
    if not check_file():
        return
    command = prepare_command()
    print("submitting job:" +command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    jobid = out.decode('UTF-8').split('\n')[0]
    print ('Jobid: '+jobid)
    
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

output.capture()
def check_file():
    file_path = seq_file_input.selected
    if file_path and os.path.isfile(file_path) and os.access(file_path, os.R_OK):
        return True
    else:
        print("Either the file is missing or not readable")
        return False

# modify as needed.
def prepare_command():
    command = service_cmd + ' --email ' + email_input.value + ' --program '+ BLAST_program.value  + ' --stype ' + sequence_type.value + ' --sequence ' + seq_file_input.selected + ' --database ' + database_dropdown.value # add more options as needed for the base command    
    command += ' --asyncjob'
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
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print (out.decode('UTF-8'))

submit.on_click(submit_job)

def blast_hint(change):
    BLAST_program_hint.value = value= '<style>p{word-wrap: break-word}</style> <p>BLAST program description: '+blast_hints[change['new']]+'</p>'
    
BLAST_program.observe(blast_hint, names='value')

def database_hint_change(change):
    database_hint.value = value= '<style>p{word-wrap: break-word}</style> <p>Database description: '+database_hints[change['new']]+'</p>'
    
database_dropdown.observe(database_hint_change, names='value')
# Define layout   

mandatory_options = widgets.VBox([mandatory_label, 
                                  email_input,
                                  BLAST_program,
                                  BLAST_program_hint,
                                  sequence_type,
                                  database_dropdown,
                                  database_hint,
                                  seq_file_input,
                                  submit])
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