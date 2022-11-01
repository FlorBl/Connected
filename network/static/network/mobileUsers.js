// Connected to /mobile route, suggest an array of people to follow
document.addEventListener('DOMContentLoaded', function(){

var arrayUserInfo = [];
var arrayUsernames = [];
var inputValue;
var userInput = document.getElementById('userInput');
const userElement = document.getElementById("searchResults");
$("#userInput").on("keydown", function() { inputValue = $(this).val().toLowerCase();})


userInput.onkeydown = function(){
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

            arrayUserInfo.push(User);
    }
})
 

    for(let i = 0; i < arrayUserInfo.length; i++){
        arrayUsernames.push(arrayUserInfo[i].user)
    }

}



    $("#userInput").on("keydown", function() {
      // call this function by passing user input
    
      filterResults2($(this).val().toLowerCase());
    })


  function filterResults2(inputValue){
     userElement.innerHTML = "";     

     let newValues = [];     


     const result = arrayUsernames.filter(item => item.toLowerCase().indexOf(inputValue) > -1);

     if (inputValue === '' || !result.length) {
          newValues = [];
      }

      for (let i = 0; i < result.length; i++) {
        newValues.push(result[i]);
      }
      
      if(inputValue === '' || !newValues.length) {
          userElement.innerHTML = "";        
          return;
       }
       
      // Gets 5 last elements of array
      var filterResult = (newValues.slice((newValues.length - 10), newValues.length));

      // Removes all duplicatess
      let uniqueElement = [...new Set(filterResult)];
    

      for (const username of uniqueElement) { 
        
        let addUser = arrayUserInfo.find(person => person.user === username);
        const aws = 'https://django-greensky-bucket.s3.amazonaws.com/'
        var profileImage = `${aws}`+`${addUser.profile}`;
        userElement.innerHTML += `
        <a href="profile/${addUser.user}">
        <div class="demo" onmouseover="this.style.backgroundColor='#f7f9f9'" onmouseout="this.style.backgroundColor=''">
                        <span><img class="suggestionPic"  src="${profileImage}"></span>
                        <span class="middle"><strong>${addUser.user}</strong><br> <p style="padding-left:8px;">@${addUser.user}</p></span>
                        <span>
                            <button class="btnS" onclick="callThis();" id="btnSuggestions" data-id="${addUser.id}" type="button"  style="background-color:rgb(15,20,25);float:right;color:whitesmoke;font-weight:bold;padding:3px 15px;border-radius:50px;">Follow</button>
                            
                        </span>
                        </div>
                        </a>
                        `
        
      }
  }
});


