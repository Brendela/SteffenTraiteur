odoo.define('delivery_date_scheduler.scheduler', function(require) {
    "use strict";
    var ajax = require('web.ajax');
    var PaymentGateway = require('payment.payment_form')
    var Widget = require("web.Widget");
    var Dialog = require("web.Dialog");

    var core = require('web.core');
    var _t = core._t;
    
    // function sleep(delay) {
    //     var start = new Date().getTime();
    //     while (new Date().getTime() < start + delay);
    // }

    return PaymentGateway.include({

        payEvent: function (ev) {
            ev.preventDefault();
            var self = this;
            var _super = this._super.bind(this);

            var customer_order_delivery_date = self.$("input[name='payment_delivery_date']").val();
            var customer_order_delivery_comment = self.$("input[name='payment_delivery_cmt']").val();
            var slot_name_val = self.$("input[name='payment_delivery_slot_id']").val();
            var slot_value = self.$("input[name='payment_delivery_slot_value']").val();

            if (customer_order_delivery_date && customer_order_delivery_date.length != 0) {
                
                ajax.jsonRpc('/shop/customer_order_delivery', 'call', {
                    'delivery_date': customer_order_delivery_date,
                    'delivery_comment': customer_order_delivery_comment,
                    'slot_name_val': slot_name_val,
                    'slot_value': slot_value,
                });
                ajax.jsonRpc('/shop/pay_delivery', 'call', {}).then(function(type) {
                    if (type) {
                        var str = customer_order_delivery_date.slice(customer_order_delivery_date.length - 2, customer_order_delivery_date.length);
                        var date = new Date();
                        var str1 = date.getDate();
                        f1 = str1.toString();
                        var f2 = f1.concat('/' + (date.getMonth() + 1) + "/" + date.getFullYear());

                        var a = moment(f2, type['dateformat']);
                        var b;

                        if ((type['dateformat'] == 'M-D-Y') || (type['dateformat'] == 'M.D.Y') || (type['dateformat'] == 'M/D/Y')) {
                            var date = new Date();
                            var str1 = date.getMonth() + 1;
                            var f1 = str1.toString();
                            var f2 = f1.concat('/' + date.getDate() + "/" + date.getFullYear());

                            var a = moment(f2, type['dateformat']);

                            var s = customer_order_delivery_date.substr(6, 4);
                            var s1 = customer_order_delivery_date.substr(3, 2);
                            var s2 = customer_order_delivery_date.substr(0, 2);
                            var date1 = new Date(s, s2 - 1, s1);
                            var str1;
                            str1 = s2.concat("/" + s1 + '/')
                            var str2 = str1.concat(s + " " + customer_order_delivery_date.substr(11, 5))

                            var b = moment(str2, type['dateformat']);
                        } else {
                            if ((str == "AM") || (str == "PM")) {
                                var ampm = customer_order_delivery_date.substring(0, customer_order_delivery_date.length - 3)
                                var b = moment(ampm, type['dateformat']);

                            } else {
                                var b = moment(customer_order_delivery_date, type['dateformat']);
                            }
                        }
                        var diffDays = b.diff(a, 'days');
                        if (Math.abs(diffDays) < type['interval']) {

                            ajax.jsonRpc('/shop/delivery_date/get_translated_warning', 'call', {
                                interval_days : type['interval'],
                            }).then(function (warning){
                                if (warning){
                                    self.customDisplayError(
                                        warning['alert_1'],
                                        warning['warning_1']
                                        );
                                }
                            });

                        } else {
                            return _super(ev)
                        }
                    }
                    else{
                        return _super(ev)
                    }
                });
            } else {
                ajax.jsonRpc('/shop/delivery_date_mandatory', 'call', {}).then(function(type) {
                    if (type) {

                        ajax.jsonRpc('/shop/delivery_date/get_translated_warning', 'call', {}).then(function (warning){
                            if (warning){
                                self.customDisplayError(
                                    warning['alert_1'],
                                    warning['warning_2']
                                );
                            }
                        });
                    } else {
                        return _super(ev);
                    }
                });
            }
        },

        customDisplayError: function(title, message){
            return new Dialog(null, {
                title: _t('Error: ') + title,
                size: 'medium',
                $content: message ,
                buttons: [
                {text: _t('Ok'), close: true}]}).open();
        },

    });
 
});
/* http://stackoverflow.com/questions/542938/how-do-i-get-the-number-of-days-between-two-dates-in-javascript */