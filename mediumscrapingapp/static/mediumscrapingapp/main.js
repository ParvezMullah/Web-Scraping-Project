var jQueryScript = document.createElement('script');  
jQueryScript.setAttribute('src','https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js');
document.head.appendChild(jQueryScript);


function scrape_post(i) {

    $.ajax({
        url : "get-posts", // the endpoint
        type : "GET", // http method
        data : { txtSearch : $('#txtSearch').val(), post_number: i}, // data sent with the post request
        // contentType: "application/json",
        async:false,
        // handle a successful response
        
        success : function(myobj) {
            if (myobj.post_title != "None"){

                document.getElementById(i.toString()).innerHTML = ""
                var mydiv = document.getElementById(i.toString());
                var aTag = document.createElement('a');
                post_link = 'details/' + myobj.post_link;
                aTag.setAttribute('href', post_link);
                aTag.setAttribute('target', '_blank')
                aTag.innerHTML = 'Post' + (i + 1) + " , " + myobj.post_title + " , " + myobj.post_author +" , " + myobj.post_details;
                mydiv.appendChild(aTag);
                return false
            }
            else{
                document.getElementById(i.toString()).innerHTML = ""
                return true
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            console.log('error');
        }
    });
}

function initial_load() {
    var t0 = performance.now();
    document.getElementById('timetaken').innerHTML = ""
    var pending = "pending....";
    var crawling = "Crawling....";
    var i = 0;
    for (i = 0; i < 10; i++){
        document.getElementById(i.toString()).innerHTML = pending;
    }
    i = 0;
    for(i = 0; i< 10; i++){
        document.getElementById(i.toString()).innerHTML = crawling;
        var val = scrape_post(i);
        if (val == true){
            break;
        }
    }
    var btn = document.getElementById("btnnext");
     if (document.getElementById(9).innerHTML != ""){
         btn.setAttribute("style","display:block;");
     }
     else{
        btn.setAttribute("style","display:block;");
     }

     var t1 = performance.now();
     document.getElementById('timetaken').innerHTML = "Total load time is " + (Math.round((t1 - t0)/ 1000)).toString() + " Seconds" ;
};



function RedirectFunct(tag){
    window.open("http://127.0.0.1:8000/?tag="+tag);
}

window.onload=function(){
    var url=new URL(document.URL);
    var tag=url.searchParams.get("tag");
    if(tag!=null){
        document.getElementById("txtSearch").value=tag;
        initial_load();
    }
}