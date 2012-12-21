/*show and hide location map for ASCHII art page*/
$(document).ready(function()
          {  
             $("a#show_map_div").click(function() {
             $("DIV#hidden_map").toggle();
             $("DIV#art_container").toggle();
             });  
           });     