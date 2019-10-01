from views import *
from jinja2 import Environment

#add method to JINJA2
app.jinja_env.add_extension('jinja2.ext.do')

if __name__ == '__main__':
    app.run(port=5555,debug=True)
