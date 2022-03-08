from flask import Blueprint, render_template
from website.models import Post, Slug
from website.webforms import SearchForm



# Blueprint declaration
main = Blueprint('main', __name__, template_folder='main_templates')



# Pass stuff to base file
@main.app_context_processor
def base():
    form = SearchForm()
    categories = Slug.query.order_by('id')
    return dict(form=form, categories=categories)

    
# -------------------- Index Route --------------------
@main.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted)

    # Post the latest 3 post.
    return render_template('index.html', posts=posts[-3:])
# -------------------- End of Index Route --------------------


# -------------------- Search Route --------------------
@main.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Post.query

    if form.validate_on_submit():
        # Get data from submitted form
        post_searched = form.searched.data
        # Query the Database
        posts = posts.filter(Post.content.like('%' + post_searched + '%'))
        posts = posts.order_by(Post.title).all()

        return render_template('search.html', form=form, searched=post_searched, posts=posts)
# -------------------- End of Search Route --------------------


# -------------------- Error Page Handaling --------------------
# Invalid URL
@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=error), 404


# Internal Server Error
@main.app_errorhandler(500)
def page_not_found(error):
    return render_template('error.html', error=error), 500
# -------------------- End of Error Page Handaling --------------------