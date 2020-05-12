import core._ui_base as gui
__name__ = 'clustalO_ui'

gui.service_cmd = 'python3 ../embl_client/clustalo.py' 
gui.app_label.value = 'EMBL-ToolsClustalO webservice'

# Define more widgets and add them to guimandatory_options  or gui.optional_options
# Add @gui.output.capture() to methods you want to have their output printed.

# Widgets for mandatory information
sequence_type = gui.widgets.Dropdown(
    options = [('DNA','dna'), ('RNA', 'rna'),('Protein', 'protein')],
    value='dna',
    description='Sequence type:',
    style = gui.style
)

def run_checks():
    if not gui.check_email():
        return False
    if not gui.check_file():
        return False
    return True
gui.run_checks = run_checks


def prepare_command():
    command = gui.service_cmd + ' --email '+ gui.email_input.value + ' --stype ' +sequence_type.value + ' --sequence ' + gui.seq_file_input.selected  
    command += ' --asyncjob'
    return command
gui.prepare_command = prepare_command

mandatory_options =[]
for widget in gui.mandatory_options.children:
    mandatory_options.append(widget)
mandatory_options.insert(2, sequence_type)
gui.mandatory_options.children = (mandatory_options)

display(gui.app_layout)
display(gui.output)