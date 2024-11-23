import http.server
import json
import os
from urllib.parse import parse_qs
from datetime import datetime
import uuid

DATA_FILE = "forum.json"
SESSIONS = {}  # In-memory session store


class ForumServer(http.server.BaseHTTPRequestHandler):
    def load_data(self):
        """Load data from the JSON file."""
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({"users": {}, "categories": {}, "reports": []}, f)
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    def save_data(self, data):
        """Save data to the JSON file."""
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def get_logged_in_user(self):
        """Get the username of the logged-in user from the session."""
        cookie = self.headers.get("Cookie")
        if cookie:
            session_id = cookie.split("=")[-1]
            return SESSIONS.get(session_id)
        return None

    def set_session(self, username):
        """Create a session for the user."""
        session_id = str(uuid.uuid4())
        SESSIONS[session_id] = username
        self.send_header("Set-Cookie", f"session_id={session_id}; HttpOnly")

    def is_admin(self, user):
        """Check if the user is an admin."""
        data = self.load_data()
        return data["users"].get(user, {}).get("is_admin", False)

    def render_template(self, template_name, **context):
        """Render an HTML template."""
        try:
            with open(f"templates/{template_name}", "r") as f:
                content = f.read()
                # Replace placeholders {{ var_name }} with their values
                for key, value in context.items():
                    if isinstance(value, dict) or isinstance(value, list):
                        value = json.dumps(value, indent=4)
                    content = content.replace(f"{{{{ {key} }}}}", str(value))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(content.encode())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Template not found")

    def do_GET(self):
        """Handle GET requests."""
        data = self.load_data()
        user = self.get_logged_in_user()

        if self.path == "/":
            self.render_template("index.html", categories=data["categories"], user=user)
        elif self.path == "/register":
            self.render_template("register.html")
        elif self.path == "/login":
            self.render_template("login.html")
        elif self.path == "/create_discussion":
            if user:
                self.render_template("create_discussion.html", user=user)
            else:
                self.send_response(302)
                self.send_header("Location", "/login")
                self.end_headers()
        elif self.path == "/reports" and user and self.is_admin(user):
            self.render_template("reports.html", reports=data["reports"], user=user)
        elif self.path.startswith("/discussion/"):
            try:
                _, _, category, discussion_id = self.path.split("/")
                discussion_id = int(discussion_id)
                discussion = data["categories"][category][discussion_id]
                self.render_template("discussion.html", category=category, discussion=discussion, discussion_id=discussion_id, user=user)
            except (KeyError, ValueError, IndexError):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Discussion not found")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Page not found")

    def do_POST(self):
        """Handle POST requests."""
        data = self.load_data()
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        params = parse_qs(post_data.decode())
        user = self.get_logged_in_user()

        if self.path == "/register":
            username = params.get("username", [""])[0]
            password = params.get("password", [""])[0]
            is_admin = params.get("is_admin", [""])[0] == "on"
            if username in data["users"]:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"User already exists")
            else:
                data["users"][username] = {"password": password, "is_admin": is_admin}
                self.save_data(data)
                self.send_response(302)
                self.send_header("Location", "/login")
                self.end_headers()
        elif self.path == "/login":
            username = params.get("username", [""])[0]
            password = params.get("password", [""])[0]
            if username in data["users"] and data["users"][username]["password"] == password:
                self.send_response(302)
                self.set_session(username)
                self.send_header("Location", "/")
                self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid username or password")
        elif self.path == "/create_discussion":
            if user:
                category = params.get("category", [""])[0]
                title = params.get("title", [""])[0]
                if category not in data["categories"]:
                    data["categories"][category] = []
                data["categories"][category].append({"title": title, "created_by": user, "messages": []})
                self.save_data(data)
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
            else:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Unauthorized")
        elif self.path.startswith("/discussion/"):
            if user:
                try:
                    _, _, category, discussion_id = self.path.split("/")
                    discussion_id = int(discussion_id)
                    discussion = data["categories"][category][discussion_id]
                    if "delete" in params:
                        if self.is_admin(user):
                            del data["categories"][category][discussion_id]
                            self.save_data(data)
                            self.send_response(302)
                            self.send_header("Location", "/")
                            self.end_headers()
                        else:
                            self.send_response(403)
                            self.end_headers()
                            self.wfile.write(b"Unauthorized")
                    elif "report" in params:
                        data["reports"].append({"category": category, "discussion_id": discussion_id, "title": discussion["title"], "reported_by": user})
                        self.save_data(data)
                        self.send_response(302)
                        self.send_header("Location", "/")
                        self.end_headers()
                except (KeyError, ValueError, IndexError):
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Discussion not found")
            else:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Unauthorized")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Page not found")


if __name__ == "__main__":
    PORT = 8080
    with http.server.HTTPServer(("localhost", PORT), ForumServer) as server:
        print(f"Server running on http://localhost:{PORT}")
        server.serve_forever()
