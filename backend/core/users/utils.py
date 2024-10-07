from django.core.mail import send_mail


def send_mail_async(user_email,email_str):
            send_mail(
                'Your Verification Code',
                from_email="mr.goku.0619@gmail.com",
                html_message=email_str,
                fail_silently=True,
                message='',
                recipient_list=[user_email]
                )
        