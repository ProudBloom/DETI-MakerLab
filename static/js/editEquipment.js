const edit_eq_table = document.querySelector("#tab1 > tbody");

function loadEquipments()
{
    const xhr = new XMLHttpRequest();

    xhr.open('GET', getEquipmentsURL + '?format=json');
    xhr.onload = () =>
    {
        try
        {
            const data = JSON.parse(xhr.responseText);
            populateEquipments(data);
        }
        catch(e)
        {
            console.warn('Could not load JSON data')
        }
    };
    xhr.send();
}

function populateEquipments(json)
{
    //Clears dummy data from table
    while(edit_eq_table.firstChild)
    {
        edit_eq_table.removeChild(edit_eq_table.firstChild);
    }

    //Populate
    for(var i in json)
    {
        let status = '';
        if(json[i].broken == 'yes')
        {
            json[i].broken = 'Broken';
        }
        else
        {
            json[i].broken = 'Intact';
        }

        const tr = document.createElement("tr");
        tr.innerHTML = 
                        "<td data-label=\"#ID\">" + json[i].ref + "</td>" +
                        "<td data-label=\"Family\">" + json[i].family + "</td>" +
                        "<td data-label=\"Desc\">" + json[i].description + "</td>" +
                        "<td data-label=\"Stock\">" + json[i].total_items + "</td>" +
                        "<td data-label=\"Status\">" + json[i].broken + "</td>"+
                        "<td data-label=\"Edit\">" + "<button class='editeq' onclick=editEq(" + json[i].ref + ")>&#9998</button>" + "</td>" +
                        "<td data-label=\"Delete\">" + "<button class='deleteeq' onclick=deleteEq(" + json[i].ref + ")>&#10006</button>" + "</td>";
        edit_eq_table.append(tr);
    }
}

function editEq(ref){
    
   window.open("https://makerlab2020.herokuapp.com/tech/admin/technician_api/equipments/" + ref + "/change/")
    
}

function deleteEq(ref){
    const xhr = new XMLHttpRequest();
    xhr.open('DELETE', getEquipmentsURL + ref + '/');
    var response = confirm("Delete selected equipment?");

    if(response)
    {
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        xhr.send();
        location.reload();
    }
}


document.addEventListener('DOMContentLoaded', () => { loadEquipments(); });