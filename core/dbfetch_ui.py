import core._ui_base as gui
__name__ = '_module_template'
gui.service_cmd = 'python3 ../embl_client/dbfetch.py ' # TODO replace service.py with real embl client python file name. Path is relative to the ui notebook, not this file.
gui.app_label.value= 'EMBL-Tools DBFetch - Retrieve entries from EMBOSS databases' # TODO replace with real application label text

db_format_style_mapping={
    'chembl':{'default':['default','html','raw'],'fasta':['default','html','raw']},
    'edam':{'default':['default','html','raw'],'obo':['default','html','raw']},
    'ena_coding':{'default':['default','html','raw'],'annot':['default','html','raw'],'embl':['default','html','raw'],
                  'emblxml-1.1':['default','raw'], 'emblxml-1.2':['default','raw'],'entrysize':['default','html','raw'],
                  'fasta':['default','html','raw'],'seqxml':['default','raw']},
    'ena_geospatial':{'default':['default','html','raw'],'annot':['default','html','raw'],
                      'embl':['default','html','raw'],'emblxml-1.2':['default','raw'],
                      'entrysize':['default','html','raw'],'fasta':['default','html','raw'],'seqxml':['default','raw']},
    'ena_noncoding':{'default':['default','html','raw'],'annot':['default','html','raw'],
                     'embl':['default','html','raw'],'emblxml-1.2':['default','raw'],
                     'entrysize':['default','html','raw'],'fasta':['default','html','raw'],'seqxml':['default','raw']},
    'ena_sequence':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'emblxml-1.1':['default','raw'],'emblxml-1.2':['default','raw'],
                    'entrysize':['default','html','raw'],'fasta':['default','html','raw'],'insdxml':['default','raw'],
                    'seqxml':['default','raw']},
    'ena_sequence_con':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'emblxml-1.1':['default','raw'],'emblxml-1.2':['default','raw'],
                    'entrysize':['default','html','raw'],'fasta':['default','html','raw'],'insdxml':['default','raw'],
                    'seqxml':['default','raw']},
    'ena_sequence_conexp':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'emblxml-1.1':['default','raw'],'emblxml-1.2':['default','raw'],
                    'entrysize':['default','html','raw'],'fasta':['default','html','raw'],'insdxml':['default','raw'],
                    'seqxml':['default','raw']},
    'ensemblgene':{'default':['default','raw'],'csv':['default','raw'],'embl':['default','raw'],'fasta':['default','raw'],
                  'genbank':['default','raw'],'gff2':['default','raw'],'gff3':['default','raw'],'tab':['default','raw']},
    'ensemblgenomesgene':{'default':['default','raw'],'csv':['default','raw'],'embl':['default','raw'],'fasta':['default','raw'],
                  'genbank':['default','raw'],'gff2':['default','raw'],'gff3':['default','raw'],'tab':['default','raw']},
    'ensemblgenomestranscript':{'default':['default','raw'],'fasta':['default','raw']},
    'ensembltranscript':{'default':['default','raw'],'fasta':['default','raw']},
    'epo_prt':{'default':['default','html','raw'],'annot':['default','html','raw'],'embl':['default','html','raw'],
              'entrysize':['default','html','raw'],'fasta':['default','html','raw'],'seqxml':['default','raw']},
    'hgnc':{'default':['default','html','raw'],'tab':['default','html','raw']},
    'imgthlacds':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
                    'seqxml':['default','raw']},
    'imgthlagen':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
                    'seqxml':['default','raw']},
    'imgthlapro':{'default':['default','html','raw'],'fasta':['default','html','raw']},
    'imgtligm':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
                    'seqxml':['default','raw']},
    'interpro':{'default':['default','html','raw'],'interpro':['default','html','raw'],'interproxml':['default','raw'],
               'tab':['default','html','raw']},
    'ipdkircds':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
                    'seqxml':['default','raw']},
    'ipdkirgen':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
                    'seqxml':['default','raw']},
    'ipdkirpro':{'default':['default','html','raw'],'fasta':['default','html','raw']},
    'ipdmhccds':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
                    'seqxml':['default','raw']},
    'ipdmhcgen':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
                    'seqxml':['default','raw']},
    'ipdmhcpro':{'default':['default','html','raw'],'fasta':['default','html','raw']},
    'iprmc':{'default':['default','html','raw'],'gff2':['default','html','raw'],'iprmc':['default','html','raw'],
           'iprmctab':['default','html','raw'],'iprmcxml':['default','raw']},
    'iprmcuniparc':{'default':['default','html','raw'],'gff2':['default','html','raw'],'iprmc':['default','html','raw'],
           'iprmctab':['default','html','raw'],'iprmcxml':['default','raw']},
    'jpo_prt':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
                    'seqxml':['default','raw']},
    'kipo_prt':{'default':['default','html','raw'],'annot':['default','html','raw'],
                    'embl':['default','html','raw'],'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
                    'seqxml':['default','raw']},
    'medline':{'default':['default','html','raw'],'medlinefull':['default','html','raw'],'medlineref':['default','html','raw'],
               'bibtex':['default','raw'],'endnote':['default','raw'],'isi':['default','raw'],'modsxml':['default','raw'],
               'pubmedxml':['default','raw'],'ris':['default','raw'],'wordbibxml':['default','raw']},
    'mp':{'default':['default','html','raw'],'fasta':['default','html','raw']},
    'mpep':{'default':['default','html','raw'],'fasta':['default','html','raw']},
    'mpro':{'default':['default','html','raw'],'fasta':['default','html','raw']},
    'nrnl1':{ 'default':['default','html','raw'],'annot':['default','html','raw'],
            'entrysize':['default','html','raw'], 'nrnl1':['default','html','raw'],
            'seqxml':['default','raw'], 'fasta':['default','html','raw']},
    'nrnl2':{ 'default':['default','html','raw'],'annot':['default','html','raw'],
            'entrysize':['default','html','raw'], 'nrnl2':['default','html','raw'],
            'seqxml':['default','raw'], 'fasta':['default','html','raw']},
    'nrpl1':{ 'default':['default','html','raw'],'annot':['default','html','raw'],
            'entrysize':['default','html','raw'], 'nrnl2':['default','html','raw'],
            'seqxml':['default','raw'], 'fasta':['default','html','raw']},
    'nrpl2':{ 'default':['default','html','raw'],'annot':['default','html','raw'],
            'entrysize':['default','html','raw'], 'nrnl2':['default','html','raw'],
            'seqxml':['default','raw'], 'fasta':['default','html','raw']},
    'patent_equivalents':{'default':['default','html','raw'], 'patent_equivalents':['default','html','raw']},
    'pdb':{'default':['default','html','raw'],'fasta':['default','raw'],
          'annot':['default','html','raw'],'mmcif':['default','raw'],
          'pdb':['default','html','raw'],'pdbml':['default','raw']},
    'refseqn':{'default':['default','html','raw'],'annot':['default','html','raw'],
              'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
              'insdxml':['default','raw'],'refseqn':['default','html','raw'],
              'seqxml':['default','raw'],'tinyseq':['default','raw']},
    'refseqp':{'default':['default','html','raw'],'annot':['default','html','raw'],
              'entrysize':['default','html','raw'],'fasta':['default','html','raw'],
              'insdxml':['default','raw'],'refseqp':['default','html','raw'],
              'seqxml':['default','raw'],'tinyseq':['default','raw']},
    'taxonomy':{'default':['default','html','raw'], 'taxonomy':['default','html','raw'],
               'enataxonomyxml':['default','raw'],
                'uniprottaxonomyrdfxml':['default','raw']},
    'uniparc':{'default':['default','raw'], 'fasta':['default','raw'],
              'seqxml':['default','raw'],'uniparc':['default','raw'],
              'uniprotrdfxml':['default','raw']},
    'uniprotkb':{'default':['default','html','raw'],'fasta':['default','html','raw'],
                'annot':['default','html','raw'], 'entrysize':['default','html','raw'],
                'gff3':['default','html','raw'], 'seqxml':['default','raw'],
                'uniprot':['default','html','raw'], 'uniprotrdfxml':['default','raw'],
                'uniprotxml':['default','raw']},
    'uniref100':{'default':['default','raw'],'fasta':['default','raw'],'seqxml':['default','raw'],'uniprotrdfxml':['default','raw'],'uniref100':['default','raw']},
    'uniref50':{'default':['default','raw'],'fasta':['default','raw'],'seqxml':['default','raw'],'uniprotrdfxml':['default','raw'],'uniref50':['default','raw']},
    'uniref90':{'default':['default','raw'],'fasta':['default','raw'],'seqxml':['default','raw'],'uniprotrdfxml':['default','raw'],'uniref100':['default','raw']},
    'unisave':{'default':['default','raw'],'annot':['default','raw'],'entrysize':['default','html','raw'],'fasta':['default','raw'],'uniprot':['default','raw']},
    'uspto_prt':{'default':['default','html','raw'],'annot':['default','html','raw'],'embl':['default','html','raw'],'entrysize':['default','html','raw'],'fasta':
                 ['default','html','raw'],'seqxml':['default','html','raw']}
    
}
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
    return True
