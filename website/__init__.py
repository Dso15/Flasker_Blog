from flask import Flask
from flask_migrate import Migrate
from flask_mail import Mail
from flask_ckeditor import CKEditor

from website.config import Config
from website.models import login_manager, db
from website.admin import admin, MyAdminIndexView



migrate = Migrate()
mail = Mail()
ckeditor = CKEditor()


# -------------------- Create_App Func --------------------
def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from website.users.routes import users
    from website.main.routes import main
    from website.posts.routes import posts
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())

    with app.app_context():
        db.create_all()

    return app
# -------------------- End of Create_App Func --------------------