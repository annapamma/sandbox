import io
import json
import pickle
import sys
import urllib.request

import pathway_assessor as pa

import smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def export_csv(df):
    with io.StringIO() as buffer:
        df.to_csv(buffer, sep='\t')
        return buffer.getvalue()


def attach_to_email(df, f_name, msg):
    part = MIMEBase("application", "octet-stream")
    part.set_payload(export_csv(df))
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={f_name}",
    )
    msg.attach(part)


def run_pa(mode, kwargs, ascending, rank_method):
    if mode == 'harmonic':
        res = pa.harmonic(
            **kwargs,
            ascending=ascending,
            rank_method=rank_method,
        )
    elif mode == 'min_p_val':
        res = pa.min_p_val(
            **kwargs,
            ascending=ascending,
            rank_method=rank_method,
        )
    else:
        res = pa.geometric(
            **kwargs,
            ascending=ascending,
            rank_method=rank_method,
        )
    return res


def process(request):
    context = ssl.create_default_context()
    file_id = request.args.get('file_id')
    urllib.request.urlretrieve(f'http://pathwayassessor.org/expression_table/{file_id}', '/tmp/tmp.pkl')
    data = pickle.load(open('/tmp/tmp.pkl', 'rb'))
    expression_table = data['expression_table']
    receiver_email = data['email']
    db = data['db']
    direction = data['direction']
    rank_method = data['rank_method']
    mode = data['mode']

    kwargs = {
        'expression_table': expression_table,
        'db': db,
    }

    subject = "IPAS Results"
    body = """
        Thanks for using IPAS. Your parameters were as follows:

        Pathway database: {}
        Mode: {}
        Direction: {}
        Please see your results attached as a TSV file.

    """.format(db, mode, direction)
    sender_email = "pathwayassessorresults@gmail.com"
    password = "wkmasmlkmwgyleqx"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    if direction == 'difference':
        ascending = run_pa(mode, kwargs, ascending=True, rank_method='max')
        descending = run_pa(mode, kwargs, ascending=False, rank_method='min')
        res = ascending - descending
        attach_to_email(res, f"ipas_{db}_{mode}_difference.csv", message)
        attach_to_email(ascending, f'ipas_{db}_{mode}_ascending.csv', message)
        attach_to_email(descending, f'ipas_{db}_{mode}_descending.csv', message)
    elif direction == 'asc':
        ascending = run_pa(mode, kwargs, ascending=True, rank_method=rank_method)
        attach_to_email(ascending, f'ipas_{db}_{mode}_ascending.csv', message)
    else:
        descending = run_pa(mode, kwargs, ascending=False, rank_method=rank_method)
        attach_to_email(descending, f'ipas_{db}_{mode}_descending.csv', message)

    text = message.as_string()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return json.dumps({'OK': file_id})


if __name__ == '__main__':
    print('test!!')
    print(sys.argv[1])
