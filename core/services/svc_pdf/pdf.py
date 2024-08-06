import pdfkit
import jinja2
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import config


def send_email(subject, body, to_email):
    from_email = config.EMAIL
    password = config.PASSWORD
    # to_email = config.TOEMAIL

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open('./output/meu_arquivo.pdf', 'rb') as file:
        part = MIMEApplication(file.read(), Name='attachment.pdf')
        part['Content-Disposition'] = f'attachment; filename="attachment.pdf"'
        msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

    print('Email with PDF sent successfully!')


class PDF:
    def __init__(self):
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath='./'))

    def create_pdf(self, data: dict, template_file: str, output_file: str, css_file: str) -> None:
        with open(template_file, 'r') as f:
            template = f.read()
        template = self._populate_template(data, template, css_file)
        options = {
            'page-size': 'A4',
            'margin-top': '0',
            'margin-right': '0',
            'margin-bottom': '0',
            'margin-left': '0',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'debug-javascript': True,
        }
        pdfkit.from_string(template, output_file, options=options)
        print(f"PDF generated successfully at '{output_file}'.")

    def _populate_template(self, data: dict, template: str, css_file: str) -> str:
        """Populates the template with the needed data and CSS."""
        jinja_template = self.environment.from_string(template)
        with open(css_file, 'r') as f:
            css_content = f.read()
        data_with_css = {**data, 'style': css_content}
        return jinja_template.render(**data_with_css)
   #   print(f"Ocorreu um erro: {e}")


pdf = PDF()
try:
    input_folder = os.path.join(os.getcwd(), 'input')
    output_folder = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_folder, exist_ok=True)
    css_file = os.path.join(input_folder, 'style.css')

    pdf.create_pdf(
        data={},
        template_file='./input/index.html',
        output_file='./output/meu_arquivo.pdf',
        css_file=css_file
    )

    with open('./output/meu_arquivo.pdf', 'rb') as f:
        print("O arquivo foi gerado com sucesso!")
        send_email('Test Subject', 'Test Body')
except FileNotFoundError:
    print("Arquivo não encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")


# send_email('Test Subject', 'Test Body', 'CV.pdf')
