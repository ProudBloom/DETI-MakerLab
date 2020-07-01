const recent_reqs = document.querySelector(".recentReqs > ul");
const current_projs = document.querySelector(".currentProj > ul");
const popular_table = document.querySelector(".statTable > tbody");

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
    request.open('GET', getStatsURL);
    
    request.onload = () =>
    {
        try
        {
            const data = JSON.parse(request.responseText);
            populateRecentReqs(data);
            populateCurrProjs(data);
            populatePopularEqs(data);
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

    for(var i in latestReqsData)
    {
        const li = document.createElement('li');

        li.innerHTML = '<span>' + latestReqsData[i].projectThatRequested + '</span>' +
                        ' | Time : ' + formatDate(latestReqsData[i].timestamp, 4, 5);
        recent_reqs.appendChild(li);
    }
}

function populateCurrProjs(json)
{
    const projectsData = json['projects'];
    const more = document.createElement('a');

    while(current_projs.firstChild)
    {
        current_projs.removeChild(current_projs.firstChild);
    }
    
    for(var i in projectsData)
    {
        if(i <= 3)
        {
            const li = document.createElement('li');

            li.innerHTML = '<span>' + projectsData[i].name + '</span>' +
                            ' | Semester : ' + projectsData[i].semester;
            current_projs.appendChild(li);
        }
        else
        {
            let counter = i - 3;
            console.log(counter);
            more.innerHTML = '<a class="moreProjects" href="tech/admin/technician_api/project/">' + counter + ' more open projects' + '</a>';
            current_projs.appendChild(more);
        }
    }
}

function populatePopularEqs(json)
{
    const popularEqs = json['popularRequests'];

    while(popular_table.firstChild)
    {
        popular_table.removeChild(popular_table.firstChild);
    }

    for(var i in popularEqs)
    {
        if(i <= 5)
        {
            const tr = document.createElement("tr");

            tr.innerHTML = "<td>" + popularEqs[i].family + "</td>" +
                            "<td>" + popularEqs[i].description + "</td>" +
                            "<td>" + popularEqs[i].TimesRequested + "</td>";
            popular_table.append(tr);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => { getStatData(); });