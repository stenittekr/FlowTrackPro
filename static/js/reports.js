async function loadReports() {

    const response =
        await fetch("/api/reports");

    const data =
        await response.json();

    document.getElementById(
        "totalTasks"
    ).textContent =
        data.total_tasks;

    document.getElementById(
        "totalProjects"
    ).textContent =
        data.total_projects;

    document.getElementById(
        "completedTasks"
    ).textContent =
        data.completed_tasks;

    document.getElementById(
        "backlogTasks"
    ).textContent =
        data.backlog_tasks;
}

loadReports();