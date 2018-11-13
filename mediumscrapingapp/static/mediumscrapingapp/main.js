<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
function scrape_post() {
    //console.log("scrape post is working!") // sanity check
    $("#talk").empty();
    $.ajax({
        url : "home", // the endpoint
        type : "GET", // http method
        data : { txtSearch : $('#txtSearch').val()}, // data sent with the post request

        // handle a successful response
        
        success : function(json) {
            $("#talk").append("<a href='#'><li><strong>"+json.title+"</strong> , <em> "+json.author_name+"</em> , <span> "+json.details+"</span></li></a>");
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            console.log('error')
        }
    });
};