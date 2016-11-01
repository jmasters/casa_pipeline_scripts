"""
Create a new CASA pipeline task.

The purpose of this script is to make it easy to create
a generic pipeline task, save time and not miss any
essential steps.
"""

import errno
import os
import tempfile
import shutil
import re

import pipeline
from mako.template import Template

repository_path = os.environ['SCIPIPE_HEURISTICS']
area = 'hif'
task_name = 'foobar'

task_name = task_name.lower()

# -----------------------------------------------------------------------------
# define the directories for new files
# -----------------------------------------------------------------------------
task_dir = '{repo}/pipeline/{area}/tasks/{task}'.format(repo=repository_path,
                                                        area=area, task=task_name)
cli_dir = '{repo}/pipeline/{area}/cli'.format(repo=repository_path, area=area)

# -----------------------------------------------------------------------------
# create the task directory
# -----------------------------------------------------------------------------
print('1.')
print('\tCreating {f}'.format(f=task_dir))
try:
    os.mkdir(task_dir)
except OSError, ee:
    if ee.errno == 17:
        pass
    else:
        raise

# -----------------------------------------------------------------------------
# define the new files
# -----------------------------------------------------------------------------
module_file = '{tdir}/{task}.py'.format(tdir=task_dir, task=task_name)
init_file = '{tdir}/__init__.py'.format(tdir=task_dir)
cli_file = '{cdir}/task_{area}_{task}.py'.format(cdir=cli_dir, area=area, task=task_name)
cli_xml = '{cdir}/{area}_{task}.xml'.format(cdir=cli_dir, area=area, task=task_name)
weblog_mako = '{repo}/pipeline/{area}/templates/{task}.mako'.format(repo=repository_path, area=area, task=task_name)

# -----------------------------------------------------------------------------
# instantiate the templates
# -----------------------------------------------------------------------------
module_template = Template(filename='{repo}/pipeline/infrastructure/'
                                    'pipeline_task_module.mako'.format(repo=repository_path))
cli_template = Template(filename='{repo}/pipeline/infrastructure/'
                                 'pipeline_cli_module.mako'.format(repo=repository_path))
cli_xml_template = Template(filename='{repo}/pipeline/infrastructure/'
                                     'pipeline_cli_xml.mako'.format(repo=repository_path))
# web_template = Template(filename='{repo}/pipeline/infrastructure/pipeline_weblog_task.mako'.format(repo=repository_path))
init_template = Template(filename='{repo}/pipeline/infrastructure/'
                                  'pipeline_task_init.mako'.format(repo=repository_path))

# -----------------------------------------------------------------------------
# create the files
# -----------------------------------------------------------------------------

print('\tCreating {f}'.format(f=module_file))
with open(module_file, 'w+') as fd:
    fd.writelines(module_template.render(taskname=task_name))

print('\tCreating {f}'.format(f=init_file))
with open(init_file, 'w+') as fd:
    fd.writelines(init_template.render(taskname=task_name))

print('\tCreating {f}'.format(f=cli_file))
with open(cli_file, 'w+') as fd:
    fd.writelines(cli_template.render(taskname=task_name))

print('\tCreating {f}'.format(f=cli_xml))
with open(cli_xml, 'w+') as fd:
    fd.writelines(cli_xml_template.render(taskname=task_name, package=area))

# print('\tCreating {f}'.format(f=weblog_mako))
# with open(weblog_mako, 'w+') as fd:
#     fd.writelines(web_template.render(taskname=task_name))

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

print('''2.
\tCheck infrastructure/jobrequest.py to see if it lists all CASA tasks
\tneeded by your new pipeline task.  If not, add them to the
\tCASATaskGenerator class.
''')

# -----------------------------------------------------------------------------
# Add import to package __init__.py
# -----------------------------------------------------------------------------

package_init_file = "{repo}/pipeline/{area}/tasks/__init__.py".format(repo=repository_path,
                                                                       area=area)

with open(package_init_file) as fd:
    init_file_data = fd.readlines()

