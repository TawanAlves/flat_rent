import pdfkit
import jinja2
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class PDF:
    def __init__(self):
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath='./'))

    def send_email(self, subject, body, to_email):
        from_email = 'your email'
        password = 'your password'

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        output_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'output/meu_arquivo.pdf'))
        with open(output_file, 'rb') as file:
            part = MIMEApplication(file.read(), Name='attachment.pdf')
            part['Content-Disposition'] = f'attachment; filename="attachment.pdf"'
            msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)

        print('Email with PDF sent successfully!')

        if os.path.exists(output_file):
            os.remove(output_file)
            print("File deleted successfully!")

    def create_pdf(self, data: dict) -> None:
        base_dir = os.path.dirname(__file__)
        input_folder = os.path.abspath(os.path.join(base_dir, 'input'))
        output_folder = os.path.abspath(os.path.join(base_dir, 'output'))
        os.makedirs(output_folder, exist_ok=True)

        template_file = os.path.abspath(
            os.path.join(input_folder, 'index.html'))
        output_file = os.path.abspath(
            os.path.join(output_folder, 'meu_arquivo.pdf'))
        css_file = os.path.abspath(os.path.join(input_folder, 'style.css'))

        print(f"Base directory: {base_dir}")
        print(f"Template file path: {template_file}")
        print(f"CSS file path: {css_file}")
        print(f"Output file path: {output_file}")

        if not os.path.exists(template_file):
            raise FileNotFoundError(
                f"Template file '{template_file}' does not exist.")
        if not os.path.exists(css_file):
            raise FileNotFoundError(f"CSS file '{css_file}' does not exist.")
        print(f"Template file path: {template_file}")
        print(f"CSS file path: {css_file}")
        print(f"Output file path: {output_file}")

        if not os.path.exists(template_file):
            raise FileNotFoundError(
                f"Template file '{template_file}' does not exist.")
        if not os.path.exists(css_file):
            raise FileNotFoundError(f"CSS file '{css_file}' does not exist.")

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
