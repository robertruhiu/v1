# from __future__ import absolute_import, unicode_literals
#
# import json
#
# from decouple import config
# from django.core.mail import get_connection, EmailMessage
# # from templated_email import get_templated_mail
#
#
# def async_send_email(email, from_address, message):
#     message: EmailMessage(
#         # template_name=template_name,
#         from_email=from_address,
#         to=[email]
#         # context=context
#     )
#
#     message.extra_headers = {'X-Mailgun-Tag': context['email_type'],
#                                  'X-Mailgun-Variables': json.dumps({"subject": message.subject})}
#     message.connection = get_connection(host=config('EMAIL_HOST_MAILGUN', default='smtp.mailgun.org'),
#                                             port=587,
#                                             username=config('EMAIL_HOST_USER_MAILGUN',
#                                                             default='postmaster@mg.legalforms.ng'),
#                                             password=config('EMAIL_HOST_PASSWORD_MAILGUN',
#                                                             default='EMAIL_HOST_PASSWORD_MAILGUN'),
#                                             use_tls=True)
#     message.send()
