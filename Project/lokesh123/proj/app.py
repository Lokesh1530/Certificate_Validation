from flask import Flask, render_template, request, redirect, flash, session, url_for
import hashlib
import json
import os
from datetime import datetime

# Flask setup
app = Flask(__name__)
app.secret_key = "secret_key"  # For session management and flash messages

# Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_from_file()

    def create_block(self, file_hash, previous_hash, student_name, roll_number):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.now()),
            "file_hash": file_hash,
            "previous_hash": previous_hash,
            "student_name": student_name,
            "roll_number": roll_number,
        }
        self.chain.append(block)
        return block


    def get_last_block(self):
        """Get the last block in the chain."""
        return self.chain[-1] if self.chain else None

    def hash(self, block):
        """Generate a SHA-256 hash for a block."""
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def save_to_file(self, filename="blockchain_data.json"):
        """Save blockchain data to a file."""
        with open(filename, "w") as file:
            json.dump(self.chain, file, indent=4)

    def load_from_file(self, filename="blockchain_data.json"):
        """Load blockchain data from a file or create a genesis block."""
        if os.path.exists(filename):
            with open(filename, "r") as file:
                self.chain = json.load(file)
        else:
            # Creating the genesis block
            genesis_block = {
                'index': 1,
                'timestamp': str(datetime.now()),
                'hash': "0",
                'previous_hash': "0"
            }
            self.chain.append(genesis_block)
            self.save_to_file()


# Initializing the blockchain
blockchain = Blockchain()

def hash_file(file_path):
    """Generate a SHA-256 hash for the contents of a file."""
    with open(file_path, "rb") as file:
        return hashlib.sha256(file.read()).hexdigest()


# Admin credentials (for simplicity, hardcoded here)
ADMIN_CREDENTIALS = {"username": "admin", "password": "admin123"}

# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    """Admin login page."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
            session["admin"] = True  # Save admin login state
            flash("Logged in successfully!", "success")
            return redirect(url_for("upload_file"))  # Redirect to the upload page
        else:
            flash("Invalid credentials!", "error")
    return render_template("admin_login.html")


@app.route("/logout")
def logout():
    """Logout route for admin."""
    session.pop("admin", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("index"))


@app.route("/upload", methods=["GET", "POST"])
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    """Upload original file."""
    if not session.get("admin"):  # Ensuring only logged-in admins can access
        flash("You must be logged in as admin to access this page.", "error")
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        student_name = request.form["student_name"]
        roll_number = request.form["roll_number"]
        file = request.files["file"]

        if file:
            # Saving file
            file_path = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(file_path)

            # Hash the file
            file_hash = hash_file(file_path)

            # Create a new block with additional metadata
            last_block = blockchain.get_last_block()
            previous_hash = blockchain.hash(last_block) if last_block else "0"
            blockchain.create_block(file_hash, previous_hash, student_name, roll_number)
            blockchain.save_to_file()

            flash(f"File uploaded successfully for {student_name} (Roll No: {roll_number})!", "success")
            return redirect(url_for("index"))
        else:
            flash("No file selected!", "error")
    return render_template("upload.html")


@app.route("/verify", methods=["GET", "POST"])
@app.route("/verify", methods=["GET", "POST"])
def verify_file():
    """Verify the uploaded file."""
    result = None
    student_name = None
    roll_number = None

    if request.method == "POST":
        file = request.files["file"]

        if file:
            # Saving the file temp for hashing
            file_path = os.path.join("uploads", "temp_verify_file")
            file.save(file_path)

            # Hashing the file
            uploaded_hash = hash_file(file_path)

            # Verifing against the blockchain
            for block in blockchain.chain:
                if block.get("file_hash") == uploaded_hash:
                    result = "The Certificate is valid."
                    student_name = block.get("student_name")
                    roll_number = block.get("roll_number")
                    break
            else:
                result = "The Certificate is fake."

            # Remove the temporary file
            os.remove(file_path)

    return render_template("verify.html", result=result, student_name=student_name, roll_number=roll_number)


@app.route("/blockchain")
def view_blockchain():
    """View the entire blockchain."""
    return render_template("blockchain.html", blockchain=blockchain.chain)


if __name__ == "__main__":
    app.run(debug=True)
