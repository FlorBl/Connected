document.addEventListener('DOMContentLoaded', function(){
var allUsers2 = document.getElementById('searchUsersss');
const element2 = document.getElementById("searchUsers222");
var value2;
$("#searchUsersss").on("keyup", function() { value2 = $(this).val();})

var newArrayy = [];
var newerArray = [];

const quantity2 = 5;

allUsers2.onkeyup = function(){
        fetch('/jsonresponse2/u')
        .then(response => response.json())
        .then(data => {
        const users = data;
        


        var x;
        for (var x = 0; x < users['suggestions'].length; x++) {
        var thisUser;
        thisUser = users['suggestions'][x].username;
        //console.log(`Username is: ${thisUser}`);
        var User = {
            'user': users['suggestions'][x].username,
            'profile' :users['suggestions'][x].profile_image,
            'bio': users['suggestions'][x].bio,
            'id': users['suggestions'][x].id,
            }

            newArrayy.push(User);
    }
})
    // str = JSON.stringify(newArrayy, null, 4); // (Optional) beautiful indented output.
     //console.log(str); // Displays output using window.alert()

    for(let i = 0; i < newArrayy.length; i++){
        newerArray.push(newArrayy[i].user)
    }

   // str2 = JSON.stringify(newerArray, null, 4)
    // console.log(str2); // Displays output using window.alert()

}



    $("#searchUsersss").on("keyup", function() {
      // call this function by passing user input
    
      filterResults2($(this).val());
    })


  function filterResults2(value2){
     element2.innerHTML = "";     

     let newValues = [];     


     const result = newerArray.filter(item => item.toLowerCase().indexOf(value2) > -1);

     if (value2 === '' || !result.length) {
          newValues = [];
      }

      for (let i = 0; i < result.length; i++) {
        newValues.push(result[i]);
      }
      
      if(value2 === '' || !newValues.length) {
          element2.innerHTML = "";        
          return;
       }
       
      // Gets 5 last elements of array
      var filterResult = (newValues.slice((newValues.length - 2), newValues.length));

      // Removes all duplicatess
      let uniqueElement = [...new Set(filterResult)];
    

      for (const username of uniqueElement) { 
        
        let addUser = newArrayy.find(person => person.user === username);

        element2.innerHTML += `
        <div class="demo">
                        <a href="/profile/${addUser.user}">
                        <span><img class="suggestionPic"  src="/media/${addUser.profile}"></span>
                        <span class="middle"><strong>${addUser.user}</strong><br> <p style="padding-left:8px;">@${addUser.user}</p></span>
                        <span>
                        </a>
                            <button class="btnS" onclick="callThis();" id="btnSuggestions" data-id="${addUser.id}" type="button"  style="background-color:rgb(15,20,25);float:right;color:whitesmoke;font-weight:bold;padding:3px 15px;border-radius:50px;">Follow</button>
                            
                        </span>
                        </div>`
        
      }
  }
});


