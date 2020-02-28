from configparser import ConfigParser

# manage configuration file
def config_update(file, section, option, value):
    config = ConfigParser()
    config.read(file)
    cfgfile = open(file, 'w')
    if config.has_section(section) == True:
        config.set(section, option, value)
    else:
        config.add_section(section)
        config.set(section, option, value)
    config.write(cfgfile)
    cfgfile.close()

def config_read(file, section, option):
    config = ConfigParser()
    config.read(file)
    if config.has_option(section, option) == True:
        value = config.get(section, option)
    return value