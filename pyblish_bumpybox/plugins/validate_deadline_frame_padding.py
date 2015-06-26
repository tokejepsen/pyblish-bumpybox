import pyblish.api

@pyblish.api.log
class ValidateDeadlineFramePadding(pyblish.api.Validator):
    """ Validates the existence of four digit frame padding
    ('%04d or ####') in output.
    """

    families = ['deadline.render']
    hosts = ['*']
    version = (0, 1, 0)
    label = 'Frame Padding'
    optional = True

    def process(self, instance):

        # skipping the call up project
        ftrack_data = instance.context.data('ftrackData')
        if ftrack_data['Project']['code'] == 'the_call_up':
            return

        if '-' in instance.data('deadlineFrames'):
            path = instance.data('deadlineJobData')['OutputFilename0']
            msg = "Couldn't find any frame padding string ('%04d or ####')"
            msg += " in output on %s" % instance
            assert '####' in path or '%04d' in path, msg