$(function () {
    $('.selectpicker').selectpicker();
});

var currentMousePos = { x: -1, y: -1 };
$(document).mousemove(function(event) {
    currentMousePos.x = event.pageX;
    currentMousePos.y = event.pageY;
});


if (!localStorage.getItem('cartItems')){
    cartItems = []
    localStorage.setItem('cartItems',JSON.stringify(cartItems));
} else {
    cartItems = JSON.parse(localStorage.getItem('cartItems'));
}

var total_price = 0

addItemHandler = (item, index, arr) => {
    if (item != null){
    var cartLi = document.createElement('li')
    cartLi.className = "list-group-item bg-dark"
    var extprice = 0
    let extras = []

    if (item.extras != undefined){
        item.extras.forEach(ext => {
            let extkey = Object.keys(ext)[0]
            extras.push(extkey.toString())
            extprice += parseFloat(ext[extkey])
        });
    }
    itemCost = item.rate + extprice
    total_price += parseFloat(itemCost)
    cartLi.innerHTML = `<span>${item.prodname}</span> `
    cartLi.innerHTML += `<span>${item.catname}</span> <span class="float-right"> $ ${itemCost} </span><br />`
    cartLi.innerHTML += ` <span>Size : ${item.size}</span> <a href="#" onClick={delItemHandler(this,${index},${itemCost})} class="delitem float-right"><i class="icon-delete"></i></a> <br />`
    cartLi.innerHTML += ` <span>Topping : ${item.topping}</span> <br />`
    cartLi.innerHTML += ` <span>Extras : ${extras.toString()}</span> <br />`
    //cartLi.innerHTML += ` <span>Item Cost : $ ${itemCost}`
    document.querySelector('#cartUL').appendChild(cartLi);
    document.querySelector('#total_price').innerHTML = '$ ' + total_price.toFixed(2)
    }
}

document.querySelectorAll('.delitem').forEach(delitem => {
    delitem.onclick = delItemHandler(delitem)
})

document.querySelector('#checkoutForm').onsubmit = (e) => {
    //e.preventDefault()
    cartData = document.createElement('input')
    cartData.setAttribute('type',"hidden")
    cartData.setAttribute('name',"cartitems")
    cartData.setAttribute('value',JSON.stringify(cartItems))
    document.querySelector('#cartUL').appendChild(cartData)
    //localStorage.setItem('cartItems',[])
    checknull = (item) => {
        return item!=null
    }

    if (cartItems.filter(checknull).length == 0){
        alert('cart is empty')
        return false
    }
    // alert(cartItems.filter(checknull).length);

}

delItemHandler = (delitem, index, itemCost) => {
    var delParent = delitem.parentElement
    delParent.remove();
    //cartItems.splice(index,1)
    delete cartItems[index]
    localStorage.setItem('cartItems',JSON.stringify(cartItems));
    total_price -= parseFloat(itemCost)
    document.querySelector('#total_price').innerHTML = '$ ' + total_price.toFixed(2)
    return false;
}

checkoutButtonHandler = (cartItems) => {
    if (cartItems.length > 0){
        document.getElementById('checkout').disabled = false
        cartItems.forEach(addItemHandler);
        
    }else{
        document.getElementById('checkout').disabled = true
        // document.querySelector('#checkout').disabled = true
    }
}

checkoutButtonHandler(cartItems);

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

    var selectedToppings = []
    var selectTopping = $(this).parent('p').parent('div').find('[name=topping]').eq(0);
    var optionTopping = $(selectTopping).find('option:selected');
    optionTopping.each(function (){
        if ($(this).data('topping') === undefined) {
            var topToAdd = ""
        } else {
            var topToAdd = $(this).data('topping')
        }
        selectedToppings.push(topToAdd);
    });

    var selectedExtras = []
    var selectExtra = $(this).parent('p').parent('div').find('#extras').eq(0);
    var optionExtra = $(selectExtra).find('option:selected');
    optionExtra.each(function (){
        const extra = $(this).data('extra');
        const price = $(this).data('price');
        selectedExtras.push({[extra] : price})
    });

    if (imgtodrag) {
        var imgclone = imgtodrag.clone();  

    var item = {
        'prodid' : imgclone.data('prodid'),
        'prodname' : imgclone.data('prodname'),
        'catname' : imgclone.data('catname'),
        'size' : $(itemSize).val(),
        'quantity' : 1,
        'topping' : selectedToppings,
        'extras' : selectedExtras,
        'rate' : parseFloat(itemPrice)
        //'img' : imgtodrag
    }

    if (!isNaN(item.prodname[0])) {
        const toppingAllowed = parseInt(item.prodname[0])
        if (toppingAllowed < optionTopping.length) {
            alert('more toppings selected')
            throw new Error('more toppings selected')
        } else if (toppingAllowed > optionTopping.length) {
            alert('Please Select more toppings')
            throw new Error('Please Select more toppings')
        }
    }
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

        addItemHandler(item, cartItems.length, cartItems)

        cartItems.push(item)
        
        localStorage.setItem('cartItems',JSON.stringify(cartItems));
        
        document.getElementById('checkout').disabled = false
    });
}
});