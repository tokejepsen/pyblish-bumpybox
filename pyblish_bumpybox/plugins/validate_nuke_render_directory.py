import os

import pyblish.api
import ftrack
import nuke


@pyblish.api.log
class ValidateNukeRenderDirectory(pyblish.api.Validator):
    """ Validates the output path for nuke renders """

    families = ['deadline.render']
    hosts = ['nuke']
    version = (0, 1, 0)
    label = 'Render Directory'

    def get_path(self, instance):
        ftrack_data = instance.context.data('ftrackData')
        shot_name = ftrack_data['Shot']['name']
        project = ftrack.Project(id=ftrack_data['Project']['id'])
        root = project.getRoot()
        file_name = os.path.basename(instance.context.data('currentFile'))
        file_name = os.path.splitext(file_name)[0]
        task_name = ftrack_data['Task']['name'].replace(' ', '_').lower()
        version_number = instance.context.data('version')
        version_name = 'v%s' % (str(version_number).zfill(3))

        output = os.path.join(root, 'renders', 'img_sequences', shot_name,
                                task_name, version_name, str(instance))
        return output

    def process(self, instance):

        path = instance.data('deadlineJobData')['OutputFilename0']

        # on going project specific exception
        ftrack_data = instance.context.data('ftrackData')
        if ftrack_data['Project']['code'] == 'the_call_up':
            msg = "Output directory doesn't exist on: %s" % str(instance)
            assert os.path.exists(os.path.dirname(path)), msg
            return

        # get output path
        basename = os.path.basename(path)
        output = self.get_path(instance)
        self.log.info(output)
        self.log.info(os.path.dirname(path))

        # validate path
        msg = 'Output directory is incorrect on: %s' % str(instance)
        assert os.path.dirname(path) == output.replace('\\', '/'), msg

    def repair(self, instance):

        node = nuke.toNode(str(instance))
        path = node['file'].value()

        # on going project specific exception
        ftrack_data = instance.context.data('ftrackData')
        if ftrack_data['Project']['code'] == 'the_call_up':
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            return

        # repairing the path string
        basename = os.path.basename(path)
        output = self.get_path(instance)
        output = os.path.join(output, basename)
        output = output.replace('\\', '/')

        node['file'].setValue(output)

        # making directories
        if not os.path.exists(os.path.dirname(output)):
            os.makedirs(os.path.dirname(output))
