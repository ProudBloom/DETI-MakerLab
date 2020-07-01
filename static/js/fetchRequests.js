const pending_request_table = document.querySelector("#tab1 > tbody");
const history_request_table = document.querySelector("#tab2 > tbody");
const pendingRequestsCounter = document.querySelector('.pendingRequestsText');

function loadRequests()
{
    const request = new XMLHttpRequest();

    request.open("get", getRequetsURL + "?format=json");
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
    const request_amount = document.createElement('p');
    let counter = 0;

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
            //Convert timestamp to normal date format
            var date = new Date(json[i].timestamp);
            date = new Date(date).toString();
            date = date.split(' ').slice(0, 5).join(' ');

            //For each object, create table row and cells
            const tr = document.createElement("tr");
            tr.innerHTML =  "<td>" + json[i].id + "</td>" +
                            "<td>" + '[' + json[i].equipment_ref.family + '] ' + json[i].equipment_ref.description + "</td>" +
                            "<td>" + json[i].project_ref.short_name + "</td>" +
                            "<td>" + date + "</td>"

            //If request is pending add it to the 1st table, and add buttons
            if(json[i].status == "pending")
            {
                counter ++;
                request_amount.innerHTML = '<span class="requestAmount">Total : ' + counter + '</span>';
                pendingRequestsCounter.append(request_amount);

                const td = document.createElement("td");
                td.innerHTML =  "<td>" +
                                "<button class='acceptReq' onclick=archiveRequestAccept(" + json[i].id + ");updateStock(" + json[i].equipment_ref.ref + ");>&#10003</button>" +
                                "<button class='denyReq' onclick=archiveRequestDeny(" + json[i].id + ")>&#10008</button>" +
                                "</td>"
                tr.append(td);
                pending_request_table.append(tr);
            }
            //Else add to 2nd table
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
        }
}

function archiveRequestAccept(id)
{
    const request = new XMLHttpRequest;
    var response = confirm("Approve the request?");
        if (response == true) 
        {
            console.log("Approved");
            request.open('PUT', approveRequetsURL + id + '/');
            request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            request.send();
            location.reload();
        } 
        else
        {
            console.log("Canceled");
        }
    
}

function updateStock(equipmentReference) {
    const request = new XMLHttpRequest();
    console.log("CALLED");
    console.log(equipmentReference.toString());
    var response = confirm("Update stock?");
        if (response == true)
        {
            request.open('PATCH', borrowEquipmentURL + equipmentReference + '/');
            request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            request.send();
            location.reload();
            console.log("Stock updated");
        }
        else
        {
            console.log("Canceled");
        }
}

function archiveRequestDeny(id)
{
    const request = new XMLHttpRequest;
    var response = confirm("Are you sure to deny the request?");
        if (response == true) 
        {
            console.log("Denied");
            request.open('PUT', denyRequetsURL + id + '/');
            request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            request.send();
            location.reload();
        } 
        else
        {
            console.log("Canceled");
        }
}

document.addEventListener("DOMContentLoaded", () => { loadRequests(); });