const rent_table = document.querySelector("#tab1 > tbody");

function loadEquipments()
{
    const request = new XMLHttpRequest();

    request.open('GET', 'http://localhost:8080/tech/equipments/?format=json');
    request.onload = () =>
    {
        try
        {
            const data = JSON.parse(request.responseText);
            populateEquipments(data);
        }
        catch(e)
        {
            console.warn('Could not load JSON data')
        }
    };
    request.send();
}

function populateEquipments(json)
{
    //Clears dummy data from table
    while(rent_table.firstChild)
    {
        rent_table.removeChild(rent_table.firstChild);
    }

    //Populate
    json.forEach( (object) =>
    {
        let status = '';
        if(object.broken == 'yes')
        {
            object.broken = 'Broken';
        }
        else
        {
            object.broken = 'Intact';
        }

        const tr = document.createElement("tr");
        tr.innerHTML = "<td data-label=\"Check\"><input type=\"checkbox\"></td>" +
                        "<td data-label=\"#ID\">" + object.ref + "</td>" +
                        "<td data-label=\"Family\">" + object.family + "</td>" +
                        "<td data-label=\"Desc\">" + object.description + "</td>" +
                        "<td data-label=\"Stock\">" + object.total_items + "</td>" +
                        "<td data-label=\"Status\">" + object.broken + "</td>";
        rent_table.append(tr);
    });
}

document.addEventListener('DOMContentLoaded', () => { loadEquipments(); });