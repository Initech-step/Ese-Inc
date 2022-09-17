from flask import redirect, flash, url_for
from eseweb import app, db
from flask import render_template, request
from eseweb.models import Users, Posts, Category, Projects, EmailList, ClientReviews, Faqs

from eseweb.forms import MakePostForm, CreateProjectForm, AddEmailForm, CreateCategoryForm, AddReviewForm, SearchForm, TestUploadForm, AddFAQ, LoginForm, RegisterForm, EditPostForm

from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required
from datetime import datetime

@app.route('/')
def hello():
    client_reviews = ClientReviews.query.limit(3).all()
    latest_posts = db.session.query(Posts).order_by(Posts.id.desc()).limit(2)

    return render_template('index.html', 
    client_reviews=client_reviews,
    latest_posts=latest_posts)



@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            search_text = form.search.data
            search_by = form.search_by.data

            if search_by == 'title':
                search_query = "%{}%".format(search_text)
                results_q = Posts.query.filter(Posts.title.ilike(search_query)).all()
                return render_template('search_posts.html', form=form, results=results_q)


            elif search_by == 'body':
                search_query = "%{}%".format(search_text)
                results_q = Posts.query.filter(Posts.body.ilike(search_query)).all()
                return render_template('search_posts.html', form=form, results=results_q)

            else:
                search_query = "%{}%".format(search_text)
                results_q = Posts.query.filter(Posts.body.ilike(search_query)).all()
                return render_template('search_posts.html', form=form, results=results_q)

        else:
            flash('Invalid data entered', 'danger')
            return redirect(url_for('search'))

    return render_template('search_posts.html', form=form)


@app.route('/blog/home')
def blog_home():
    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Posts).order_by(Posts.id.desc()).paginate(per_page=4, page=page)
    categories = Category.query.all()
    last_post = db.session.query(Posts).order_by(Posts.id.desc()).first()
    level = 'All'
    return render_template('blog_home.html', posts=posts, categories=categories, last_post=last_post, level=level)


@app.route('/blog/category/<int:category_id>')
def blog_by_category(category_id):
    #know the current category
    current_category = Category.query.get_or_404(category_id)  
    #get the page requested
    page = request.args.get('page', 1, type=int)
    #get all posts concerning the category
    posts = db.session.query(Posts).filter_by(category_id=category_id).order_by(Posts.id.desc()).paginate(per_page=4, page=page)
    #get all categories for listing
    categories = Category.query.all()
    #get the last post
    last_post = db.session.query(Posts).order_by(Posts.id.desc()).first()
    return render_template('category_blog.html', posts=posts, categories=categories, last_post=last_post, current_category=current_category)




@app.route('/blog/post/<int:post_id>')
def blog_post(post_id):
    read_target = Posts.query.get_or_404(post_id)
    categories = Category.query.all()
    return render_template('single_blog_post.html', post=read_target, categories=categories)



@app.route('/projects')
def projects():
    projects = Projects.query.all()
    return render_template('our_projects.html', projects=projects)


@app.route('/aboutus')
def aboutus():
    client_reviews = ClientReviews.query.limit(3).all()
    return render_template('about_us.html', client_reviews=client_reviews)


@app.route('/faqs')
def faqs():
    faqs = Faqs.query.all()
    return render_template('faqs.html', faqs=faqs)



@app.route('/ourteam')
def ourteam():
    return render_template('our_team.html')




def check_for_duplicate(check_email):
    mails = EmailList.query.all()
    for mail in mails:
        if mail.Email == check_email:
            return False
    return True




@app.route('/subscribe_newsletter', methods=['GET', 'POST'])
def subscribe_to_newsletter():
    form = AddEmailForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            try_clone = check_for_duplicate(form.email.data)
            if try_clone:
                email_to_add = EmailList(Email=form.email.data)
                db.session.add(email_to_add)
                db.session.commit()
                flash('You have successfully subscribed!', 'success')
                return redirect(url_for('subscribe_to_newsletter'))
            else:
                flash('This email is already subscribed', 'danger')
                return redirect(url_for('subscribe_to_newsletter'))
        else:
            flash('Invalid email, not added', 'danger')
            return redirect(url_for('subscribe_to_newsletter'))

    return render_template('subscribe_to_newsletter.html', form=form)





