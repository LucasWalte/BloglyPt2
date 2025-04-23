import unittest
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

# Prevent CSRF issues
app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(unittest.TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Clean up"""
        with app.app_context():
            db.drop_all()
            db.create_all()

            user = User(first_name="Test", last_name="User", image_url="https://via.placeholder.com/150")
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

        self.client = app.test_client()

    def tearDown(self):
        """Clean up"""
        with app.app_context():
            db.session.rollback()

    def test_home_redirects(self):
        """Test root route redirects to /users."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/users", resp.location)

    def test_user_list(self):
        """Test the /users page shows the user list."""
        resp = self.client.get("/users")
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Test User", html)

    def test_add_user(self):
        """Test adding a user via POST."""
        resp = self.client.post("/users/new", data={
            "first_name": "New",
            "last_name": "User",
            "image_url": ""
        }, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("New User", html)

    def test_show_user(self):
        """Test showing a single user."""
        resp = self.client.get(f"/users/{self.user_id}")
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Test User", html)

    def test_edit_user(self):
        """Test editing a user via POST."""
        resp = self.client.post(f"/users/{self.user_id}/edit", data={
            "first_name": "Edited",
            "last_name": "Name",
            "image_url": "https://via.placeholder.com/150"
        }, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Edited Name", html)

    def test_delete_user(self):
        """Test deleting a user via POST."""
        resp = self.client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertNotIn("Test User", html)

if __name__ == "__main__":
    unittest.main()
