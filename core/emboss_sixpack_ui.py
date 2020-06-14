import core._ui_base as gui
__name__ = '_module_template'
gui.service_cmd = 'python3 embl_client/service.py' # TODO replace service.py with real embl client python file name. Path is relative to the ui notebook, not this file.
gui.app_label.value= 'EMBL-Tools webservice template gui' # TODO replace with real application label text

# Define more widgets and add them to guimandatory_options  or gui.optional_options
# Add @gui.output.capture() to methods you want to have their output printed.
# The submit button is the last widget in the mandatory_options, thus you should instert widgets before that.
# It is recommended to insert any new widgets after the email field.

# Append more checks as needed. Define your check functions in the file and call them here.
# The method MUST only return true if all checks pass.
# use @gui.output.capture() annotation for the check method to capture it's output.
def run_checks():
    if not gui.check_email():
        return False
    if not gui.check_file():
        return False
    return True
gui.run_checks = run_checks

# Modify this method as needed to prepare the command to be executed
def prepare_command():
    command = gui.service_cmd + '--email '+gui.email_input.value # add more options as needed for the base command    
    command += ' --asyncjob'
    return command
gui.prepare_command = prepare_command


mandatory_options =[]
for widget in gui.mandatory_options.children:
    mandatory_options.append(widget)

# Use the code below to insert widget just after email field.
# mandatory_options.insert(2, widget_variable)

optional_options =[]
for widget in gui.optional_options.children:
    optional_options.append(widget)

# Append or insert widgets to the optional widgets list with append() or insert()    
gui.mandatory_options.children = (mandatory_options)
gui.optional_options.children = (optional_options)
display(gui.app_layout)
display(gui.output)