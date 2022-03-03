from flask import Blueprint, redirect, render_template, flash, url_for
from flask_login import current_user, login_required
from website.webforms import AddPostForm
from website.models import Post, db
from website.decoretors import check_confirmed



# Blueprint declaration
posts = Blueprint('posts', __name__, template_folder='posts_templates', url_prefix='/posts')


# -------------------- Add_Post Route --------------------
@posts.route('add-post', methods=['GET', 'POST'])
@login_required
@check_confirmed
def add_post():
    form = AddPostForm()

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
@posts.route('/view-post/<int:id>')
@login_required
@check_confirmed
def view_post(id):
    post = Post.query.get_or_404(id)

    return render_template('view_post.html', post=post)
# -------------------- End of View_Post Route --------------------


# -------------------- Edit_Post Route --------------------
@posts.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def edit_post(id):
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

    return render_template('posts.html', posts=posts)
# -------------------- End of My_Posts Route --------------------