#Blog Post section
#Blog Post section
#Blog Post section



@app.route('/panel')
@login_required
def panel_home():
    return render_template('panel_index.html')



@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    delete_target = Posts.query.get_or_404(post_id)

    if request.method == 'POST':
        db.session.delete(delete_target)
        db.session.commit()
        flash('Post successfully deleted', 'success')
        return redirect(url_for('updelpost'))
        
    return render_template('confirm_delete_posts.html')





@app.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):

    update_target = Posts.query.get_or_404(post_id)
    form = EditPostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    #to check validity of data
    if request.method == 'POST':
        if form.validate_on_submit():

            update_target.title = form.title.data
            update_target.body = form.body.data
            update_target.preview_text = form.post_preview.data
            update_target.category_id = form.category.data
            update_target.mins_read = form.mins_read.data

            db.session.commit()
            flash('Post successfully Updated', 'success')
            return redirect(url_for('updelpost'))
        else:
            flash('Invalid data entered', 'danger')
            return redirect(url_for('updelpost'))

    elif request.method == 'GET':
        print('hh')
        #to put in existing data into the form
        form.title.data = update_target.title
        form.body.data = update_target.body
        form.post_preview.data = update_target.preview_text
        form.category.data = update_target.category_id
        form.mins_read.data = update_target.mins_read

        return render_template('edit_post.html', form=form)
    else:
        return 'Not permitted'


@app.route('/panel/post/updelpost')
@login_required
def updelpost():
    all_posts = Posts.query.all()
    return render_template('update_delete.html', all_posts=all_posts)



@app.route('/panel/post/view_all_posts')
@login_required
def viewposts():
    all_posts = Posts.query.all()
    return render_template('see_posts.html', all_posts=all_posts)




@app.route('/panel/post/makepost', methods=['GET', 'POST'])
@login_required
def make_post():

    form = MakePostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if request.method == 'POST':

        if form.validate_on_submit():

            # prepare filename for post image
            filename = secure_filename(form.photo.data.filename)

            # save the image
            form.photo.data.save('eseweb/static/blog_posts_image/' + filename)

            post_to_make = Posts(
                title=form.title.data, 
                body=form.post_body.data, 
                mins_read=form.mins_read.data, 
                category_id=form.category.data, 
                post_image=filename,
                preview_text=form.post_preview.data
            )

            #save the post
            db.session.add(post_to_make)
            db.session.commit()

            flash('Post successfully Made!', 'success')
            return redirect(url_for('make_post'))

        else:
            flash('Invalid data entered', 'danger')
            return redirect(url_for('make_post'))

    return render_template('make_post.html', form=form)













##PROJECT SECTION
##PROJECT SECTION
##PROJECT SECTION
@app.route('/panel/project/create_proj', methods=['GET', 'POST'])
@login_required
def create_project():

    form = CreateProjectForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            project_to_create = Projects(project_name=form.project_name.data, 
                                        project_description=form.project_description.data, 
                                        client_name=form.client_name.data, 
                                        client_review=form.client_review.data)

            db.session.add(project_to_create)
            db.session.commit()
            flash('Project successfully Posted!', 'success')
            return redirect(url_for('create_project'))

        else:
            flash('Invalid data entered !', 'danger')
            return redirect(url_for('create_project'))

    elif request.method == 'GET':
        return render_template('create_project.html', form=form)

    else:
        return 'Not Permitted'



