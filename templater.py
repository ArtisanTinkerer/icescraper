from mako.template import Template


def populate_template(dict_variables: dict, template_file: str):
    """Render the template with the variables"""

    results_template: Template = Template(filename=template_file)

    filled_template: Template = results_template.render(**dict_variables)

    # Create a file:
    file_name: str = "populated.html"
    file = open(file_name, "w+")
    file.write(filled_template)
    file.close()
