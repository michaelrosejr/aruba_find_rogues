import datetime
import os

# from sendgrid import SendGridAPIClient
import sendgrid
import yaml
from jinja2 import (Environment, FileSystemLoader, PackageLoader,
                    select_autoescape)
from loguru import logger
from sendgrid.helpers.mail import Mail

rdata = [
    {
        'acknowledged': False,
        'classification': 'Rogue',
        'containment_status': 'Un-contained',
        'cust_id': '5bf9f40bc876413dac2a533d392d6fa1',
        'encryption': 'OPEN',
        'first_det_device': 'CNH2HN797D',
        'first_det_device_name': 's1262ap3',
        'first_seen': '2022-04-07T06:41:02.515Z',
        'group_name': 'West -1',
        'id': '00:30:44:19:C5:40',
        'labels': 'Some(505)',
        'last_det_device': 'CNH2HN7972',
        'last_det_device_name': 's1262ap1',
        'last_seen': '2022-11-21T17:04:24.244Z',
        'mac_vendor': 'CradlePoint, Inc',
        'name': 'CradlePoint,-19:C5:40',
        'overriden': False,
        'signal': -21,
        'ssid': 'SephoraFreeWifi',
        'human_first_seen': 'Thursday, 07-Apr-2022 06:41:02 UTC'
    },
    {
        'acknowledged': False,
        'classification': 'Rogue',
        'containment_status': 'Un-contained',
        'cust_id': '5bf9f40bc876413dac2a533d392d6fa1',
        'encryption': 'WPA',
        'first_det_device': 'PHL4KD56BD',
        'first_det_device_name': 's212ap1',
        'first_seen': '2021-12-11T02:32:00.101Z',
        'group_name': 'East -2',
        'id': '00:30:44:2B:6B:40',
        'labels': 'Some(180)',
        'last_det_device': 'PHL4KD56BG',
        'last_det_device_name': 's212ap2',
        'last_seen': '2022-11-21T17:57:13.800Z',
        'mac_vendor': 'CradlePoint, Inc',
        'name': 'CradlePoint,-2B:6B:40',
        'overriden': False,
        'signal': -24,
        'ssid': 'teamwork',
        'human_first_seen': 'Saturday, 11-Dec-2021 02:32:00 UTC'
    },
    {
        'acknowledged': False,
        'classification': 'Rogue',
        'containment_status': 'Un-contained',
        'cust_id': '5bf9f40bc876413dac2a533d392d6fa1',
        'encryption': 'OPEN',
        'first_det_device': 'PHL4KD56BD',
        'first_det_device_name': 's212ap1',
        'first_seen': '2022-04-01T18:37:50.487Z',
        'group_name': 'East -2',
        'id': '02:30:44:2B:6B:40',
        'labels': 'Some(180)',
        'last_det_device': 'PHL4KD56BG',
        'last_det_device_name': 's212ap2',
        'last_seen': '2022-11-21T17:57:13.749Z',
        'mac_vendor': '02:30:44:2B:6B:40',
        'name': '02:30:44:2B:6B:40',
        'overriden': False,
        'signal': -19,
        'ssid': 'Sephora Free WiFi',
        'human_first_seen': 'Friday, 01-Apr-2022 18:37:50 UTC'
    }
]



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
    # send_email(to, subj, template.render(**kwargs))
    # with open("index.html", "w") as f:
    #     f.write(template.render(body))
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
    }
    # sendmail("test")
    print(account['sendgrid_api_key'])
    print(message_details)
    # sendmail(message_details, account)
    send_template_email('rogues_found.html.jinja2', message_details, rdata, rdata, account=account)
