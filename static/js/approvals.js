async function loadApprovals() {
    const response = await fetch("/api/approvals");

    if (response.status === 403) {
        alert("Access denied.");
        return;
    }

    const approvals = await response.json();
    const table = document.getElementById("approvalTable");

    table.innerHTML = "";

    approvals.forEach(item => {
        table.innerHTML += `
            <tr>
                <td>${item.id}</td>
                <td>${item.task_id}</td>
                <td>${item.requested_by}</td>
                <td>${item.status}</td>
                <td>${item.created_at}</td>
                <td>
                    <button onclick="approveRequest(${item.id})">
                        Approve
                    </button>
                </td>
            </tr>
        `;
    });
}

async function approveRequest(id) {
    const response = await fetch(`/api/approvals/${id}/approve`, {
        method: "POST"
    });

    const result = await response.json();
    alert(result.message || result.error);

    loadApprovals();
}

loadApprovals();