from datetime import datetime

import yaml
from jinja2 import (Environment, FileSystemLoader, PackageLoader,
                    select_autoescape)
from loguru import logger


# def save_to_file(template, found, all_types):
def save_to_file(template, rogues, found):

    body = {
        'rdata': rogues,
        'all_types': found,
        'file_details': __file__
    }


    template_env = Environment(
        loader=FileSystemLoader('templates'),
        # autoescape=select_autoescape(['html', 'xml'])
    )
    template = template_env.get_template(template)
    now = datetime.now().isoformat().split(".")[0]
    with open(f"rogues_found-{now}.html", "w") as f:
        f.write(template.render(body))


if __name__ == "__main__":
    rdata = []
    save_to_file('rogues_found.html.jinja2', rdata, rdata)
