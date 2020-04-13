__name__ = 'ncbiBlast_ui' 
import ipywidgets as widgets
from IPython.display import display
import subprocess
from time import sleep
import re
import os
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


# Widgets  for optional options, add widgets as you need
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

def fetch_result(jobid):
    command = service_cmd + ' --polljob --jobid '+ jobid
    command = append_outfile(command)
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
optional_options = widgets.VBox([optional_label])
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