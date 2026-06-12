async function loadUsers() {

    const response =
        await fetch("/api/users");

    const users =
        await response.json();

    const dropdown =
        document.getElementById("assignedUser");

    dropdown.innerHTML =
        '<option value="">Assign User</option>';

    users.forEach(user => {

        dropdown.innerHTML += `
            <option value="${user.id}">
                ${user.username}
                (${user.role})
            </option>
        `;
    });
}async function loadProjects() {
    const response = await fetch("/api/projects");
    const projects = await response.json();

    const table = document.getElementById("projectTable");
    table.innerHTML = "";

    projects.forEach(project => {
        table.innerHTML += `
            <tr>
                <td>${project.id}</td>
                <td>${project.name}</td>
                <td>${project.description}</td>
                <td>${project.status}</td>
            </tr>
        `;
    });
}
async function loadChart() {

    const response =
        await fetch("/api/dashboard");

    const data =
        await response.json();

    const ctx =
        document.getElementById(
            "taskChart"
        );

    new Chart(ctx, {

        type: "bar",

        data: {

            labels: [
                "Backlog",
                "In Progress",
                "Review",
                "Done"
            ],

            datasets: [{

                label: "Tasks",

                data: [
                    data["Backlog"],
                    data["In Progress"],
                    data["Review"],
                    data["Done"]
                ]
            }]
        }
    });
}

loadChart();
async function createProject() {
    const name = document.getElementById("projectName").value;
    const description = document.getElementById("projectDescription").value;

    if (!name.trim()) {
        alert("Please enter project name");
        return;
    }

    const response = await fetch("/api/projects", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            description: description
        })
    });

    if (response.status === 403) {
        alert("Access denied: only Admin or Manager can create projects.");
        return;
    }

    document.getElementById("projectName").value = "";
    document.getElementById("projectDescription").value = "";

    loadProjects();
}

loadProjects();
async function createTask() {

    const title =
    document.getElementById("taskTitle").value;

const priority =
    document.getElementById("taskPriority").value;

const assignedTo =
    document.getElementById("assignedUser").value;

const dueDate =
    document.getElementById("dueDate").value;

    await fetch("/api/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
    title: title,
    priority: priority,
    assigned_to: assignedTo,
    due_date: dueDate
})
    });
}