import pymel
import pyblish.api
import pyblish_maya


class BumpyboxMayaExtractMayaFormats(pyblish.api.InstancePlugin):
    """ Extracts Maya ascii and binary files. """

    order = pyblish.api.ExtractorOrder
    families = ["mayaAscii", "mayaBinary"]
    optional = True
    label = "Maya Formats"
    hosts = ["maya"]

    def process(self, instance):

        # Export to file.
        path = list(instance.data["collection"])[0]
        with pyblish_maya.maintained_selection():

            pymel.core.select(instance[0].members())

            export_type = set(self.families) & set(instance.data["families"])
            pymel.core.system.exportSelected(
                path, force=True, type=list(export_type)[0],
                preserveReferences=True
            )