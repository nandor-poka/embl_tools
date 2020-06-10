import core._ui_base as gui
__name__ = 'emboss_backtranambig'
import xml.etree.ElementTree as ET
gui.service_cmd = 'python3 ../embl_client/emboss_backtranambig.py' 
gui.app_label.value= 'EMBL-Tools Backtranambig - Back-translate a protein sequence to ambiguous nucleotide sequence.Back-translate a protein sequence to ambiguous nucleotide sequence.'
codon_table_options = []
_file_path = gui.os.path.dirname(__file__)
databases_xml = ET.parse(_file_path+'/../core/Backtranambig_codon_table.xml')
values = databases_xml.getroot().find('values');
for option in values:
    codon_table_options.append((option.find('label').text, option.find('value').text))

# Define more widgets and add them to gui mandatory_options or gui.optional_options
# Add @gui.output.capture() to methods you want to have their output printed.
# The submit button is the last widget in the mandatory_options, thus you should instert widgets before that.
# It is recommended to insert any new widgets after the email field.
codon_table_dropdown= gui.widgets.Dropdown(
    options = codon_table_options,
    value = codon_table_options[0][1],
    description='Cotdon table to use:',
    style = gui.style,
    layout=gui.default_widget_layout
)

sequence_input_textarea = gui.widgets.Textarea(
    value='',
    placeholder='Sequence(s) to translate. Valid formats: GCG, FASTA, PIR, NBRF, PHYLIP or UniProtKB/Swiss-Prot.',
    description='Direct input for sequence(s):',
    disabled=False,
    rows=10,
    layout=gui.default_widget_layout,
    style = gui.style
)


@gui.output.capture()
def check_sequence_input():
    if ''.__eq__(sequence_input_textarea.value):
        print('Direct sequence input is empty.')
        return False
    return True

# Append more checks as needed. Define your check functions in the file and call them here.
# The method MUST only return true if all checks pass.
# use @gui.output.capture() annotation for the check method to capture it's output.
input_file_exists=False
direct_input=False
def run_checks():
    if not gui.check_email():
        return False
    input_file_exists =  gui.check_file()
    direct_input = check_sequence_input()
    if not input_file_exists and not direct_input:
        print('Either paste sequence into direct input or select a file.')
        return False
    if input_file_exists and direct_input:
        print('File upload and direct cannot be used at the same time. Please use only one of the input methods.')
        return False
    return True
gui.run_checks = run_checks

def write_tmp_seq_file():
    with open('/tmp/temp_seq_file', mode='w') as tempfile:
        tempfile.write(sequence_input_textarea.value)
        tempfile.close()
        
# Modify this method as needed to prepare the command to be executed
def prepare_command():
    sequence = None
    if input_file_exists:
        sequence = gui.seq_file_input.selected
    else:
        write_tmp_seq_file()
        sequence = '/tmp/temp_seq_file'
    command = f'''{gui.service_cmd} --email {gui.email_input.value} --sequence {sequence} --codontable {codon_table_dropdown.value}'''# add more options as needed for the base command    
    command += ' --asyncjob'
    return command
gui.prepare_command = prepare_command

mandatory_options =[]
for widget in gui.mandatory_options.children:
    mandatory_options.append(widget)

# Use the code below to insert widget just after email field.\
mandatory_options.insert(3, sequence_input_textarea)

optional_options =[]
for widget in gui.optional_options.children:
    optional_options.append(widget)
optional_options.insert(1, codon_table_dropdown)
# Append or insert widgets to the optional widgets list with append() or insert()    
gui.mandatory_options.children = (mandatory_options)
gui.optional_options.children = (optional_options)
display(gui.app_layout)
display(gui.output)