@app.route('/panel/project/update_proj/<int:proj_id>', methods=['GET', 'POST'])
@login_required
def update_project(proj_id):
    form = CreateProjectForm()
    target_update = Projects.query.get_or_404(proj_id)

    if request.method == 'POST':
        if form.validate_on_submit():
            target_update.project_name = form.project_name.data
            target_update.project_description = form.project_description.data
            target_update.client_name = form.client_name.data
            target_update.client_review = form.client_review.data
            db.session.commit()
            flash('Project successfully Updated!', 'success')
            return redirect(url_for('updel_project'))
        else:
            flash('Invalid data entered!', 'danger')
            return redirect(url_for('updel_project'))

    elif request.method == 'GET':
        #populate fields
        form.project_name.data = target_update.project_name
        form.project_description.data = target_update.project_description
        form.client_name.data = target_update.client_name
        form.client_review.data = target_update.client_review
        #render
        return render_template('create_project.html', form=form)
    else:
        return 'Not Permitted'


@app.route('/panel/project/updelproj')
@login_required
def updel_project():
    all_projects = Projects.query.all()
    return render_template('view_projects.html', all_projects=all_projects)


@app.route('/panel/project/delete/<int:proj_id>', methods=['GET', 'POST'])
@login_required
def delete_project(proj_id):
    delete_target = Projects.query.get_or_404(proj_id)

    if request.method == 'POST':
        db.session.delete(delete_target)
        db.session.commit()
        flash('Project successfully deleted!', 'success')
        return redirect(url_for('updel_project'))
 
    return render_template('confirm_delete_proj.html')









## email section
## email section
## email section
## email section
## email section

@app.route('/panel/email/add_email', methods=['GET', 'POST'])
@login_required
def add_email():

    form = AddEmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email_to_add = EmailList(Email=form.email.data)
            db.session.add(email_to_add)
            db.session.commit()
            flash('Email successfully added!', 'success')
            return redirect(url_for('list_emails'))
        else:
            flash('Invalid email, not added', 'danger')
            return redirect(url_for('list_emails'))

    elif request.method == 'GET':
        return render_template('add_email.html', form=form)
    else:
        return 'Not Permitted'


@app.route('/panel/email/listall')
@login_required
def list_emails():
    all_emails = EmailList.query.all()
    return render_template('list_emails.html', all_emails=all_emails)


@app.route('/panel/email/listall/delete/<int:email_id>', methods=['GET', 'POST'])
@login_required
def delete_email(email_id):
    delete_target = EmailList.query.get_or_404(email_id)

    if request.method == 'POST':
        db.session.delete(delete_target)
        db.session.commit()
        flash('Email successfully deleted!', 'success')
        return redirect(url_for('list_emails'))
 
    return render_template('confirm_delete_email.html')








#category section
#category section
#category section
#category section
#category section


@app.route('/panel/category/create_category', methods=['GET', 'POST'])
@login_required
def create_category():

    form = CreateCategoryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            category_to_create = Category(name=form.category_name.data)
            db.session.add(category_to_create)
            db.session.commit()
            flash('Category successfully added!', 'success')
            return redirect(url_for('list_categories'))

        else:
            flash('Invalid data', 'danger')
            return redirect(url_for('list_categories'))

    elif request.method == 'GET':
        return render_template('create_category.html', form=form)
    else:
        return 'Not Permitted'



@app.route('/panel/category/listall')
@login_required
def list_categories():
    all_categories = Category.query.all()
    return render_template('view_update_cat.html', categories=all_categories)



@app.route('/panel/category/listall/update/<int:category_id>', methods=['GET', 'POST'])
@login_required
def update_category(category_id):
    update_target = Category.query.get_or_404(category_id)
    form = CreateCategoryForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            update_target.name = form.category_name.data
            db.session.commit()
            flash('Category successfully Updated!', 'success')
            return redirect(url_for('list_categories'))
        else:
            flash('Invalid data', 'danger')
            return redirect(url_for('list_categories'))

    elif request.method == 'GET':
        #populate fields
        form.category_name.data = update_target.name
        return render_template('create_category.html', form=form)
    else:
        return 'Not Permitted'












#reviews section
#reviews section
#reviews section
#reviews section
#reviews section

