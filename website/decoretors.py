from flask import redirect, url_for
from flask_login import current_user

from functools import wraps



# -------------------- Check_Confirmed --------------------
def check_confirmed(func):
    """ 
    Check if user is confirmed 
    ----------------------------
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirm is False:
            return redirect(url_for('users.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function
# -------------------- End of Check_Confirmed --------------------