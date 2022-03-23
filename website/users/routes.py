from flask import Blueprint, redirect, render_template, url_for, request, flash, abort
from flask_login import login_user, login_required, logout_user, current_user

from website.webforms import LoginForm, RegisterForm, EditAccountForm, ChangePasswordForm, RequestResetPasswordForm, ResetPasswordForm
from website.users.utils import email_or_username_or_not_exist, flash_errors, send_mail
from website.models import User, UserMessage, Post, db
from website.decoretors import check_confirmed

from datetime import datetime



# Blueprint declaration
users = Blueprint('users', __name__, template_folder='users_templates', url_prefix='/user')


# -------------------- Register Route --------------------
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_add = User.query.filter_by(email=form.email.data).first()
        username_check = User.query.filter_by(username=form.username.data).first()
        email = form.email.data

        if user_to_add is None and username_check is None:
            # Add User To Database
            user_to_add = User(name=form.name.data, username=form.username.data, email=email, password=form.password.data)
            db.session.add(user_to_add)
            db.session.commit()

            # Confarmation Email Message With Token Link
            send_mail(user_to_add, base_link='users.confirm', salt='email-confirm', message_title="Email Confirmation", template='mail_templates/email_confirm.html') 

            return redirect(url_for('users.login'))
        else:
            return render_template('error.html', error='User Already Exist!!')
    
    # Clear the form
    form.name.data = ''
    form.username.data = ''
    form.email.data = ''
    form.password.data = ''
    form.re_password.data = ''
        

    return render_template('register.html', form=form)
# -------------------- End of Register Route --------------------


# -------------------- Login Route --------------------
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()


    if current_user.is_authenticated: return redirect(url_for('main.index'))

    if form.validate_on_submit():
        user_is_exist = email_or_username_or_not_exist(form.email.data)

        if user_is_exist and User.verify_password(user_is_exist, form.password.data):
            login_user(user_is_exist, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
        
    form.email.data = ''
    form.password.data = ''
        

    return render_template('login.html', form=form)
# -------------------- End of Login Route --------------------


# -------------------- Logout Route --------------------
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
# -------------------- End of Logout Route --------------------


# -------------------- Profile Route --------------------
@users.route('/profile')
@login_required
@check_confirmed
def profile():
    # Variables
    amount_of_user_messages = len(UserMessage.query.filter_by(user_id=current_user.id).all())
    amount_of_user_posts = len(Post.query.filter_by(poster_id=current_user.id).all())


    return render_template('profile.html', amount_of_user_messages=amount_of_user_messages, amount_of_user_posts=amount_of_user_posts)
# -------------------- End of Profile Route --------------------


# -------------------- Edit_Account Route --------------------
@users.route('/edit_account/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_account(id):
    form = EditAccountForm()
    change_password_form = ChangePasswordForm()
    user_to_update = User.query.get_or_404(id)

    # if request.method == 'POST':

    # Profile Details Form
    if form.identifier.data == 'EditAccountForm' and form.validate_on_submit():
                
        user_to_update.name = request.form['name']

        # Check if Username is aleady exist
        if user_to_update.username != request.form['username']:
            if email_or_username_or_not_exist(request.form['username']) is None:
                user_to_update.username = request.form['username'] 
            else:
                flash("Username is Already Taken", category='error')
        
        # Check if Email is aleady exist
        if user_to_update.email != request.form['email']:
            if email_or_username_or_not_exist(request.form['email']) is None:
                user_to_update.email = request.form['email']
            else:
                flash("Email is Already Taken", category='error')
        
        try:
            db.session.commit()
            flash("User Updated Successfully!", category='success')
        except:
            flash("Error While Updating User - Try Again!!", category='error')

    else:
        flash_errors(form)
        pass

    # Password Changing Form
    if form.identifier.data == 'ChangePasswordForm' and change_password_form.validate_on_submit():
        user_to_update.password = change_password_form.password.data  

        try:
            db.session.commit()
            flash("User Updated Successfully!", category='success')
        except:
            flash("Error While Updating User - Try Again!!", category='error') 

    else:
        flash_errors(change_password_form)


    form.name.data = user_to_update.name
    form.username.data = user_to_update.username
    form.email.data = user_to_update.email

    return render_template('edit_account.html', form=form, change_password_form=change_password_form, id=id, abort=abort)
# -------------------- End of Edit_Account Route --------------------


# -------------------- Email_Confirm Route --------------------
@users.route('/confirm/<token>')
def confirm(token):
    user = User.verify_token(token, "email-confirm")

    if user is None:
        flash("That is an invalid or expired token", category='error')
        return redirect(url_for('main.index'))

    if user.confirm:
        flash("Account Already Confirmed. Please Login.", category='error')
        return redirect(url_for('users.login'))
    else:
        try:
            user.confirm = True
            user.confirm_at = datetime.utcnow()
            db.session.commit()
        except:
            return render_template('error.html', error="Whoops! Somthing Went Wrong - User Doesn't confirmed - Try Again")
        else:
            flash("Thank's {} Your Account is confirmed".format(user.name), category='success')
            return redirect(url_for('users.login'))
# -------------------- End of Email_Confirm Route --------------------


# -------------------- Unconfirm Route --------------------
@users.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirm:
        return redirect(url_for('main.index'))
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')
# -------------------- End of Unconfirm Route --------------------


# -------------------- Resend Route --------------------
@users.route('/resend')
@login_required
def resend_confirmation():
    if current_user.confirm == False:
        # Confarmation Email Message With Token Link
        send_mail(current_user, base_link='users.confirm', salt='email-confirm', message_title="Email Confirmation", template='mail_templates/email_confirm.html') 
        
        flash('A new confirmation email has been sent.', 'success')
        return redirect(url_for('users.unconfirmed'))
    else:
        return redirect(url_for('main.index'))
# -------------------- End of Resend Route --------------------   


# -------------------- Reset_password Route --------------------
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # Make sure user is logged out 
    if current_user.is_authenticated: return redirect(url_for('main.index'))

    form = RequestResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        send_mail(user, base_link='users.reset_password', salt='reset-password', message_title="Reset Password", template='mail_templates/reset_password_confirm.html')

        flash("An email has been sent with instructions to reset your password.", category='success')
        return redirect(url_for('users.login'))

    return render_template('request_reset_token.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Make sure user is logged out 
    if current_user.is_authenticated: return redirect(url_for('main.index'))

    user = User.verify_token(token, "reset-password")

    if user is None:
        flash("That is an invalid or expired token", category='error')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()


        return redirect(url_for('users.login'))

    return render_template('reset_password.html', form=form)
# -------------------- End of Reset_password Route --------------------   