# look for the last "from " import line and
# add the new module import on the next line
for idx, line in enumerate(init_file_data[::-1]):
    if line.startswith('from '):
        if task_name not in line:
            init_file_data.insert(-idx, 'from .{task} import {task_class}\n'.format(task=task_name,
                                                                                    task_class=task_name.capitalize()))
            print('\tAdding "from .{task} import {task_class}" to {pfile}'.format(task=task_name,
                                                                                task_class=task_name.capitalize(),
                                                                                pfile=package_init_file))
        break

temp_init_file = tempfile.NamedTemporaryFile(delete=False)
with open(temp_init_file.name, "w+") as fd:
    fd.writelines(init_file_data)

shutil.copy(temp_init_file.name, package_init_file)
os.unlink(temp_init_file.name)

# -----------------------------------------------------------------------------
# Add task to casataskdict
# -----------------------------------------------------------------------------

casa_task_dictionary_file = "{repo}/pipeline/infrastructure/casataskdict.py".format(repo=repository_path)

with open(casa_task_dictionary_file) as fd:
    casataskdict_data = fd.readlines()

for idx, line in enumerate(casataskdict_data):
    match = re.match('(\s+{area}_tasks.)([a-zA-Z]+)([^:]+)(:)'.format(area=area), line)
    if task_name in line:
        break

    if match and match.group(2) > task_name.title():
        casataskdict_data.insert(idx, "    {area}_tasks.{task_camel:24}"
                                 ": '{area}_{task}',\n".format(area=area,
                                                               task_camel=task_name.title(),
                                                               task=task_name))
        print('\tAdding {task} to classToCASATask in {ctd_file}'.format(task=task_name,
                                                                          ctd_file=casa_task_dictionary_file))
        break

temp_taskdict_file1 = tempfile.NamedTemporaryFile(delete=False)
temp_taskdict_file2 = tempfile.NamedTemporaryFile(delete=False)
with open(temp_taskdict_file1.name, "w+") as fd:
    fd.writelines(casataskdict_data)

with open(temp_taskdict_file1.name) as fd:
    casataskdict_data = fd.readlines()

for idx, line in enumerate(casataskdict_data):
    match = re.match("(\s+'{area}_)([a-zA-Z]+)(': ')".format(area=area), line)
    if match and match.group(2) > task_name.title():
        if task_name not in line:
            casataskdict_data.insert(idx, "    '{area}_{task}': "
                                          "'{task_camel}',\n".format(area=area,
                                                                     task_camel=task_name.title(),
                                                                     task=task_name))
            print('\tAdding {task} to CasaTaskDict in {ctd_file}'.format(task=task_name,
                                                                       ctd_file=casa_task_dictionary_file))
        break

with open(temp_taskdict_file2.name, "w+") as fd:
    fd.writelines(casataskdict_data)

shutil.copy(temp_taskdict_file2.name, casa_task_dictionary_file)
os.unlink(temp_taskdict_file1.name)
os.unlink(temp_taskdict_file2.name)

# -----------------------------------------------------------------------------
# Say something about call library
# -----------------------------------------------------------------------------

print('''3.
\tConsider adding code to infrastructure/callibrary.py if needed.
''')

# -----------------------------------------------------------------------------
# Say something about file namer
# -----------------------------------------------------------------------------

print('''4.
\tConsider adding code to infrastructure/filenamer.py if needed for calibration tables.
''')

# -----------------------------------------------------------------------------
# Web log rendering
# -----------------------------------------------------------------------------

print('''5.
\tConsider adding code to infrastructure/displays/ if needed for the web log.
''')

print('''6.
\tLater you might need to add a renderer.py file to {area}/tasks/{task}/ if needed for the web log.
'''.format(area=area, task=task_name))

# -----------------------------------------------------------------------------
# mako template for weblog
# -----------------------------------------------------------------------------
mako_template = '{repo}/pipeline/infrastructure/pipeline_weblog_task.mako'.format(repo=repository_path)

print('7.')
print('\tCreating {f}'.format(f=mako_template))

temp_mako = tempfile.NamedTemporaryFile(delete=False)

with open(mako_template) as infile, open(temp_mako.name, 'w+') as outfile:
    for line in infile:
        # print(line.replace("$$mytaskname$$", task_name.capitalize()))
        outfile.write(line.replace("$$mytaskname$$", task_name.capitalize()))

shutil.copy(temp_mako.name, weblog_mako)
os.unlink(temp_mako.name)
