import sys
from jinja2 import Template
import jinja2
from models.data import RouteTable


def load_template(template_file):
    """Loads Jinja2 template from file"""
    try:
        print(f"Loading jinja template { template_file }")
        with open(template_file) as t:
            template = Template(t.read())
    except IOError as ex:
        print(f"Template file { template_file} could not be opened!")
        print(f"I/O error { ex.errno } '{ ex.strerror }'")
        sys.exit(1)
    return template


def generate_config(template: jinja2, udrs: list, tf_file: str):
    """Generates config file"""

    print(f"Generating terraform file!")
    try:
        with open(tf_file, "w") as f:
            f.write(template.render(data=udrs))
    except IOError as ex:
        print(f"Could not write {tf_file}")
        print(f"I/O error { ex.errno } '{ ex.strerror }'")
        sys.exit(3)
