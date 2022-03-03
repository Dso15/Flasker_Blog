from flask import abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from website.models import db, User



admin = Admin()
admin.add_view(ModelView(User, db.session))


# -------------------- Admin Model --------------------   
class MyAdminIndexView(AdminIndexView):
    template_mode = "bootstrap3"
    def is_accessible(self):
        if current_user.is_authenticated:
            return True if current_user.is_admin == True else False
        else:
            return False
    
    def inaccessible_callback(self, name, **kwargs):
        return abort(404)
# -------------------- End of Admin Model -------------------- 