async function loadUsers() {

    const response = await fetch("/api/users");
    const users = await response.json();

    console.log("Users:", users);

    const table = document.getElementById("userTable");

    console.log("Table:", table);

    table.innerHTML = "";

    users.forEach(user => {
        table.innerHTML += `
        <tr>
            <td>${user.id}</td>
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td>${user.role}</td>
        </tr>
        `;
    });
}

loadUsers();

loadUsers();
    const users = await response.json();

    const table =
        document.getElementById("userTable");

    table.innerHTML = "";

    users.forEach(user => {

        table.innerHTML += `
            <tr>
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>
    <select id="role-${user.id}">
        <option value="Admin" ${user.role === "Admin" ? "selected" : ""}>Admin</option>
        <option value="Manager" ${user.role === "Manager" ? "selected" : ""}>Manager</option>
        <option value="Developer" ${user.role === "Developer" ? "selected" : ""}>Developer</option>
        <option value="Viewer" ${user.role === "Viewer" ? "selected" : ""}>Viewer</option>
    </select>
</td>

<td>
    <button onclick="updateRole(${user.id})">
        Update
    </button>
</td>
            </tr>
        `;
    });

async function updateRole(userId) {

    const role =
        document.getElementById(
            `role-${userId}`
        ).value;

    const response =
        await fetch(
            `/api/users/${userId}/role`,
            {
                method: "PUT",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({
                    role: role
                })
            }
        );

    const result =
        await response.json();

    alert(result.message);

    loadUsers();
}
loadUsers();