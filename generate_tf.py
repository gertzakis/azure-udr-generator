"""Generate tf configuration file based on Jinja2 template."""
import sys

import jinja2
from jinja2 import Template


def load_template(template_file):
    """Load Jinja2 template from file."""
    try:
        print(f"Loading jinja template { template_file }")
        with open(template_file, encoding="utf-8") as t_file:
            template = Template(t_file.read())
    except OSError as ex:
        print(f"Template file { template_file} could not be opened!")
        print(f"I/O error { ex.errno } '{ ex.strerror }'")
        sys.exit(1)
    return template


def generate_config(template: jinja2, udrs: list, tf_file: str):
    """Generate config file."""
    print("Generating terraform file!")
    try:
        with open(tf_file, "w", encoding="utf-8") as conf_file:
            conf_file.write(template.render(data=udrs))
    except OSError as ex:
        print(f"Could not write {tf_file}")
        print(f"I/O error { ex.errno } '{ ex.strerror }'")
        sys.exit(3)