@app.route('/panel/review/add_review', methods=['GET', 'POST'])
@login_required
def add_review():

    form = AddReviewForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            review_to_add = ClientReviews(client_name=form.client_name.data, client_review=form.client_review.data)
            db.session.add(review_to_add)
            db.session.commit()
            flash('review successfully added!', 'success')
            return redirect(url_for('updel_reviews'))
        else:
            flash('Invalid data', 'danger')
            return redirect(url_for('updel_reviews'))

    elif request.method == 'GET':
        return render_template('create_customer_review.html', form=form)
    else:
        return 'Not Permitted'




@app.route('/panel/review/listall')
@login_required
def updel_reviews():
    all_reviews = ClientReviews.query.all()
    return render_template('updel_client_review.html', reviews=all_reviews)





@app.route('/panel/review/listall/update/<int:review_id>', methods=['GET', 'POST'])
@login_required
def update_review(review_id):
    update_target = ClientReviews.query.get_or_404(review_id)
    form = AddReviewForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            update_target.client_name = form.client_name.data
            update_target.client_review = form.client_review.data
            db.session.commit()
            flash('review successfully Updated!', 'success')
            return redirect(url_for('updel_reviews'))
        else:
            flash('Invalid data', 'danger')
            return redirect(url_for('updel_reviews'))

    elif request.method == 'GET':
        #populate fields
        form.client_name.data = update_target.client_name
        form.client_review.data = update_target.client_review
        return render_template('create_customer_review.html', form=form)
    else:
        return 'Not Permitted'




@app.route('/panel/project/delete_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def delete_review(review_id):
    delete_target = ClientReviews.query.get_or_404(review_id)

    if request.method == 'POST':
        db.session.delete(delete_target)
        db.session.commit()
        flash('review successfully deleted!', 'success')
        return redirect(url_for('updel_reviews'))
 
    return render_template('delete_customer_review.html')





#test
#test
#test
@app.route('/testupload', methods=['POST', 'GET'])
def test_upload():
    form = TestUploadForm()
    if request.method =='POST':
        if form.validate_on_submit():
            print(type(form.photo.data))
            filename = secure_filename(form.photo.data.filename)
            print(filename)
            form.photo.data.save('uploads/' + filename)
            return 'Done'

        else:
            return 'This form is invalid'
    return render_template('test_upload.html', form=form)





#FAQ
#FAQ
#FAQ

@app.route('/panel/faq/addfaq', methods=['GET', 'POST'])
@login_required
def addfaq():
    form = AddFAQ()
    if request.method == 'POST':
        if form.validate_on_submit():
            faq_to_add = Faqs(question=form.question.data, answer=form.question.data)
            db.session.add(faq_to_add)
            db.session.commit()
            flash('FAQ successfully added', 'success')
            return redirect(url_for('read_faqs'))
    else:
        return render_template('add_faqs.html', form=form)

@app.route('/panel/faq/readfaq', methods=['GET', 'POST'])
def read_faqs():
    all_faqs = Faqs.query.all()
    return render_template('read_faqs.html', faqs=all_faqs)






@app.route('/panel/project/delete_faq/<int:faq_id>', methods=['GET', 'POST'])
@login_required
def delete_faq(faq_id):
    delete_target = Faqs.query.get_or_404(faq_id)

    if request.method == 'POST':
        db.session.delete(delete_target)
        db.session.commit()
        flash('FAQ successfully deleted!', 'success')
        return redirect(url_for('read_faqs'))
 
    return render_template('confirm_delete_faqs.html')








#authentication
#authentication
#authentication

@app.route('/admin/panelo/hidreg', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_to_create = Users(email=form.email.data, username=form.username.data, password_enc=form.password.data)
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for('loginroute'))
    return render_template('register.html', form=form)


@app.route('/admin/panel/res/login', methods=['GET', 'POST'])
def loginroute():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            attempted_user = Users.query.filter_by(email=form.email.data).first()
            if attempted_user and attempted_user.check_password(form.password.data):
                login_user(attempted_user)
                flash('You have been loged in. Welcome', 'success')
                return redirect(url_for('panel_home'))
            else:
                return redirect(url_for('hello'))
    return render_template('login.html', form=form)


@app.route('/admin/panel/res/logout')
def logoutroute():
    logout_user()
    return redirect(url_for('loginroute'))


