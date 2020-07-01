
document.getElementById('add_equipment_form').addEventListener('submit', addEquipment);

function addEquipment(){
    const xhr = new XMLHttpRequest();
    var data = {
        family: document.getElementById('equipment_family').value,
        ref: document.getElementById('n_ref').value,
        description: document.getElementById('equipment_description').value,
        location: document.getElementById('equipment_location').value,
        total_items: document.getElementById('total_quantity').value,
        borrowed_items: document.getElementById('borrowed_quantity').value,
        price: document.getElementById('price').value
    }

    var family = document.getElementById('equipment_family').value;
    var ref = document.getElementById('n_ref').value;
    var description = document.getElementById('equipment_description').value;
    var location = document.getElementById('equipment_location').value;
    var total_items = document.getElementById('total_quantity').value;
    var borrowed_items = document.getElementById('borrowed_quantity').value;
    var price = document.getElementById('price').value;
    
    xhr.open('POST', getEquipmentsURL);

    if(data){
         xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }

    xhr.send('ref=' + ref + '&family=' + family + '&description=' + description + '&location=' + location + '&total_items=' + total_items + '&borrowed_items=' + borrowed_items + '&price=' + price);
}