import os 
from website.models import User
from flask import flash, url_for, render_template
from flask_mail import Message
from website import mail



# -------------------- Email_Or_Username_Or_Not_Exist Func --------------------
def email_or_username_or_not_exist(string):
    """
    Check if user enter Email or Username and check if User is exist.
    -----------------------------------------------------------------

    string = email or username \n
    return = user column or None
    """
    user_is_exist_email = User.query.filter_by(email=string ).first()
    user_is_exist_username = User.query.filter_by(username=string).first()
    
    if user_is_exist_email:
        return user_is_exist_email
    elif user_is_exist_username:
        return user_is_exist_username
    else:
        return None
# -------------------- End of Email_Or_Username_Or_Not_Exist Func --------------------


# -------------------- Flash_Error Func --------------------
def flash_errors(form):
    """
    Flash Wtforms error messages.
    -----------------------------

    form = wtforms form \n
    return = flash error messages
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash("{}: {}".format(field, error), category='error')
# -------------------- End of Flash_Error Func --------------------


# -------------------- Send_Mail Func --------------------
def send_mail(user, base_link, salt, message_title, template):
    """
    Create token + build url with 'url_for' and send mail.
    ----------------------------------------------------

    user = The user who will recieve the message \n
    base_link = Base func for url_for.\n
    salt = Salt for generating token. \n
    message_title = The title for the mail message. \n
    template = Template for the mail message. 
    """
    link = url_for(base_link, token=user.get_token(salt), _external=True)

    msg = Message(subject=message_title, sender=os.environ.get('MAIL_SENDER'), recipients=[user.email])
    msg.html = render_template(template, link=link)

    mail.send(msg)
# -------------------- End of Send_Mail Func --------------------