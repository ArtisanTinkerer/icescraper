from mako.template import Template


def populate_template(dict_variables, template_file):
    """Render the template with the variables"""

    results_template = Template(filename=template_file)

    filled_template = results_template.render(**dict_variables)

    # Create a file:
    file_name = "populated.html"
    file = open(file_name, "w+")
    file.write(filled_template)
    file.close()