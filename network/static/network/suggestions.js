document.addEventListener('DOMContentLoaded', function () {


    if (document.getElementById("btnSuggestions")) {
        document.querySelectorAll('#btnSuggestions').forEach(e => e.addEventListener("click", function (event) {
            fetch(`/follow/${this.dataset.id}`)
                .then(response => response.json())
                .then(data => {
                    if (data.result == "follow") {
                        this.innerHTML = "Following";
                        var update = Number(document.getElementById('sp_following').innerHTML);
                        document.getElementById('sp_following').innerHTML = update + 1;

                    } else {
                        this.innerHTML = "Follow";
                        var update = Number(document.getElementById('sp_following').innerHTML);
                        document.getElementById('sp_following').innerHTML = update - 1;

                    }

                    
                });

        }))
    }

    
  
});


