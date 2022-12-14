from smtplib import SMTPException
from socket import gaierror
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .token import account_activation_token
from django.contrib.auth import get_user_model


def send_email(mail_subject, message, message_no_style, to_email):
    try:
        outbox = EmailMultiAlternatives(
            mail_subject,
            message_no_style,
            settings.EMAIL_HOST_USER,
            [to_email],
        )
        outbox.attach_alternative(message, "text/html")
        outbox.send(fail_silently=False)
        return "success"
    except (ConnectionAbortedError, SMTPException, gaierror):
        return "error"


def send_user_email(user, mail_subject, to_email, current_site, template, template_no_style):
    message_no_style = render_to_string(
        template_no_style,
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.id)),
            "token": account_activation_token.make_token(user),
        },
    )

    message = render_to_string(
        template,
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.id)),
            "token": account_activation_token.make_token(user),
        },
    )

    return send_email(mail_subject, message, message_no_style, to_email)


def send_user_email_with_reasons(
    user, mail_subject, to_email, current_site, template, template_no_style, reasons
):
    message_no_style = render_to_string(
        template_no_style,
        {
            "user": user,
            "domain": current_site.domain,
            "reasons": reasons,
        },
    )

    message = render_to_string(
        template,
        {
            "user": user,
            "domain": current_site.domain,
            "reasons": reasons,
        },
    )

    return send_email(mail_subject, message, message_no_style, to_email)


def send_admin_email(
    volunteer,
    mail_subject,
    current_site,
    template,
    template_no_style,
    to_email=settings.EMAIL_HOST_USER,
):

    User = get_user_model()

    user = User.objects.get(email=settings.EMAIL_HOST_USER)

    message_no_style = render_to_string(
        template_no_style,
        {"user": user, "domain": current_site.domain, "volunteer": volunteer},
    )

    message = render_to_string(
        template,
        {"user": user, "domain": current_site.domain, "volunteer": volunteer},
    )

    return send_email(mail_subject, message, message_no_style, to_email)
