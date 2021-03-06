<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" ?>
<casaxml xmlns="http://casa.nrao.edu/schema/psetTypes.html"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://casa.nrao.edu/schema/casa.xsd file:///opt/casa/code/xmlcasa/xml/casa.xsd">

<task type="function" name="${package.lower()}_${taskname.lower()}" category="pipeline">
<shortdescription>Base ${taskname.lower()} task</shortdescription>
<description>
</description>
<input>
    <param type="stringArray" name="vis" subparam="true">
	<description>List of input visibility data</description>
	<value></value>
    </param>


    <param type="string" name="pipelinemode">
	<description>The pipeline operating mode</description>
	<value>automatic</value>
	<allowed kind="enum">
	    <value>automatic</value>
	    <value>interactive</value>
	    <value>getinputs</value>
	</allowed>
    </param>

    <param type="bool" name="dryrun" subparam="true">
	<description>Run the task (False) or display task command (True)</description>
	<value>False</value>
    </param>

    <param type="bool" name="acceptresults" subparam="true">
	<description>Add the results into the pipeline context</description>
	<value>True</value>
    </param>

    <constraints>
	<when param="pipelinemode">
	    <equals type="string" value="automatic">
	    </equals>
	    <equals type="string" value="interactive">
                <default param="vis"><value type="stringArray"></value></default>

		<default param="dryrun"><value type="bool">False</value></default>
		<default param="acceptresults"><value type="bool">True</value></default>
	    </equals>
	    <equals type="string" value="getinputs">
                <default param="vis"><value type="stringArray"></value></default>

	    </equals>
	</when>
    </constraints>

</input>

<output>
    <param type="any" name="results">
        <description>The output results object</description>
        <any type="variant"/>
        <value></value>
    </param>
</output>
<returns type="void"/>


<example>
The ${package.lower()}_${taskname.lower()} task

Keyword arguments:

---- pipeline parameter arguments which can be set in any pipeline mode

vis -- List of visisbility  data files. These may be ASDMs, tar files of ASDMs,
   MSs, or tar files of MSs, If ASDM files are specified, they will be
   converted  to MS format.
   default: []
   example: vis=['X227.ms', 'asdms.tar.gz']



pipelinemode -- The pipeline operating mode. In 'automatic' mode the pipeline
   determines the values of all context defined pipeline inputs
   automatically.  In 'interactive' mode the user can set the pipeline
   context defined parameters manually.  In 'getinputs' mode the user
   can check the settings of all pipeline parameters without running
   the task.
   default: 'automatic'.

---- pipeline context defined parameter argument which can be set only in
'interactive mode'


--- pipeline task execution modes

dryrun -- Run the commands (True) or generate the commands to be run but
   do not execute (False).
   default: True

acceptresults -- Add the results of the task to the pipeline context (True) or
   reject them (False).
   default: True

Output:

results -- If pipeline mode is 'getinputs' then None is returned. Otherwise
   the results object for the pipeline task is returned.


Examples

1. Basic ${taskname.lower()} task

   ${package.lower()}_${taskname.lower()}()


</example>
</task>
</casaxml>
