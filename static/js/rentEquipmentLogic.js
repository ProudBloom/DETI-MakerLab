const rent_table = document.querySelector("#tab1 > tbody");
const projectSelection = document.getElementById('project-selectbox');

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
            selectProjectLogic();
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
        let qty = object.total_items - object.borrowed_items;
        if(object.broken == 'yes')
        {
            object.broken = 'Broken';
        }
        else
        {
            object.broken = 'Intact';
        }

        const tr = document.createElement("tr");
        tr.innerHTML = "<td data-label=\"Check\"><input type=\"checkbox\" class=\"checkbox\" value=\"" + object.ref + "\"></td>" +
                        "<td data-label=\"#ID\">" + object.ref + "</td>" +
                        "<td data-label=\"Family\">" + object.family + "</td>" +
                        "<td data-label=\"Desc\">" + object.description + "</td>" +
                        "<td data-label=\"Stock\">" + qty + "</td>" +
                        "<td data-label=\"Status\">" + object.broken + "</td>" + 
                        "<td><button class=\"showDialogBtt\" onclick=\"showDialog(" + object.ref + ")\">Show</button></td>";
        rent_table.append(tr);
    });
}

function rentCheckedItems()
{
    var checkboxes = document.getElementsByClassName('checkbox');

    let projectID = projectSelection.options[projectSelection.selectedIndex].value;

    for(i=0; i < checkboxes.length; i++)
    {
        if(checkboxes[i].checked == true)
        {
            rentItem(checkboxes[i].value, projectID);
        }
    }
}

function rentItem(itemID, projectID)
{
    console.log('Rented item ID : ' + itemID);
    console.log('Id of the selected project : ' + projectID);

    const request = new XMLHttpRequest;
    var response = confirm("Create a request for selected item?");
        if (response == true)
        {
            console.log("Request created");
            request.open('POST', createRequestURL + '/');
            request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            request.send("equipment_ref=" + itemID + "&project_ref=" + projectID);
            location.reload();
        }
        else
        {
            console.log("Canceled");
        }
}

function selectProjectLogic()
{
    const request = new XMLHttpRequest;
    request.open('GET', getProjectsURL);

    request.onload = () =>
    {
        const data = JSON.parse(request.responseText);
        populateProjects(data);
    }

    request.send();
}

function populateProjects(projectsData)
{
    while(projectSelection.firstChild)
    {
        projectSelection.removeChild(projectSelection.firstChild);
    }

    projectsData.forEach( (object) =>
    {
        const option = document.createElement("option");
        option.value = object.code;
        option.innerText = object.short_name;
        projectSelection.append(option);
    });
}


document.addEventListener('DOMContentLoaded', () => { loadEquipments(); });