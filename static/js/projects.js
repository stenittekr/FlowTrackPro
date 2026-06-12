async function loadProjects() {

    const response =
        await fetch("/api/projects");

    const projects =
        await response.json();

    const table =
        document.getElementById(
            "projectTable"
        );

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


async function createProject() {

    const name =
        document.getElementById(
            "projectName"
        ).value;

    const description =
        document.getElementById(
            "projectDescription"
        ).value;

    if (!name.trim()) {

        alert(
            "Please enter project name"
        );

        return;
    }

    const response =
        await fetch(
            "/api/projects",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    description: description
                })
            }
        );

    if (response.status === 403) {

        alert(
            "Access denied"
        );

        return;
    }

    document.getElementById(
        "projectName"
    ).value = "";

    document.getElementById(
        "projectDescription"
    ).value = "";

    loadProjects();
}

loadProjects();