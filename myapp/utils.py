from io import BytesIO
from django.template.loader import get_template
from django.core.mail import EmailMessage
from weasyprint import HTML, CSS
from django.contrib.staticfiles import finders

def generar_pdf_factura(pago):
    template = get_template("factura-email.html")
    context = {
        "alumno": pago.alumno,
        "tutores": pago.alumno.tutores.all(),
        "colegiatura": pago,
    }
    html_string = template.render(context)

    css_path = finders.find("Styles/factura.css")

    pdf_file = BytesIO()
    HTML(string=html_string, base_url=".").write_pdf(
        pdf_file,
        stylesheets=[CSS(filename=css_path)]
    )
    return pdf_file.getvalue()

def enviar_factura_por_correo(pago):
    pdf_bytes = generar_pdf_factura(pago)

    asunto = f"Factura de colegiatura {pago.mes}"
    mensaje = f"Adjunto encontrarás la factura del pago de {pago.mes}."
    destinatarios = [t.email for t in pago.alumno.tutores.all() if t.email]

    email = EmailMessage(
        subject=asunto,
        body=mensaje,
        from_email="juanguzmango01@gmail.com",
        to=destinatarios,
    )
    email.attach(f"factura_{pago.alumno}.pdf", pdf_bytes, "application/pdf")
    email.send()
