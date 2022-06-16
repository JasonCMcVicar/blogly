from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)

        second_user = User(first_name="test_first_two", last_name="test_last_two",
                           image_url=None)

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_show_new_user_form(self):
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("new_user page", html)

    def test_add_user(self):
        with self.client as c:
            resp = c.post("/users/new",
                data={'first_name':'test1', 'last_name':'test2',
                'image_url':'https://i.stack.imgur.com/l60Hf.png'})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def test_add_user_redirect(self):
        with self.client as c:
            resp = c.post("/users/new",
                data={'first_name':'test1', 'last_name':'test2',
                'image_url':'https://i.stack.imgur.com/l60Hf.png'},
                follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("test1", html)

    def test_single_user_page(self):
        with self.client as c:
            test_user1 = User(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)

            db.session.add_all([test_user1])
            db.session.commit()
            resp = c.get(f"/users/{test_user1.id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("user_detail page", html)

    def test_edit_user_page(self):
        with self.client as c:
            test_user1 = User(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)

            db.session.add_all([test_user1])
            db.session.commit()
            resp = c.get(f"/users/{test_user1.id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("edit_users page", html)
