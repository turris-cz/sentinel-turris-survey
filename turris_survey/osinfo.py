"""This parses and provides fieds from /etc/os-release
"""


def os_info():
    """Returns dictionary with minimal info about current system.
    """
    result = {}
    with open("/etc/os-release", "r") as os_info_file:
        for line in os_info_file:
            (key, val) = line.split("=", 1)
            val = val.strip()
            # Remove quotes from beginning and end of string if any matching
            # are there
            if (len(val) > 1 and val[0] == val[-1] and
                    (val[0] == '"' or val[0] == "'")):
                val = val[1:-1]
            result[key] = val
    return result
