const pending_request_table = document.querySelector("#tab1 > tbody");
const history_request_table = document.querySelector("#tab2 > tbody");


function loadRequests()
{
    const request = new XMLHttpRequest();

    request.open("get", "http://localhost:8000/tech/requests/?format=json");
    request.onload = () =>
    {   
        try
        {
            const data = JSON.parse(request.responseText);
            populateRequests(data);
        }
        catch(e)
        {
            console.warn("Could not load JSON data : " + e);
        }
    };
    request.send();
}

function populateRequests(json)
{

    //Clears dummy data from table
    while(pending_request_table.firstChild)
    {
        pending_request_table.removeChild(pending_request_table.firstChild);
    }
    while(history_request_table.firstChild)
    {
        history_request_table.removeChild(history_request_table.firstChild);
    }
    
    //Populate
    for(var i in json)
    {
        var date = new Date(json[i].timestamp);
        date = new Date(date).toString();
        date = date.split(' ').slice(0, 5).join(' ');

        const tr = document.createElement("tr");
        tr.innerHTML =  "<td>" + json[i].id + "</td>" +
                        "<td>" + json[i].equipment_ref.family + "</td>" +
                        "<td>" + json[i].project_ref.short_name + "</td>" +
                        "<td>" + date + "</td>"

        if(json[i].status == "pending")
        {
            const td = document.createElement("td");
            td.innerHTML =  "<td>" +
                            "<button class=\"acceptReq\">&#10003</button>" +
                            "<button class=\"denyReq\">&#10008</button>" +
                            "</td>"
            tr.append(td);
            pending_request_table.append(tr);
        }
        else
        {
            const td = document.createElement("td");
            td.innerHTML =  "<td>" + json[i].status + "</td>"
            tr.append(td);
            history_request_table.append(tr);
            
            if(json[i].status == 'approved')
            {
                tr.style.backgroundColor = 'rgba(127, 255, 128, 0.6)';
            }
            else
            {
                tr.style.backgroundColor = 'rgba(247, 93, 124, 0.6)';
            }
        }
    };
}
document.addEventListener("DOMContentLoaded", () => { loadRequests(); });


    var accButtons = document.getElementsByClassName('acceptReq');
    
    console.log(accButtons);
    //Wyrzuca całą kolekcję dobrze
    //Ni chuj nie da się przez nią iterować (DOM nie do końca załadowany?) STACK!

function archiveRequest()
{
    console.log(accButtons);
}