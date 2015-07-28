import subprocess
import re

# This class exposes the powercfg command line tool to python scripts using subprocess.
# Allows viewing of contents of powercfg profiles, as well as changing values and
# adding new profiles. 


# A reference for powercfg usage is https://technet.microsoft.com/en-us/library/Cc748940(v=WS.10).aspx

class LaptopControl:

    def __init__(self):

    #**************************************************************************
    # BASIC FUNCTIONS OF POWERCFG                                             *
    #**************************************************************************

    def list(self):
        "Returns a dict containing all powercfg setting profiles"
        output = subprocess.check_output(["powercfg", "-list"])
        output = output.splitlines()
        # result is object to be returned containing all of the name GUID pairs in output
        result = {}

        for line in output:
            # Select name and GUID from each line and place them in the result
            # EG 1d77c431-8167-48c8-aca3-0d1260bfdf2b
            GUID = re.findall('[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}', line)[0]
            # EG  (Extended Battery Life (Max run-time).)
            name = re.findall(' \(.+', line)[0]
            result[name] = GUID

        return result

    def query(self, scheme_guid, sub_guid = ""):
        "Returns a list of all power profile text for specific scheme"
        output = subprocess.check_output(["powercfg", "-query", scheme_guid, sug_guid])
        # Split by lines
        output = output.splitlines()
        # Remove blanks lines
        filteredOutput = filter(lambda x: not re.match(r'^\s*$', x), output)
        return filteredOutput

    def change_setting_value(self, setting, value):
        "Changes a setting of the powercfg, setting, to the new value, value. Returns output if any"
        return subprocess.check_output(["powercfg", "-change", setting, str(value)])

    def import_file(self, path, GUID):
        "Imports a power scheme file from the given path and with GUID"
        return subprocess.check_output(["powercfg", "-import", "filename", GUID])

    def export_file(self, path, GUID):
        "Exports a power scheme of the given GUID to path"
        return subprocess.check_output(["powercfg", "-export", "filename", GUID])

    def get_aliases(self):
        "Returns a list of all aliases"
        return subprocess.check_output(["powercfg", "-aliases"]).splitlines()

    def delete_scheme(self, GUID):
        "Deletes power scheme associated with GUID"
        return subprocess.check_output(["powercfg", "-d", GUID])

    def duplicatescheme(self, GUID, destinationGUID):
        "Creates a copy of scheme, GUID, with new GUID, destinationGUID"
        return subprocess.check_output(["powercfg", "-duplicatescheme", GUID, destinationGUID])

    def set_active(self, GUID):
        "Sets GUID to be the active power scheme"
        return subprocess.check_output(["powercfg", "-setactive", GUID)

    def get_active(self):
        "Returns the active GUID"
        return subprocess.check_output(["powercfg", "-getactivescheme"])

    def change_name(self, GUID, name, description = ""):
        "Changes name and description of scheme with GUID passed in"
        return subprocess.check_output(["powercfg", "-changename", GUID, name, description])

    #**************************************************************************
    # ADDITIONAL FUNCTIONS ADDED                                              *
    #**************************************************************************

    def set_active_by_name(self, name):
        "Sets active power scheme by name"
        GUID = self.list()[name]
        return self.set_active(GUID)
