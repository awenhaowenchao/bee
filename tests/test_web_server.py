from bee import bapp
from bee import bapp_start_up


@bapp.route('/hello', methods=['GET', 'POST'])
def hello():
    s = '<h1>Hello world</h1>'
    return s

bapp_start_up()