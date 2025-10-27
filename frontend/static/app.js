const form = document.getElementById("enumeration-form")
const targetWebsite = document.getElementById("target-website-input")
const resultsContainer = document.getElementById("results")

function tableCreate(responseData) {
    const body = document.body,
    tbl = document.createElement('table');
    tbl.classList.add("results-table");

    responseData.forEach(function (response) {
        const tr = tbl.insertRow();
        let fieldNames = Object.keys(response);
        fieldNames.forEach(function (fieldName) {
            const td = tr.insertCell();
            td.appendChild(document.createTextNode(`${fieldName}: ${response[fieldName]}`));
        })
        
    })
    body.appendChild(tbl);
    }


form.addEventListener("submit", async function (event) {
    resultsContainer.innerHTML = ""
    event.preventDefault();
    const targetHost = document.getElementById("target-website-input").value;
    console.log(`Target Website: ${targetHost}`);
    
    const url = "http://localhost:8000/enumerate"
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({target_host: targetHost})
        }).then(res => res.json())
        .then(data => {
            tableCreate(data);
        })
    } catch (error) {
        console.error("Failed to enumerate website")
    }
}
);
