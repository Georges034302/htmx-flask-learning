import os
import time
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, flash, get_flashed_messages, session, redirect, url_for, current_app

from data.mock import employees, users
from utils.auth import login_required

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "txt", "csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def home():
	return render_template("index.html")


@main.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form.get("username", "").strip()
		password = request.form.get("password", "")

		if username in users and users[username] == password:
			session["user"] = username
			return redirect(url_for("main.home"))

		flash("Invalid username or password.")
		return redirect(url_for("main.login"))

	return render_template("login.html")


@main.route("/logout")
def logout():
	session.pop("user", None)
	return redirect(url_for("main.login"))


@main.route("/hello")
def hello():
	return "<h3>Hello HTMX + Flask!</h3>"


@main.route("/hello-toggle")
def hello_toggle():
	show_message = session.get("show_hello_message", False)
	if show_message:
		session["show_hello_message"] = False
		return ""

	session["show_hello_message"] = True
	return "<h3>Hello HTMX + Flask!</h3>"


@main.route("/search")
def search():
	time.sleep(1)

	query = request.args.get("query", "").lower()

	filtered_employees = []
	for employee in employees:
		name_match = query in employee["name"].lower()
		department_match = query in employee["department"].lower()
		if name_match or department_match:
			filtered_employees.append(employee)

	return render_template(
		"partials/search_results.html",
		employees=filtered_employees
	)


@main.route("/messages")
def messages():
	return render_template("partials/messages.html")


@main.route("/latest")
def latest():
	latest_updates = [
		"Server running normally",
		"3 new employees added",
		"Backup completed successfully"
	]

	return render_template(
		"partials/latest.html",
		updates=latest_updates
	)


@main.route("/employees")
def get_employees():
	query = request.args.get("query", "").lower()
	sort = request.args.get("sort", "id")
	page = int(request.args.get("page", 1))
	per_page = 5

	filtered_employees = []
	for employee in employees:
		name_match = query in employee["name"].lower()
		department_match = query in employee["department"].lower()
		if name_match or department_match:
			filtered_employees.append(employee)

	filtered_employees.sort(key=lambda employee: employee[sort])

	start = (page - 1) * per_page
	end = start + per_page
	paginated_employees = filtered_employees[start:end]
	total_pages = (len(filtered_employees) + per_page - 1) // per_page

	return render_template(
		"partials/employees_table.html",
		employees=paginated_employees,
		sort=sort,
		query=query,
		page=page,
		total_pages=total_pages
	)


@main.route("/add-employee", methods=["POST"])
def add_employee():
	name = request.form.get("name")
	department = request.form.get("department")

	existing_employee = next(
		(
			employee
			for employee in employees
			if employee["name"].lower() == name.lower()
		),
		None
	)

	if existing_employee:
		flash(f"Employee '{name}' already exists.")
		return "", 200, {
			"HX-Trigger": "refresh-messages"
		}

	new_employee = {
		"id": len(employees) + 1,
		"name": name,
		"department": department
	}

	employees.append(new_employee)

	flash(f"Employee {name} added successfully.")

	response = f"""
		<p>
			Added employee:
			<strong>{name}</strong>
			({department})
		</p>
	"""

	return response, 200, {
		"HX-Trigger": "employee-added, refresh-messages"
	}


@main.route("/edit-employee/<int:id>")
def edit_employee(id):
	employee = next(
		(
			employee
			for employee in employees
			if employee["id"] == id
		),
		None
	)

	return render_template(
		"partials/edit_employee_row.html",
		employee=employee
	)


@main.route("/update-employee/<int:id>", methods=["PUT"])
def update_employee(id):
	employee = next(
		(
			employee
			for employee in employees
			if employee["id"] == id
		),
		None
	)

	employee["name"] = request.form.get("name")
	employee["department"] = request.form.get("department")

	return render_template(
		"partials/employee_row.html",
		employee=employee
	)


@main.route("/employee-row/<int:id>")
def employee_row(id):
	employee = next(
		(
			employee
			for employee in employees
			if employee["id"] == id
		),
		None
	)

	return render_template(
		"partials/employee_row.html",
		employee=employee
	)


@main.route("/employee-details/<int:id>")
def employee_details(id):
	employee = next(
		(
			employee
			for employee in employees
			if employee["id"] == id
		),
		None
	)

	return render_template(
		"partials/employee_details_modal.html",
		employee=employee
	)


@main.route("/close-modal")
def close_modal():
	return ""


@main.route("/delete-employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
	global employees

	employees = [
		employee
		for employee in employees
		if employee["id"] != id
	]

	return ""


@main.route("/upload-file", methods=["POST"])
@login_required
def upload_file():
	file = request.files.get("file")

	if not file or file.filename == "":
		return render_template("partials/upload_result.html", error="No file selected.")

	if not allowed_file(file.filename):
		return render_template(
			"partials/upload_result.html",
			error=f"File type not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}."
		)

	filename = secure_filename(file.filename)
	save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
	file.save(save_path)

	return render_template("partials/upload_result.html", filename=filename)
