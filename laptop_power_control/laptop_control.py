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
        GUID = re.findall('[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}', line)
        # EG  (Extended Battery Life (Max run-time).)
        name = re.findall('\(([^\)]+)\)', line)
        if len(GUID) > 0 and len(name) > 0:
            result[name[0]] = {'GUID': GUID[0]}
    return result


def query(scheme_guid, sub_guid = None):
    "Returns a dict of all power profile text for specific scheme"
    if sub_guid:
        output = subprocess.check_output(["powercfg", "-query", scheme_guid, sub_guid])
    else:
        output = subprocess.check_output(["powercfg", "-query", scheme_guid])
    # Split by lines
    output = output.splitlines()
    # Remove blanks lines
    filteredOutput = filter(lambda x: not re.match(r'^\s*$', x), output)
    # Dict for result
    result = {}
    # Process text using tabs for sugroups

    process_text(filteredOutput, result, 0, 0)
    return result


def change_setting_value(setting, value):
    "Changes a setting of the powercfg, setting, to the new value, value. Returns output if any"
    return subprocess.check_output(["powercfg", "-change", setting, str(value)]).strip()


def import_file(path, GUID):
    "Imports a power scheme file from the given path and with GUID"
    return subprocess.check_output(["powercfg", "-import", "filename", GUID]).strip()


def export_file(path, GUID):
    "Exports a power scheme of the given GUID to path"
    return subprocess.check_output(["powercfg", "-export", "filename", GUID]).strip()


def get_aliases():
    "Returns a list of all aliases"
    output = subprocess.check_output(["powercfg", "-aliases"]).splitlines()
    output = filter(None, output)
    result = {}
    for line in output:
        split_line = line.split()
        result[split_line[1]] = split_line[0]
    return result


def delete_scheme(GUID):
    "Deletes power scheme associated with GUID"
    return subprocess.check_output(["powercfg", "-d", GUID]).strip()


def duplicatescheme(GUID, destinationGUID):
    "Creates a copy of scheme, GUID, with new GUID, destinationGUID"
    return subprocess.check_output(["powercfg", "-duplicatescheme", GUID, destinationGUID]).strip()


def set_active(GUID):
    "Sets GUID to be the active power scheme"
    return subprocess.check_output(["powercfg", "-setactive", GUID]).strip()


def get_active():
    "Returns the active GUID"
    output = subprocess.check_output(["powercfg", "-getactivescheme"])
    GUID = re.findall('[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}', output)[0]
    name = re.findall('\(([^\)]+)\)', output)[0]
    return {'Power Scheme GUID': GUID, 'name': name}


def change_name(GUID, name, description = ""):
    "Changes name and description of scheme with GUID passed in"
    return subprocess.check_output(["powercfg", "-changename", GUID, name, description]).strip()

#**************************************************************************
# FUNCTIONS OF Win32_Battery                                              *
#**************************************************************************


def get_estimated_charge_remaining():
    "Returns a number representing the current % of charge. If the laptop is charging will return 111"
    output = subprocess.check_output(["WMIC", "Path", "Win32_Battery", "Get", "EstimatedChargeRemaining"]).strip()
    split_line = output.split()
    result = {}
    result[split_line[0]] = split_line[1]
    return result


def get_estimated_run_time():
    "Returns a number representing the number of minutes of battery life remaining."
    output = subprocess.check_output(["WMIC", "Path", "Win32_Battery", "Get", "EstimatedRunTime"]).strip()
    split_line = output.split()
    result = {}
    result[split_line[0]] = split_line[1]
    return result

#**************************************************************************
# ADDITIONAL FUNCTIONS ADDED and helpers                                  *
#**************************************************************************


def set_active_by_name(name):
    "Sets active power scheme by name"
    GUID = list()[name]
    return set_active(GUID).strip()


def process_text(output, result, index, numSpaces):
    "Updates the result dict to contain the information stored in the strings divided according to content"
    # Returns the current index of the file, for processing
    lastTag = None
    while index < len(output):
        # Check if GUID is in line, if so, start new property
        spaces = len(output[index]) - len(output[index].strip(' '))
        # In 1 Level
        if spaces > numSpaces:
            if lastTag is not None:
                index = process_text(output, result[lastTag], index, spaces)
            else:
                index = process_text(output, result, index, spaces)
        # Out 1 Level
        elif spaces < numSpaces:
            return index
        # Same level
        elif(re.match('.*[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}.*', output[index])):
            GUID = re.findall('[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}', output[index])[0]
            colonIndex = output[index].index(':')
            tag = output[index][0:colonIndex].strip()
            name = output[index][(colonIndex + 1):].strip()
            result[name] = {'type': tag, 'GUID': GUID}
            index = index + 1
            lastTag = name
        else:
            colonIndex = output[index].index(':')
            tag = output[index][0:colonIndex].strip()
            value = output[index][(colonIndex + 1):].strip()
            result[tag] = value
            index = index + 1
    return index