gui.run_checks = run_checks

# Modify this method as needed to prepare the command to be executed
def prepare_command():
    command = gui.service_cmd # add more options as needed for the base command    
    command += f'fetchData {db_dropdown.value}:{id_text.value} {format_type_dropdown.value} {style_dropdown.value}'
    return command
gui.prepare_command = prepare_command

@gui.output.capture()
def local_submit_job(button):
    if not run_checks():
        return
    command = prepare_command()
    print('Executing: ', command)
    proc = gui.subprocess.Popen(command, stdout=gui.subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    for line in out.decode('UTF-8').split('\n'):
        print(line)


local_submit = gui.widgets.Button(description='Fetch',disabled=False, button_style='', tooltip='Fetch',style = gui.style, icon='check')
local_submit.on_click(local_submit_job)

db_dropdown =  gui.widgets.Dropdown(
    options = list(db_format_style_mapping),
    value = list(db_format_style_mapping)[0],
    description='Database',
    style = gui.style
)
id_text = gui.widgets.Text(value= '', placeholder='item id (mandatory)', description='Item id (mandatory):',style = gui.style )

mandatory_options =[]
for widget in gui.mandatory_options.children:
    if not isinstance(widget, gui.widgets.Button):
        mandatory_options.append(widget)
mandatory_options.append(local_submit)
mandatory_options.append(gui.clearOutput_button)
# Use the code below to insert widget just after email field.
mandatory_options.insert(2, id_text)
mandatory_options.insert(2, db_dropdown)


format_type_dropdown = gui.widgets.Dropdown(
    options =list(db_format_style_mapping[db_dropdown.value]),
    value= list(db_format_style_mapping[db_dropdown.value])[0],
    description='Format',
    style = gui.style
)

style_dropdown =  gui.widgets.Dropdown(
    options = db_format_style_mapping[db_dropdown.value][format_type_dropdown.value],
    value= db_format_style_mapping[db_dropdown.value][format_type_dropdown.value][-1],
    description='Style',
    style = gui.style
)

def format_update(change):
    format_type_dropdown.options = list(db_format_style_mapping[change["new"]])
    format_type_dropdown.value = list(db_format_style_mapping[change["new"]])[0]
    
db_dropdown.observe(format_update,names='value')

def style_update(change):
    style_dropdown.options = db_format_style_mapping[db_dropdown.value][change["new"]]
    style_dropdown.value = list(db_format_style_mapping[db_dropdown.value][change["new"]])[-1]

format_type_dropdown.observe(style_update,names='value')

optional_options =[]
for widget in gui.optional_options.children:
    optional_options.append(widget)
optional_options.append(format_type_dropdown)
optional_options.append(style_dropdown)

# Append or insert widgets to the optional widgets list with append() or insert()    
gui.mandatory_options.children = (mandatory_options)
gui.optional_options.children = (optional_options)
display(gui.app_layout)
display(gui.output)