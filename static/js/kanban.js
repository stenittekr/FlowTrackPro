async function loadKanban() {
    const response = await fetch("/api/tasks");
    const tasks = await response.json();

    const columns = ["Backlog", "In Progress", "Review", "Done"];

    columns.forEach(status => {
        document.getElementById(status).innerHTML = "";
    });

    tasks.forEach(task => {
        const card = document.createElement("div");
        card.className = "kanban-task";

        card.innerHTML = `
            <h3>${task.title}</h3>
            <p>Priority: ${task.priority}</p>

            <select onchange="updateStatus(${task.id}, this.value)">
                <option value="Backlog" ${task.status === "Backlog" ? "selected" : ""}>Backlog</option>
                <option value="In Progress" ${task.status === "In Progress" ? "selected" : ""}>In Progress</option>
                <option value="Review" ${task.status === "Review" ? "selected" : ""}>Review</option>
                <option value="Done" ${task.status === "Done" ? "selected" : ""}>Done</option>
            </select>
        `;

        const column = document.getElementById(task.status);

        if (column) {
            column.appendChild(card);
        }
    });
}

async function updateStatus(id, status) {
    const response = await fetch(`/api/tasks/${id}/status`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ status: status })
    });

    if (response.status === 403) {
        alert("Access denied: your role cannot update task status.");
        loadKanban();
        return;
    }

    loadKanban();
}

loadKanban();