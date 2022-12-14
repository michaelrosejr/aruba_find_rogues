import datetime
import os

# from sendgrid import SendGridAPIClient
import sendgrid
import yaml
from jinja2 import (Environment, FileSystemLoader, PackageLoader,
                    select_autoescape)
from loguru import logger
from sendgrid.helpers.mail import Mail


def sendmail(message_details, config, html_template_content):
    message = Mail(
        from_email=message_details['from_email'],
        to_emails=message_details['to_emails'],
        subject=message_details['subject'],
        # html_content='<strong>and easy to do anywhere, even with Python</strong>'
        html_content=html_template_content
        )
    try:
        sg = sendgrid.SendGridAPIClient(message_details['sendgrid_api_key'])
        response = sg.send(message)
    except Exception as e:
        logger.error(e)


def send_template_email(template, message_details, found, all_types, account):
    body = {
        'rdata': found,
        'all_types': all_types,
        'file_details': __file__
    }

    env = Environment(
        # loader=PackageLoader('project', 'email_templates'),
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(template)

    sendmail(message_details, account, html_template_content=template.render(body))

if __name__ == "__main__":
    none = []
    with open(".env.yaml", "r") as envf:
        central_info = yaml.safe_load(envf)
    account = central_info['default']
    message_details = {
        "from_email": account['from_email'],
        "to_emails": account['to_emails'],
        "subject": "Wireless Rogue AP Alert",
        "sendgrid_api_key": account['sendgrid_api_key']
    }

    rdata = []
    send_template_email('rogues_found.html.jinja2', message_details, rdata, rdata, account=account)
