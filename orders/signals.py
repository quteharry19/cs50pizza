from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Order_detail


def topping_check(instance):

    try:
        topping_allowed = int(instance.product_detail.product_name[0])
        print('topping_allowed:',topping_allowed)
    except ValueError:
        topping_allowed = 0
        print('topping_allowed:',topping_allowed)

    topping_selected = instance.topping.in_bulk()
    topping_len = len(topping_selected)

    if topping_allowed != topping_len:
        pass
        raise ValidationError(f'Toppings allowed {topping_allowed} but selected {topping_len}',code='topping')
    else :
        print('toppings perfect')            


@receiver([m2m_changed],sender=Order_detail.topping.through)
def topping_changed(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    if "add" in action: #== 'post_add' or action == 'post_remove':
        topping_check(instance)


