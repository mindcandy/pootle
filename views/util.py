import os
from os import path
import kid
from django.http import HttpResponse
import mimetypes

# settings.py is in the root of our Django application's
# directory structure, so we can use path.dirname to
# find the root directory.
from Pootle import settings
root_dir = path.dirname(settings.__file__)

kid.enable_import()

def find_template(relative_template_path):
    """Find the full path of the template whose relative path is
    'relative_template_path'."""

    for template_dir in settings.TEMPLATE_DIRS:
        full_template_path = path.join(root_dir, template_dir, relative_template_path)
        if path.exists(full_template_path):
            return full_template_path
    raise Exception('No template named %s found' % relative_template_path)

def render(relative_template_path, **template_vars):
    # Find the template at relative_template_path, get the
    # constructed kid template and pass template_vars
    # through...
    template = kid.Template(file = find_template(relative_template_path), **template_vars)
    
    # Render the template to a string and send the string
    # to HttpResponse
    return HttpResponse(template.serialize(output="xhtml"))

def render_jtoolkit(obj):
    """Render old style Pootle display objects which are jToolkit objects
    containing all the necessary information to be rendered."""
    if hasattr(obj, "templatename") and hasattr(obj, "templatevars"):
        return render("%s.html" % obj.templatename, **obj.templatevars)
    else:
        return HttpResponse(obj.getcontents(), obj.content_type)
