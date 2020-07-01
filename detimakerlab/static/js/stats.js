const recent_reqs = document.querySelector(".recentReqs > ul");
const current_projs = document.querySelector(".currentProj > ul");

function formatDate(date, beginning, end)
{
    var newDate = new Date(date);
    newDate = new Date(newDate).toString();
    newDate = newDate.split(' ').slice(beginning, end).join(' ');
    return newDate;
}

function getStatData()
{
    const request = new XMLHttpRequest;
    request.open('GET', 'http://localhost:8000/tech/stats/');
    
    request.onload = () =>
    {
        try
        {
            const data = JSON.parse(request.responseText);
            populateRecentReqs(data);
            populateCurrProjs(data);
            // populateTable(data);
        }
        catch(e)
        {
            console.warn('Could not load JSON data: ' + e);
        }
    }
    request.send();
}

function populateRecentReqs(json)
{
    const latestReqsData = json['latestRequests'];

    while(recent_reqs.firstChild)
    {
        recent_reqs.removeChild(recent_reqs.firstChild);
    }

    for(var i in latestReqs)
    {
        const li = document.createElement('li');
        li.innerHTML = '<span>' + latestReqsData[i].projectThatRequested + '</span>' +
                        'Time : ' + formatDate(latestReqsData[i].timestamp, 4, 5);
        recent_reqs.appendChild(li);
    }
}

function populateCurrProjs(json)
{
    const projectsData = json['projects'];

    while(current_projs.firstChild)
    {
        current_projs.removeChild(current_projs.firstChild);
    }
    
    for(var i in projectsData)
    {
        const li = document.createElement('li');
        li.innerHTML = '<span>' + projectsData[i].name + '</span>' +
                        'Semester : ' + projectsData[i].semester;
        current_projs.appendChild(li);
    }
}

document.addEventListener('DOMContentLoaded', () => { getStatData(); });