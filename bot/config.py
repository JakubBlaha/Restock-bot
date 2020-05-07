from configparser import ConfigParser


DEFAULTS = {
    'GENERAL': {
        'token': '',
        'notification_channel_id': ''
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
    assert conf['notification_channel_id'].isnumeric(), 'notification_channel_id must be a number'

except AssertionError as ex:
    print(ex)
    input('Invalid config! Press enter to exit...')
    raise