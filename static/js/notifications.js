async function loadNotifications() {
    const response = await fetch("/api/notifications");
    const notifications = await response.json();

    const table = document.getElementById("notificationTable");
    table.innerHTML = "";

    notifications.forEach(item => {
        table.innerHTML += `
            <tr>
                <td>${item.id}</td>
                <td>${item.message}</td>
                <td>${item.is_read === 1 ? "Read" : "Unread"}</td>
                <td>${item.created_at}</td>
                <td>
                    <button onclick="markRead(${item.id})">
                        Mark Read
                    </button>
                </td>
            </tr>
        `;
    });
}

async function markRead(id) {
    await fetch(`/api/notifications/${id}/read`, {
        method: "PUT"
    });

    loadNotifications();
}

loadNotifications();