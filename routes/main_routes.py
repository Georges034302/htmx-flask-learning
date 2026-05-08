import time
from flask import Blueprint, render_template, request

from data.mock import employees

main = Blueprint("main", __name__)


@main.route("/")
def home():
	return render_template("index.html")


@main.route("/hello")
def hello():
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
	return render_template(
		"partials/employees_table.html",
		employees=employees
	)


@main.route("/add-employee", methods=["POST"])
def add_employee():
	name = request.form.get("name")
	department = request.form.get("department")

	new_employee = {
		"id": len(employees) + 1,
		"name": name,
		"department": department
	}

	employees.append(new_employee)

	response = f"""
		<p>
			Added employee:
			<strong>{name}</strong>
			({department})
		</p>
	"""

	return response, 200, {
		"HX-Trigger": "employee-added"
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


@main.route("/delete-employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
	global employees

	employees = [
		employee
		for employee in employees
		if employee["id"] != id
	]

	return ""
