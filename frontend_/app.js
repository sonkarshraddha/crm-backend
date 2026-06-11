const API_URL = "https://crm-backend-1-ohag.onrender.com";


// CREATE TICKET
async function createTicket() {

    const customer_name =
        document.getElementById("name").value.trim();

    const customer_email =
        document.getElementById("email").value.trim();

    const subject =
        document.getElementById("subject").value.trim();

    const description =
        document.getElementById("desc").value.trim();


    if (
        !customer_name ||
        !customer_email ||
        !subject ||
        !description
    ) {
        alert("Please fill all fields");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/api/tickets`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    customer_name,
                    customer_email,
                    subject,
                    description
                })
            }
        );

        const data = await response.json();

        alert(`Ticket Created: ${data.ticket_id}`);

        // CLEAR FORM
        document.getElementById("name").value = "";
        document.getElementById("email").value = "";
        document.getElementById("subject").value = "";
        document.getElementById("desc").value = "";

        loadTickets();

    } catch (error) {
        console.log(error);
        alert("Failed to create ticket");
    }
}



// UPDATE STATUS
async function updateStatus(ticketId, status) {

    try {

        await fetch(
            `${API_URL}/api/tickets/${ticketId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    status: status,
                    notes: ""
                })
            }
        );

        loadTickets();

    } catch (error) {
        console.log(error);
        alert("Failed to update status");
    }
}



// LOAD TICKETS
async function loadTickets() {

    try {

        const response =
            await fetch(`${API_URL}/api/tickets`);

        const tickets =
            await response.json();


        const searchText =
            document.getElementById("searchBox")
            .value
            .toLowerCase()
            .trim();


        const selectedStatus =
            document.getElementById("statusFilter")
            .value;


        const filteredTickets =
            tickets.filter(ticket => {

                const matchesSearch =

                    ticket.customer_name
                    .toLowerCase()
                    .includes(searchText)

                    ||

                    ticket.subject
                    .toLowerCase()
                    .includes(searchText)

                    ||

                    ticket.ticket_id
                    .toLowerCase()
                    .includes(searchText);


                const matchesStatus =

                    selectedStatus === ""

                    ||

                    ticket.status === selectedStatus;


                return (
                    matchesSearch &&
                    matchesStatus
                );
            });


        const ticketsDiv =
            document.getElementById("tickets");

        ticketsDiv.innerHTML = "";


        if (filteredTickets.length === 0) {

            ticketsDiv.innerHTML =
                `<p>No tickets found</p>`;

            return;
        }


        filteredTickets.forEach(ticket => {

            ticketsDiv.innerHTML += `

            <div class="bg-white rounded-xl shadow p-4">

                <div class="flex justify-between items-center mb-3">

                    <h3 class="font-bold text-2xl">
                        ${ticket.ticket_id}
                    </h3>

                    <select
                        onchange="updateStatus('${ticket.ticket_id}', this.value)"
                        class="border rounded px-2 py-1">

                        <option value="Open"
                        ${ticket.status === "Open" ? "selected" : ""}>
                        Open
                        </option>

                        <option value="In Progress"
                        ${ticket.status === "In Progress" ? "selected" : ""}>
                        In Progress
                        </option>

                        <option value="Closed"
                        ${ticket.status === "Closed" ? "selected" : ""}>
                        Closed
                        </option>

                    </select>

                </div>

                <p>
                    <strong>Name:</strong>
                    ${ticket.customer_name}
                </p>

                <p>
                    <strong>Email:</strong>
                    ${ticket.customer_email}
                </p>

                <p>
                    <strong>Subject:</strong>
                    ${ticket.subject}
                </p>

                <p>
                    <strong>Description:</strong>
                    ${ticket.description}
                </p>

                <p class="mt-2">
                    <strong>Status:</strong>
                    ${ticket.status}
                </p>

            </div>
            `;
        });

    } catch (error) {
        console.log(error);
    }
}



// PAGE LOAD
loadTickets();