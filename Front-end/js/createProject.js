function change() {
    var select = document.getElementById("no_team_members");
    var names = document.getElementById("names");
    var value = select.value;
        if (value == 1) {
            toAppend = `<input type='email' class='project_input' placeholder='Student e-mail' name='student1_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>`;  
            names.innerHTML=toAppend;
            return;
        }
        if (value == 2) {
            toAppend = `<input type='email' class='project_input' placeholder='Student e-mail' name='student1_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student2_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>`;
            names.innerHTML = toAppend; 
            return;
        }
        if (value == 3) {
            toAppend = `<input type='email' class='project_input' placeholder='Student e-mail' name='student1_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student2_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student3_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>`;
            names.innerHTML = toAppend;
            return;
        }
        if (value == 4) {
            toAppend = `<input type='email' class='project_input' placeholder='Student e-mail' name='student1_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student2_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student3_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student4_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>`;
            names.innerHTML = toAppend;
            return;

        }
        if (value == 5) {
            toAppend = `<input type='email' class='project_input' placeholder='Student e-mail' name='student1_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student2_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student3_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student4_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student5_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>`;
            names.innerHTML = toAppend;
            return;
        }
        if (value == 6) {
            toAppend = `<input type='email' class='project_input' placeholder='Student e-mail' name='student1_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student2_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student3_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student4_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student5_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>
            <input type='email' class='project_input' placeholder='Student e-mail' name='student6_name' pattern=".+@ua.pt" title="Use UA e-mail!" required>`;
            names.innerHTML = toAppend;
            return;
        }
}

