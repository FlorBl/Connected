// Shows a list of users, matching or similar to the input typed.
var allUsers = document.getElementById('searchUsers');
const element = document.getElementById("searchUsers2");
var value;
$("#searchUsers").on("keyup", function() { value = $(this).val();})

var newArray = [];
const quantity = 5;

allUsers.onclick = function(){
        fetch('/allUsers')
        .then(response => response.json())
        .then(data => {
        const users = data['UsersInfo'];
        


        
        for(let i = 0;i < users.length; i++){
         newArray.push(users[i]);  
        }



})

}

    


    $("#searchUsers").on("keyup", function() {
      // call this function by passing user input
      filterResults($(this).val())
    })


  function filterResults(value){
     element.innerHTML = "";     
     let newValues = [];     
     const result = newArray.filter(item => item.toLowerCase().indexOf(value) > -1);
     
     if (value === '' || !result.length) {
          newValues = [];
      }

      for (let i = 0; i < result.length; i++) {
        newValues.push(result[i]);
      }
      
      if(value === '' || !newValues.length) {
          element.innerHTML = "";        
          return;
       }
       
      // Gets 5 last elements of array
      var filterResult = (newValues.slice((newValues.length - 5), newValues.length));

      // Removes all duplicatess
      let uniqueElement = [...new Set(filterResult)];
    

      for (const user of uniqueElement) {       
        element.innerHTML += `<li class="li-User" ><a href="/profile/${user}">${user}</a></li>`;

      }
  }


