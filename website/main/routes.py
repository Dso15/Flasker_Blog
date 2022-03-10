from email import message
from flask import Blueprint, redirect, render_template, url_for, request
from website.models import Post, Slug, UserMessage
from website.webforms import SearchForm



# Blueprint declaration
main = Blueprint('main', __name__, template_folder='main_templates')


# Pass stuff to base file
@main.app_context_processor
def base():
    form = SearchForm()
    categories = Slug.query.order_by('id')
    messages = UserMessage.query.order_by('id')
    return dict(form=form, categories=categories, messages=messages)

    
# -------------------- Index Route --------------------
@main.route('/')
def index():
    # Variables
    amount_of_latest_posts = -6 # Number should be negative
    slugs = Slug.query.order_by('id').all()
    messages = UserMessage.query.order_by('date_posted').all()

    #  amount_of_latest_posts should be negative because the list order_by 'date_posted', Last 'post' is in the last 'index'.
    post_by_time_and_slug = [dict(category=slug, posts=Post.query.filter_by(slug=slug.id).order_by('date_posted').all()[amount_of_latest_posts:]) for slug in slugs]

    
    return render_template('index.html', messages=messages, post_by_time_and_slug=post_by_time_and_slug, amount_of_latest_posts=abs(amount_of_latest_posts))
# -------------------- End of Index Route --------------------


# -------------------- Search Route --------------------
@main.route('/search', methods=['GET', 'POST'])
def search():
    # Variables
    form = SearchForm()
    posts = Post.query


    if request.method == 'GET': return redirect(url_for('main.index'))


    if form.validate_on_submit():
        print('form sent')
        # Get data from submitted form
        post_searched = form.searched.data
        # Query the Database
        posts = posts.filter(Post.content.like('%' + post_searched + '%'))
        posts = posts.order_by(Post.title).all()


        return render_template('search.html', form=form, searched=post_searched, posts=posts)
    else:
        return redirect(request.referrer)
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