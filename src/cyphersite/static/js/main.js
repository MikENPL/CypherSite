const selector = document.getElementById("function-select");
const forms = document.querySelectorAll(".function");

if (forms.length > 1) {
    selector.classList.toggle("active")
}
function showForm() {
    forms.forEach(form => {
        form.classList.toggle("active", form.id === selector.value);
    });
    const oldTable = document.getElementById("results-table");

    if (oldTable) {
        oldTable.remove();
    }
}

selector.addEventListener("change", showForm);

// Show the first form on page load
showForm();

document.querySelectorAll("form.function").forEach(form => {
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const response = await fetch(form.action, {
            method: "POST",
            body: new FormData(form)
        });

        const data = await response.json();

        if (typeof(data.result) === "object") {
            const table = document.createElement("table")
            for (const [key, value] of Object.entries(data.result)){
                const row = document.createElement("tr");

                const th = document.createElement("th");
                th.textContent = key;

                const td = document.createElement("td");
                td.textContent = value;

                row.appendChild(th);
                row.appendChild(td);
                table.appendChild(row);
            }
            const oldTable = document.getElementById("results-table");
            if (oldTable) {
                oldTable.remove();
            }
            table.id = "results-table";
            document.getElementById("results").appendChild(table);
        } else {
            document.getElementById("result_highlight").textContent = data.result;
            document.getElementById("result").textContent = data.result_text;
        }
        // document.getElementById("result").textContent = JSON.stringify(data.result, null, 2);
    });
});