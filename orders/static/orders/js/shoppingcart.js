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
        var span1 = elem.nextElementSibling.children[0]
        span1.innerHTML = '$ ' + price
    });
});


/*
	Add to cart fly effect with jQuery. - May 05, 2013
	(c) 2013 @ElmahdiMahmoud - fikra-masri.by
	license: https://www.opensource.org/licenses/mit-license.php
*/   

$('.add-to-cart').on('click', function (e) {
    e.preventDefault();
    var cart = $('.shopping-cart');

    //var imgtodrag = $('.shop-img').eq(0)
    var imgtodrag = $(this).parent('p').parent('div').parent('div').parent('div').find(".shop-img").eq(0);
    
    if (imgtodrag) {
        console.log(imgtodrag)
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
            var cartItems = localStorage.getItem('cartItems');
            if (!cartItems){
                var cartItems = []
                localStorage.setItem('cartItems',cartItems)
            }

            alert(imgtodrag.data('prodid'))
        });
    }
});