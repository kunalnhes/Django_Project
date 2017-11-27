/*
//method 1
function myFunct(){
    alert("Button is clicked");
}
//Method 2
//select the element using selector API

var b = document.querySelector('#btn');

// add event listener to the selected element
b.addEventListener('click',function (evt){
alert("Button is clicked");
});

*/

function likeThisPost(element){
    //get post id of the current post
    var postId = element.querySelector('[name=post]').value;
    //send a ajax request to server
    var likeCount = element.querySelector('[name=likeCount]').innerHTML;
    var likeBtn = element.querySelector('[name=like]').innerHTML;


    $.ajax({
        url: "/like/",
        type: "POST",
        dataType: "json",
        data: {
         post_id: postId
        },
        success: function(result){
            //This function executes when request is successful
            if (result.flag){
                //like is successful
                //increment the like counter
                likeCount++;
                element.querySelector('[name=likeCount]').innerHTML = likeCount;
                //change the style of like button
                likeBtn.style.backgroundColor = "blue"
                likeBtn.style.color = "white"

            }else{
                //unlike is successful
                //decrement the like counter/
                likeCount--;
                element.querySelector('[name=likeCount]').innerHTML = likeCount;
                likeBtn.style.backgroundColor = "white"
                likeBtn.style.color = "black"
            }

        },
        error: function(result){
            //This function executes when request is failed
            alert("Request failed");
        },
    });
}