from configparser import ConfigParser

config = ConfigParser()
config.add_section('dummy')
try:
    config.read('application.ini')
except:
    pass


EXAMPLE_WORD = config.get('app', 'example_word', fallback='Not Found')
