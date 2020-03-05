$( document ).ready(function() {
    console.log( "ready!" );
    $.ajax(
    {
        url : '/basket/counter',
        type: 'GET',
        success:function(data, textStatus, jqXHR)
        {
            update_basket(data.basket_count)
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            alert('error')
        }
    });
});


function update_basket(basket_count) {
    span = document.getElementById("basket_counter");
    txt = document.createTextNode(basket_count);
    span.innerText = txt.textContent;
}
