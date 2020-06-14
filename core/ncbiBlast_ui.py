import core._ui_base as gui
__name__ = 'ncbiBlast_ui' 
import xml.etree.ElementTree as ET

# 'Global' variables used later
gui.service_cmd ="python3 ../embl_client/ncbiblast.py"
blast_hints = { 'blastp': 'Mathces a protein query to a protein database.',
                'blastn': 'Matches a nucleotide query to a nucleotide query',
                'blastx':  'Compares a DNA query to a protein database, by translating the query sequence in the 6 possible frames,\n' 
                           +'and comparing each against the database (3 reading frames from each strand of the DNA) searching.',
                'tblastn': 'Compares a protein query to a DNA database, in the 6 possible frames of the database.',
                'tblastx': 'Compares the protein encoded in a DNA query to the protein encoded in a DNA database,\n'
                           +'in the 6*6 possible frames of both query and database sequences (Note that all the combinations of frames may have different scores).' }
database_options = []
database_hints = {}
_file_path = gui.os.path.dirname(__file__)
databases_xml = ET.parse(_file_path+'/../core/ncbiBlast_databases.xml')
values = databases_xml.getroot().find('values');
for db in values:
    database_options.append((db.find('value').text, db.find('value').text))
    database_hints[db.find('value').text]=db.find('label').text 
    
#Defining UI elements / widgets
gui.app_label.value = 'EMBL-Tools NCBI BLAST+ webservice'

# Widgets for mandatory information, starting with predefined label and email input
    
#add more widgets as you need below this line
BLAST_program = gui.widgets.Dropdown(
    options = [('blastp','blastp'), ('blastn', 'blastn'),
               ('blastx', 'blastx'),('tblastx', 'tblastx'),
               ('tblastn', 'tblastn')],
    value='blastp',
    description='BLAST program:',
    style = gui.style
)

BLAST_program_hint = gui.widgets.HTML(value= '<style>p{word-wrap: break-word}</style> <p>BLAST program description: '+blast_hints[BLAST_program.value]+' </p>')

sequence_type = gui.widgets.Dropdown(
    options = [('DNA','dna'), ('RNA', 'rna'),('Protein', 'protein')],
    value='dna',
    description='Sequence type:',
    style = gui.style
)

database_dropdown= gui.widgets.Dropdown(
    options = database_options,
    value = database_options[0][1],
    description='Database to use:',
    style = gui.style
)

database_hint = gui.widgets.HTML(value= '<style>p{word-wrap: break-word}</style> <p>Database description: '+database_hints[database_dropdown.value]+' </p>')

def run_checks():
    if not gui.check_email():
        return False
    if not gui.check_file():
        return False
    return True
gui.run_checks = run_checks


# modify as needed.
def prepare_command():
    command = gui.service_cmd + ' --email ' + gui.email_input.value + ' --program '+ BLAST_program.value  + ' --stype ' + sequence_type.value + ' --sequence ' + gui.seq_file_input.selected + ' --database ' + database_dropdown.value 
    command += ' --asyncjob'
    return command
gui.prepare_command = prepare_command


def blast_hint(change):
    BLAST_program_hint.value = value= '<style>p{word-wrap: break-word}</style> <p>BLAST program description: '+blast_hints[change['new']]+'</p>'
    
BLAST_program.observe(blast_hint, names='value')

def database_hint_change(change):
    database_hint.value = value= '<style>p{word-wrap: break-word}</style> <p>Database description: '+database_hints[change['new']]+'</p>'
    
database_dropdown.observe(database_hint_change, names='value')


mandatory_options =[]
for widget in gui.mandatory_options.children:
    mandatory_options.append(widget)

mandatory_options.insert(2, sequence_type)
mandatory_options.insert(2, database_hint)
mandatory_options.insert(2, database_dropdown)
mandatory_options.insert(2, BLAST_program_hint)
mandatory_options.insert(2, BLAST_program)
optional_options =[]
for widget in gui.optional_options.children:
    optional_options.append(widget)

# Append or insert widgets to the optional widgets list with append() or insert()    
gui.mandatory_options.children = (mandatory_options)
gui.optional_options.children = (optional_options)
display(gui.app_layout)
display(gui.output)
