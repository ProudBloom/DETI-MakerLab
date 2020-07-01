function showDialog(equipmentID)
{
    document.querySelector('.bg-modal').style.display = 'flex';
    document.querySelector('#rentBtt').style.display='none';
    
    const request = new XMLHttpRequest();
    request.open('GET', getEquipmentsURL + equipmentID);
    request.onload = () =>
    {
        try
        {
            const data = JSON.parse(request.responseText);
            displayEqData(data);
        }
        catch(e)
        {
            console.warn('Could not load JSON data')
        }
    };
    request.send();
}

function closeDialog()
{
    document.querySelector('.bg-modal').style.display = 'none';
    document.querySelector('#rentBtt').style.display='block';
}

function displayEqData(json)
{
    let content = document.querySelector('.modal-content > .data');

    while(content.firstChild)
    {
        content.removeChild(content.firstChild);
    }

    const image = document.createElement('img');
        image.src = json.image_file;

    const family = document.createElement('p');
    const description = document.createElement('p');
    const totalItems = document.createElement('p');
    const status = document.createElement('p');
    const price = document.createElement('p');

    json.status == "dis" ? json.status = "Available" : json.status = "Not available";

    family.innerText = "Family: " + json.family;
    description.innerText = "Full description: " + json.description;
    totalItems.innerText = "Items total: " + json.total_items;
    status.innerText = "Status: " + json.status;
    price.innerText = "Price: " + json.price + "€";

    content.appendChild(image);
    content.appendChild(family);
    content.appendChild(description);
    content.appendChild(totalItems);
    content.appendChild(status);
    content.appendChild(price);
}
