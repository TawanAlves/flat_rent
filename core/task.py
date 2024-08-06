from celery import shared_task
import os
from core.services.svc_pdf.pdf import PDF


@shared_task
def generate_and_send_pdf_task(email, flatIds):
    pdf = PDF()
    pdf.create_pdf(data={'flat_Ids': flatIds})

    pdf.send_email('Generated PDF', 'Please find the attached PDF.', email)
