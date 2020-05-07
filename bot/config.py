from configparser import ConfigParser


DEFAULTS = {
    'GENERAL': {
        'token': ''
    }
}
FILENAME = 'config.ini'


config = ConfigParser()
config.read_dict(DEFAULTS)

config.read(FILENAME)

with open(FILENAME, 'w') as f:
    config.write(f)


# For easier importing
conf = config['GENERAL']


# Validation
try:
    assert conf['token'], 'token must be a string'

except AssertionError as ex:
    print(ex)
    input('Invalid config! Press enter to exit...')
    raise