 odoo.define('delivery_date_scheduler.payment', function(require) {
     "use strict";

     var ajax = require('web.ajax');


     function find_time_for_disable(d_format, slot_name, slot, i) {
         var last_am = 2;
         //var radios = $('input[name=slot]');
         var date_find = new Date();
         var current_hours = date_find.getHours()
         var hour_str = current_hours.toString();
         var new_hour_str = hour_str.concat('.' + (date_find.getMinutes()));
         var seperator = d_format[2];
         var month = d_format[0];
         var extra_reg = '\\';
         var new_seperator = extra_reg.concat(seperator);
         var re = new RegExp(new_seperator, 'g');
         var get_date = $('#delivery_date').val().replace(re, '/');
         var current_date = get_date.split('/')
         if (month == "M") {
             var get_month = current_date[0]
             var get_day = current_date[1]
         } else {
             var get_month = current_date[1]
             var get_day = current_date[0]
         }
         var dateObj = new Date(Number(current_date[2]), Number(get_month) - 1, Number(get_day))
         if (slot == 12) {
             var time_zone = slot_name.split("-")
             var start_time = parseFloat(time_zone[0])
             var am_pm = parseFloat(time_zone[1])
             var end_time = parseFloat(time_zone[2])
             if (start_time < 12 && am_pm == 1) {
                 start_time += 12;
             }
             //var hour_str = current_hours.toString();
             //var new_hour_str = hour_str.concat('.'+ (date_find.getMinutes()));
             if (parseFloat(new_hour_str) >= start_time && last_am != 1 && date_find == dateObj) {
                 radios[i].disabled = true;
                 slot_disable.push(radios[i]['value'])
             } else if (parseFloat(new_hour_str) > start_time && last_am == 1 && am_pm == 0) {
                 radios[i].disabled = false;
                 return false;
             } else {
                 last_am = am_pm;
             }
         } else {
             // var slot_24 = $(this).attr('value')
             var time_zone = slot_name.split("-")
             var start_time = parseFloat(time_zone[0])
             var end_time = parseFloat(time_zone[1])
             if (parseFloat(new_hour_str) >= start_time && date_find == dateObj) {
                 radios[i].disabled = true;
                 slot_disable.push(radios[i]['value'])
             }
         }
     }

     function disable_radio(d_format) {
         //var radios = $('input[name=slot]');
         $("input[name='slot']").each(function(i) {
             var slot_name = $(this).attr('value')
             if (slot_name.split("-").length > 2) {
                 find_time_for_disable(d_format, slot_name, 12, i);
             } else {
                 find_time_for_disable(d_format, slot_name, 24, i);
             }
         });
         /*$("input[name='slot']").each(function(i) {
           var slot_24 = $(this).attr('value')
           find_time_for_disable(slot_24,24,i);
         });*/
     }

     // change date format for compatible for new library 
     function change_dt_format(list) {
         var new_list = []
         for (var i = 0; i < list.length; i++) {
             var date = new Date(list[i]);
             new_list[i] = date
         }
         return new_list
     }

     $(document).ready(function() {
         try {
             var slot_disable = []
             var radios = $("input[name='slot']");
             $("input[name='slot']").each(function(i) {
                 radios[i].disabled = true;
             });
             ajax.jsonRpc('/shop/terms_json', 'call', {}).then(function(type) {

                 var disabledDateslist = change_dt_format(type['list']);
                 var daysOfWeekDisabled = type['days'];
                 var d_format = "MM/DD/YYYY HH:mm"
                 if (type['timeformat'] != 'am/pm') {
                     if (type['dateformat'] == "M/D/Y") {
                         d_format = "MM/DD/YYYY HH:mm";
                     } else if (type['dateformat'] == "D/M/Y") {
                         d_format = "DD/MM/YYYY HH:mm";
                     } else if (type['dateformat'] == "M-D-Y") {
                         d_format = "MM-DD-YYYY HH:mm";
                     } else if (type['dateformat'] == "D-M-Y") {
                         d_format = "DD-MM-YYYY HH:mm";
                     } else if (type['dateformat'] == "M.D.Y") {
                         d_format = "MM.DD.YYYY HH:mm";
                     } else if (type['dateformat'] == "D.M.Y") {
                         d_format = "DD.MM.YYYY HH:mm";
                     } else {
                         d_format = "DD/MM/YYYY HH:mm";
                     }
                     $('#datetimepicker1').datetimepicker({
                         minDate: new Date(),
                         disabledDates: disabledDateslist,
                         daysOfWeekDisabled: type['days'],
                         format: d_format,
                         ignoreReadonly: true,
                         // calendarWeeks:true,
                     });
                 } else {
                     if (type['dateformat'] == "M/D/Y") {
                         d_format = "MM/DD/YYYY hh:mm A";
                     } else if (type['dateformat'] == "D/M/Y") {
                         d_format = "DD/MM/YYYY hh:mm A";
                     } else if (type['dateformat'] == "M-D-Y") {
                         d_format = "MM-DD-YYYY hh:mm A";
                     } else if (type['dateformat'] == "D-M-Y") {
                         d_format = 'DD-MM-YYYY hh:mm A';
                     } else if (type['dateformat'] == "M.D.Y") {
                         d_format = "MM.DD.YYYY hh:mm A";
                     } else if (type['dateformat'] == "D.M.Y") {
                         d_format = "DD.MM.YYYY hh:mm A";
                     } else {
                         d_format = "DD/MM/YYYY hh:mm A";

                     }
                     $('#datetimepicker1').datetimepicker({
                         minDate: new Date(),
                         disabledDates: disabledDateslist,
                         daysOfWeekDisabled: type['days'],
                         format: d_format,
                         ignoreReadonly: true,
                         // calendarWeeks:true,
                     });

                 }

                 if (type['dateformat'] == "M/D/Y") {
                     d_format = "MM/DD/YYYY";
                 } else if (type['dateformat'] == "D/M/Y") {
                     d_format = "DD/MM/YYYY";
                 } else if (type['dateformat'] == "M-D-Y") {
                     d_format = "MM-DD-YYYY";
                 } else if (type['dateformat'] == "D-M-Y") {
                     d_format = "DD-MM-YYYY";
                 } else if (type['dateformat'] == "M.D.Y") {
                     d_format = "MM.DD.YYYY";;
                 } else if (type['dateformat'] == "D.M.Y") {
                     d_format = "DD.MM.YYYY";
                 } else {
                     d_format = "DD/MM/YYYY";
                 }
                 $('#datetimepicker2').datetimepicker({
                     minDate: new Date(),
                     disabledDates: disabledDateslist,
                     daysOfWeekDisabled: type['days'],
                     format: d_format,
                     useCurrent: false,
                     format: d_format,
                     ignoreReadonly: true,
                     // calendarWeeks:true,
                 }).on("dp.change", function(inst) {
                     //var radios = $('input[name=slot]');
                     disable_radio(d_format);
                     $("input[name='slot']").each(function(i) {
                         radios[i].checked = false;
                     });
                     ajax.jsonRpc('/shop/disable_slot', 'call', {}).then(function(type) {
                         var seperator = d_format[2];
                         var month = d_format[0];
                         var extra_reg = '\\';
                         var new_seperator = extra_reg.concat(seperator);
                         var re = new RegExp(new_seperator, 'g');
                         var get_date = $('#delivery_date').val().replace(re, '/');
                         var current_date = get_date.split('/')
                         if (month == "M") {
                             var get_month = current_date[0]
                             var get_day = current_date[1]
                         } else {
                             var get_month = current_date[1]
                             var get_day = current_date[0]
                         }
                         var dateObj = new Date(Number(current_date[2]), Number(get_month) - 1, Number(get_day))
                         var day = moment(dateObj).format('LLLL');
                         var day_string = day.toString();
                         var day_name = day_string.split(',')[0]
                         var new_date = current_date[2] + '-' + get_month + '-' + get_day;
                         var date_match = false;
                         var list_disable = []
                         var time_disable = []

                         for (var r = slot_disable.length; r < radios.length; r++) {
                             if (match != true || $.inArray(parseFloat(radios[r]['id']), time_disable) < 0 == false || $.inArray(parseFloat(radios[r]['id']), slot_disable) < 0 == false) {
                                 radios[r].disabled = false;
                             }
                         }
                         for (var slot_date in type['date_slot']) {
                             if (new_date == slot_date) {
                                 for (var slot = 0; slot < type['date_slot'][slot_date].length; slot++) {
                                     for (var r = slot_disable.length; r < radios.length; r++) {
                                         if (radios[r]['id'] == type['date_slot'][slot_date][slot]) {
                                             radios[r].disabled = true;
                                             list_disable.push(parseFloat(radios[r]['id']))
                                             date_match = true
                                         } else if (date_match != true || $.inArray(parseFloat(radios[r]['id']), list_disable) < 0) {
                                             radios[r].disabled = false;
                                         }
                                     }
                                 }
                             } else if (slot_date != new_date) {
                                 for (var slot = 0; slot < type['date_slot'][slot_date].length; slot++) {
                                     for (var r = slot_disable.length; r < radios.length; r++) {
                                         if ($.inArray(radios[r]['id'], list_disable) < 0 == false) {
                                             radios[r].disabled = false;
                                         } else if (radios[r]['id'] == type['date_slot'][slot_date][slot] && date_match != true) {
                                             radios[r].disabled = false;
                                         }
                                     }
                                 }
                             }
                             for (var r = slot_disable.length; r < radios.length; r++) {
                                 if (date_match != true || $.inArray(parseFloat(radios[r]['id']), list_disable[r]) > 0) {
                                     radios[r].disabled = false;
                                 }
                             }
                         }
                         
                         for (var i = 0; i < type['day'].length; i++) {
                             day = type['day'][i]
                             if (day_name == type['day'][i]) {
                                 var match = false
                                 for (var slot = 0; slot < type['slot'][day_name].length; slot++) {
                                     for (var r = slot_disable.length; r < radios.length; r++) {
                                         if (radios[r]['id'] == type['slot'][day_name][slot]) {
                                             radios[r].disabled = true;
                                             time_disable.push(parseFloat(radios[r]['id']))
                                             match = true
                                         } else if ($.inArray(parseFloat(radios[r]['id']), list_disable) < 0 != false && $.inArray(parseFloat(radios[r]['id']), time_disable) < 0 != false) {
                                             radios[r].disabled = false;
                                         }
                                     }
                                 }
                             } 
                            // This must be wrong becuase it should be select the day of the date which is selected.
                             /*else if ($.inArray(day, type['day']) > -1 && day_name != day) {
                                 for (var slot = 0; slot < type['slot'][day].length; slot++) {
                                     for (var r = slot_disable.length; r < radios.length; r++) {
                                         if (radios[r]['id'] == type['slot'][day][slot] && date_match != true) {
                                             radios[r].disabled = false;
                                         }
                                     }
                                 }
                             }*/
                         }
                     });
                 });
                 $('#delivery_date').val('');
             });

         } catch (e) {}
     });

 });