
document.getElementById('add_equipment_form').addEventListener('submit', addEquipment);

function addEquipment(){
    const xhr = new XMLHttpRequest();
    var data = 
    {
        family: document.getElementById('equipment_family').value,
        ref: 6,
        description: document.getElementById('equipment_description').value,
        location: document.getElementById('equipment_location').value,
        total_items: document.getElementById('total_quantity').value,
        borrowed_items: document.getElementById('borrowed_quantity').value,
        price: document.getElementById('price').value
    }
    
    xhr.open('POST', 'http://localhost:8000/tech/equipments/');

    if(data){
         xhr.setRequestHeader('Content-type', 'application/json');
    }
   
    xhr.onload = function(){
        console.log(this.responseText);
    }

    xhr.send(JSON.stringify(data));

}