$(function () {
    $('.selectpicker').selectpicker();
});

var currentMousePos = { x: -1, y: -1 };
$(document).mousemove(function(event) {
    currentMousePos.x = event.pageX;
    currentMousePos.y = event.pageY;
});


document.querySelectorAll('.size').forEach(elem =>{
    elem.addEventListener('change',(event)=>{
        var price = event.target.options[event.target.selectedIndex].dataset.price
        
        if (elem.nextElementSibling.children[0]){
            var span1 = elem.nextElementSibling.children[0]
            span1.innerHTML = '$ ' + price
        }
    });
});

$('.add-to-cart').on('click', function (e) {
    e.preventDefault();
    var cart = $('.shopping-cart');

    //var imgtodrag = $('.shop-img').eq(0)
    var imgtodrag = $(this).parent('p').parent('div').parent('div').parent('div').find(".shop-img").eq(0);

    var itemSize = $(this).parent('p').parent('div').find('.size').eq(0);

    var itemPrice = $(itemSize).find(':selected').data('price')


    if (imgtodrag) {
        var imgclone = imgtodrag.clone();  

        imgclone.css({
            'opacity': '0.8',
            'position': 'absolute',
            'height': '150px',
            'width': '150px',
            'top' : currentMousePos.y + 'px',
            'left': currentMousePos.x + 'px',
            'border-radius':'20px',
            'z-index': '100'
        })

        imgclone.appendTo($('body'))

        imgclone.animate({
            'top': cart.offset().top,
            'left': cart.offset().left,
            'width': 40,
            'height': 40
        }, 700, 'linear');
        //easeInOutExpo
        imgclone.animate({
            'width': 0,
                'height': 0
        }, function () {
            $(this).detach()

            if (!localStorage.getItem('cartItems')){
                var cartItems = []
                localStorage.setItem('cartItems',JSON.stringify(cartItems));
            } else {
                var cartItems = JSON.parse(localStorage.getItem('cartItems'));
            }

            var item = {
                'prodid' : imgclone.data('prodid'),
                'size' : $(itemSize).val(),
                'quantity' : 1,
                'topping' : ['Pepproni','Mushroom','Onions'],
                'rate' : parseFloat(itemPrice) ,
                // 'img' : imgtodrag
            }

            cartItems.push(item)

            console.log(cartItems);

            localStorage.setItem('cartItems',JSON.stringify(cartItems));

        });
    }
});