

var currentMousePos = { x: -1, y: -1 };
$(document).mousemove(function(event) {
    currentMousePos.x = event.pageX;
    currentMousePos.y = event.pageY;
});

/*
	Add to cart fly effect with jQuery. - May 05, 2013
	(c) 2013 @ElmahdiMahmoud - fikra-masri.by
	license: https://www.opensource.org/licenses/mit-license.php
*/   

$('.add-to-cart').on('click', function (e) {
    e.preventDefault();
    var cart = $('.shopping-cart');
    var imgtodrag = $('.shop-img')
    //var imgtodrag = $(this).parent('.container').find(".shop-img").eq(0);
    
    if (imgtodrag) {
        //alert(' imgtodrag is true');
        console.log(imgtodrag)
        var imgclone = imgtodrag.clone();  
        

        imgclone.css({
            'opacity': '0.5',
            'position': 'absolute',
            'height': '150px',
            'width': '150px',
            'top' : currentMousePos.y + 'px',
            'left': currentMousePos.x + 'px',
            'border-radius':'20px',
            'z-index': '100'
        })

        // imgclone.offset({
        //     top: currentMousePos.y,
        //     left: currentMousePos.x
        //     //left: imgtodrag.offset().left
        // });
        
        imgclone.appendTo($('body'))

        imgclone.animate({
            'top': cart.offset().top,
            'left': cart.offset().left,
            'width': 40,
            'height': 40
        }, 500, 'easeInOutExpo');
        
        // setTimeout(function () {
        //     cart.effect("shake", {
        //         times: 2
        //     }, 200);
        // }, 1500);

        imgclone.animate({
            'width': 0,
                'height': 0
        }, function () {
            $(this).detach()
        });
    }
});