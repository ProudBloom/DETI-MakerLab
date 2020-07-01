const return_table = document.querySelector("#tab1 > tbody");

function loadEquipments()
{
    const request = new XMLHttpRequest();

    request.open('GET', getEquipmentsURL);
    request.onload = () =>
    {
        try
        {
            const data = JSON.parse(request.responseText);
            populateEquipments(data);
        }
        catch(e)
        {
            console.warn('Could not load JSON data');
            console.warn(e);
        }
    };
    request.send();
}

function populateEquipments(json)
{
    //Clears dummy data from table
    while(return_table.firstChild)
    {
        return_table.removeChild(return_table.firstChild);
    }

    //Populate
    for(var i in json)
    {
        const tr = document.createElement("tr");
        tr.innerHTML = "<td data-label=\"Check\"><input type=\"checkbox\" class=\"checkbox\" value=\"" + json[i].ref + "\"></td>" +
                        "<td data-label=\"#ID\">" + json[i].ref + "</td>" +
                        "<td data-label=\"Family\">" + json[i].family + "</td>" +
                        "<td data-label=\"Desc\">" + json[i].description + "</td>" + 
                        "<td>" + json[i].borrowed_items + "</td>" + 
                        "<td><img src=\"" + json[i].image_file + "\"/></td>"
        return_table.append(tr);
    }
}

function returnCheckedItems()
{
    var checkboxes = document.getElementsByClassName('checkbox');

    for(i=0; i < checkboxes.length; i++)
    {
        if(checkboxes[i].checked == true)
        {
            returnItem(checkboxes[i].value);
        }
    }
}

function returnItem(id)
{
    const request = new XMLHttpRequest;
    var response = confirm("Return checked equipments?");
        if (response == true)
        {
            request.open('PATCH', returnEquipmentURL + id + '/');
            request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            request.send();
            location.reload();

            console.log('Request : ' + request.status);

            //Access data from the table (QTY) and give feedback when 0
        }
        else
        {
            console.log("Canceled");
        }
}

document.addEventListener('DOMContentLoaded', () => { loadEquipments(); });