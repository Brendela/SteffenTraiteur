odoo.define('delivery_date_scheduler.mapped_values', function(require) {
    $(document).ready(function(){

        $("button#o_payment_form_pay").bind("click", function(ev) {
            ev.preventDefault()

            var customer_order_delivery_date = $('#delivery_date').val();
            var customer_order_delivery_comment = $('#delivery_comment').val();
            var slot_name_val = $("input[name='slot']:checked").attr('id');
            var slot_value = $("input[name='slot']:checked").attr('value');
            

            var $val = $(this).closest('form.o_payment_form')
            
            $val.find("input[name='payment_delivery_date']").val(customer_order_delivery_date);
            $val.find("input[name='payment_delivery_cmt']").val(customer_order_delivery_comment);
            $val.find("input[name='payment_delivery_slot_id']").val(slot_name_val);
            $val.find("input[name='payment_delivery_slot_value']").val(slot_value);

        });
    });
});
