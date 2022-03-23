from flask import Blueprint, redirect, render_template, flash, url_for, abort, request
from flask_login import current_user, login_required
from website.webforms import AddPostForm, ReplyForm, EditMessageForm
from website.models import Post, Slug, UserMessage, db
from website.decoretors import check_confirmed



# Blueprint declaration
posts = Blueprint('posts', __name__, template_folder='posts_templates', url_prefix='/posts')


# Constant variables
LIMIT_POST_ON_PAGE = 3


# -------------------- Add_Post Route --------------------
@posts.route('add-post', methods=['GET', 'POST'])
@login_required
@check_confirmed
def add_post():
    form = AddPostForm()

    # Getting all categories to the selected field
    categories = [(g.id, g.name) for g in Slug.query.order_by('name')]
    form.slug.choices = categories


    if form.validate_on_submit():
        poster = current_user.id
        post = Post(title=form.title.data, content=form.content.data, slug=form.slug.data, poster_id=poster)
        
        # Clear the form
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a message to user 
        flash("Blog post  submitted successfully", category='success')


    # Redirect to the webpage
    return render_template('add_post.html', form=form)
# -------------------- End of Add_Post Route --------------------


# -------------------- View_Post Route --------------------
@posts.route('/view-post/<slug>/<int:id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def view_post(slug, id):
    # Variables
    messages = [message for message in UserMessage.query.filter_by(post_id=id)]
    len_messages = len([message for message in messages])
    number_of_pages = len([i for i in range(0, len(messages), LIMIT_POST_ON_PAGE)])

    post = Post.query.get_or_404(id)
    form = ReplyForm()


    if form.validate_on_submit():
        message = UserMessage(content=form.content.data, post_id=id, user_id=current_user.id)
        db.session.add(message)
        db.session.commit()

        number_of_pages = len([i for i in range(0, len([message for message in UserMessage.query.filter_by(post_id=id)]), LIMIT_POST_ON_PAGE)])
        
        return redirect(url_for('posts.view_messages', slug=slug, id=id, page_number=number_of_pages))


    return render_template('view_post.html', slug=slug, id=id, post=post, form=form, messages=messages, 
                                            len_messages=len_messages, limit_post_on_page=LIMIT_POST_ON_PAGE, number_of_pages=number_of_pages)
# -------------------- End of View_Post Route --------------------


# -------------------- View_Messages Route --------------------
@posts.route('/view-post/<slug>/<int:id>/page=<int:page_number>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def view_messages(slug, id, page_number):
    # Variables
    messages = [message for message in UserMessage.query.filter_by(post_id=id)]
    number_of_pages = len([i for i in range(0, len(messages), LIMIT_POST_ON_PAGE)])
    start_list_index = (page_number - 1) * LIMIT_POST_ON_PAGE
    end_list_index = page_number * LIMIT_POST_ON_PAGE

    post = Post.query.get_or_404(id)
    form = ReplyForm()


    if page_number == 1: return redirect(url_for('posts.view_post', slug=slug, id=id))
    if page_number > number_of_pages: return abort(404)
    
    if form.validate_on_submit():
        message = UserMessage(content=form.content.data, post_id=id, user_id=current_user.id)
        db.session.add(message)
        db.session.commit()

        messages = [message for message in UserMessage.query.filter_by(post_id=id)]
        number_of_pages = len([i for i in range(0, len(messages), LIMIT_POST_ON_PAGE)])

        return redirect(url_for('posts.view_messages', slug=slug, id=id, page_number=number_of_pages))


    return render_template('view-messages.html', messages=messages, slug=slug, id=id, post=post, 
                                                form=form, start_list_index=start_list_index, 
                                                end_list_index=end_list_index, number_of_pages=number_of_pages, page_number=page_number)
# -------------------- End of View_Messages Route --------------------


# -------------------- Edit_Message Route --------------------
@posts.route('/edit-message/message-<int:message_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def edit_message(message_id):
    # Variables
    message_to_edit = UserMessage.query.get_or_404(message_id)
    form = EditMessageForm()
    if request.method == 'GET': 
        global referrer 
        referrer = request.referrer


    if form.validate_on_submit():
        message_to_edit.content = form.content.data

        # Update database
        db.session.add(message_to_edit)
        db.session.commit()

        # Return a message to user
        flash("Message has been Edited!", category='success')

        return redirect(referrer)

    if current_user.id == message_to_edit.user_id:
        form.content.data = message_to_edit.content

        return render_template('edit_message.html', form=form, message_id=message_to_edit.id, referrer=referrer)
    else:
        # Return a message to user
        flash("You aren't authorized to edit this message", category='error')
        return redirect(referrer)
# -------------------- End of Edit_Message Route --------------------


# -------------------- Quick_Edit_Message Route --------------------
@posts.route('quick-message-edit-<int:message_id>', methods=['POST'])
@login_required
@check_confirmed
def quick_message_edit(message_id):
    # Variables
    message_to_edit = UserMessage.query.get_or_404(message_id)
    

    if current_user.id == message_to_edit.user_id:

        message_to_edit.content = request.form['content']

        # Update database
        db.session.add(message_to_edit)
        db.session.commit()

        # Return a message to user
        flash("Message has been Edited!", category='success')

        return redirect(request.referrer)

    else:
        # Return a message to user
        flash("You aren't authorized to edit this message", category='error')
        return redirect(request.referrer)
# -------------------- Quick_Edit_Message Route --------------------


# -------------------- Edit_Post Route --------------------
@posts.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def edit_post(id):
    # Variables
    post = Post.query.get_or_404(id)
    form = AddPostForm()


    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data

        # Update database
        db.session.add(post)
        db.session.commit()

        # Return a message to user
        flash("Post has been updated!", category='success')

        return redirect(url_for('posts.view_post', id=post.id))

    if current_user.id == post.poster.id:
        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content

        return render_template('edit_post.html', form=form, post_id=post.id)
    else:
        # Return a message to user
        flash("You aren't authorized to edit this post", category='error')
        return redirect(url_for('posts.my_posts'))
# -------------------- End of Edit_Post Route --------------------


# -------------------- Delete_Post Route --------------------
@posts.route('/delete_post/<int:id>')
@login_required
@check_confirmed
def delete_post(id):
    # Grab all the posts from the database
    post_to_delete = Post.query.get_or_404(id)
    id = current_user.id


    if id == post_to_delete.poster.id or current_user.is_admin == True:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            # Return a message to user
            flash("Post has been deletet!", category='success')

            return redirect(url_for('posts.my_posts'))
        except:
            # Return an error message
            flash("Whoops! There was a problem deleting post - Try Again", category='error')

            return redirect(url_for('posts.my_posts'))
    else:
        # Return an error message
        flash("You aren't authorized to delete that post", category='error')

        return redirect(url_for('posts.my_posts'))
# -------------------- End of Delete_Post Route --------------------


# -------------------- My_Posts Route --------------------
@posts.route('/my_posts')
@login_required
@check_confirmed
def my_posts():
    # Grab all the posts from the database
    posts = Post.query.filter_by(poster_id=current_user.id)


    return render_template('my_posts.html', posts=posts)
# -------------------- End of My_Posts Route --------------------


# -------------------- Posts_Category Route --------------------
@posts.route('/posts/<category>')
@login_required
@check_confirmed
def posts_category(category):
    # Variables
    slug_id = Slug.query.filter_by(name=category).first_or_404()
    posts = Post.query.filter_by(slug=slug_id.id)
    messages = UserMessage.query.order_by('date_posted')


    return render_template('posts_category.html', posts=posts, category=category, messages=messages)
# -------------------- Posts_Category Route --------------------