import subprocess
import re

# This class exposes the powercfg command line tool to python scripts using subprocess.
# Allows viewing of contents of powercfg profiles, as well as changing values and
# adding new profiles.


# A reference for powercfg usage is https://technet.microsoft.com/en-us/library/Cc748940(v=WS.10).aspx

    #**************************************************************************
    # BASIC FUNCTIONS OF POWERCFG                                             *
    #**************************************************************************

    def list():
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

    # def process_text(output, result, index, numReturns):
    #     # Check if GUID is in line, if so, start new property
    #     if(re.match('[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}', result[0])):
    #         tag = re.findall(": ", result)
    #         index++
    #         while(index < len(output):
    #             result[tag]

    #         result[tag] = process_text(output, result[tag], index, numReturns + 1)

    def query(scheme_guid, sub_guid = ""):
        "Returns a list of all power profile text for specific scheme"
        output = subprocess.check_output(["powercfg", "-query", scheme_guid, sug_guid])
        # Split by lines
        output = output.splitlines()
        # Remove blanks lines
        filteredOutput = filter(lambda x: not re.match(r'^\s*$', x), output)
        return filteredOutput
        #result = {}
        #result = process_text(result)



    def change_setting_value(setting, value):
        "Changes a setting of the powercfg, setting, to the new value, value. Returns output if any"
        return subprocess.check_output(["powercfg", "-change", setting, str(value)])

    def import_file(path, GUID):
        "Imports a power scheme file from the given path and with GUID"
        return subprocess.check_output(["powercfg", "-import", "filename", GUID])

    def export_file(path, GUID):
        "Exports a power scheme of the given GUID to path"
        return subprocess.check_output(["powercfg", "-export", "filename", GUID])

    def get_aliases():
        "Returns a list of all aliases"
        return subprocess.check_output(["powercfg", "-aliases"]).splitlines()

    def delete_scheme(GUID):
        "Deletes power scheme associated with GUID"
        return subprocess.check_output(["powercfg", "-d", GUID])

    def duplicatescheme(GUID, destinationGUID):
        "Creates a copy of scheme, GUID, with new GUID, destinationGUID"
        return subprocess.check_output(["powercfg", "-duplicatescheme", GUID, destinationGUID])

    def set_active(GUID):
        "Sets GUID to be the active power scheme"
        return subprocess.check_output(["powercfg", "-setactive", GUID)

    def get_active():
        "Returns the active GUID"
        return subprocess.check_output(["powercfg", "-getactivescheme"])

    def change_name(GUID, name, description = ""):
        "Changes name and description of scheme with GUID passed in"
        return subprocess.check_output(["powercfg", "-changename", GUID, name, description])

    #**************************************************************************
    # FUNCTIONS OF Win32_Battery                                              *
    #**************************************************************************

    def get estimated_charge_remaining():
        "Returns a number representing the current % of charge. If the laptop is charging will return 111"
        return subprocess.check_output(["WMIC", "PATH", "Win32_Battery", "Get EstimatedChargeRemaining"])

    def get estimated_run_time():
        "Returns a number representing the number of minutes of battery life remaining."
        return subprocess.check_output(["WMIC", "PATH", "Win32_Battery", "Get EstimatedRunTime"])

    #**************************************************************************
    # ADDITIONAL FUNCTIONS ADDED and helpers                                  *
    #**************************************************************************

    def set_active_by_name(name):
        "Sets active power scheme by name"
        GUID = .list()[name]
        return .set_active(GUID)
