const my_projects_table = document.querySelector("#table1 > tbody");

function loadProjects()
{
    const request = new XMLHttpRequest();

    request.open('GET', getProjectsURL + '?format=json');
    request.onload = () =>
    {
        try
        {
            const data = JSON.parse(request.responseText);
            populateProjects(data);
        }
        catch(e)
        {
            console.warn('Could not load JSON data')
        }
    };
    request.send();
}

function populateProjects(json)
{
    //Clears dummy data from table
    while(my_projects_table.firstChild)
    {
        my_projects_table.removeChild(my_projects_table.firstChild);
    }

    //Populate
    json.forEach( (object) =>
    {
        
        const tr = document.createElement("tr");
        tr.innerHTML = 
                        "<td data-label=\"Code\">" + object.code + "</td>" +
                        "<td data-label=\"Short Name\">" + object.short_name + "</td>" +
                        "<td data-label=\"Name\">" + object.name + "</td>" +
                        "<td data-label=\"Year\">" + object.year + "</td>";
        my_projects_table.append(tr);
    });
}

document.addEventListener('DOMContentLoaded', () => { loadProjects(); });