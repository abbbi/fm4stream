$("form").submit(function(e) {
    var formURL = $(this).attr("action");
    var postData = $(this).serializeArray();
    $.ajax(
    {
        url : formURL,
        type: "POST",
        data : postData,
        success:function(data, textStatus, jqXHR) 
        {
            document.getElementById("add_basket_button_" + data.button_disable).innerHTML="Hinzugefügt";
            document.getElementById("add_basket_button_" + data.button_disable).disabled=true;
            update_basket(data.basket_count)
        },
        error: function(jqXHR, textStatus, errorThrown) 
        {
            alert('error')
        }
    });
    e.preventDefault(); //STOP default action
    e.unbind(); //unbind. to stop multiple form submit.
});

