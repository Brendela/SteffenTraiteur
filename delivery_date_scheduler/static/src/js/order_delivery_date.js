 odoo.define('delivery_date_scheduler.order_delivery', function(require){
'use strict';

var ajax = require('web.ajax');

 $(document).ready(function () {
 
        try{
                ajax.jsonRpc('/shop/terms_json', 'call', {}).then(function (type)
                {   
                    
                    if(type['timeformat'] != 'am/pm')
                    {
                        if(type['dateformat'] == 'M/D/Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "MM/DD/YYYY HH:mm",
                            });
                        }
                        if(type['dateformat'] == 'D/M/Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD/MM/YYYY HH:mm",
                            });
                        }
                        if(type['dateformat'] == 'M-D-Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "MM-DD-YYYY HH:mm",
                            });
                        }
                        if(type['dateformat'] == 'D-M-Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD-MM-YYYY HH:mm",
                            });
                        }
                        if(type['dateformat'] == 'M.D.Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "MM.DD.YYYY HH:mm",
                            });
                        }
                        if(type['dateformat'] == 'D.M.Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD.MM.YYYY HH:mm",
                            });
                        }
                        else
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD/MM/YYYY HH:mm",
                            });
                                
                        }
                    }
                    else
                    {
                    if(type['dateformat'] == 'M/D/Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "MM/DD/YYYY hh:mm A",
                            });
                        }
                        if(type['dateformat'] == 'D/M/Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD/MM/YYYY hh:mm A",
                            });
                        }
                        if(type['dateformat'] == 'M-D-Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "MM-DD-YYYY hh:mm A",
                            });
                        }
                        if(type['dateformat'] == 'D-M-Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : 'DD-MM-YYYY hh:mm A',
                            });
                        }
                        if(type['dateformat'] == 'M.D.Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "MM.DD.YYYY hh:mm A",
                            });
                        }
                        if(type['dateformat'] == 'D.M.Y')
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD.MM.YYYY hh:mm A",
                            });
                        }
                        else
                        {
                        $('#datetimepicker1').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD/MM/YYYY hh:mm A",
                            });
                                
                        }
                    
                    }
                
                if(type['dateformat'] == 'M/D/Y')
                        {
                        $('#datetimepicker2').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "MM/DD/YYYY",
                            });
                        }
                        if(type['dateformat'] == 'D/M/Y')
                        {
                        $('#datetimepicker2').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD/MM/YYYY",
                            });
                        }
                        if(type['dateformat'] == 'M-D-Y')
                        {
                        $('#datetimepicker2').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "MM-DD-YYYY",
                            });
                        }
                        if(type['dateformat'] == 'D-M-Y')
                        {
                        $('#datetimepicker2').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD-MM-YYYY",
                            });
                        }
                        if(type['dateformat'] == 'M.D.Y')
                        {
                        $('#datetimepicker2').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "MM.DD.YYYY",
                            });
                        }
                        if(type['dateformat'] == 'D.M.Y')
                        {
                        $('#datetimepicker2').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD.MM.YYYY",
                            });
                        }
                        else
                        {
                        $('#datetimepicker2').datetimepicker({
                            minDate:new Date(),
                            disabledDates: type['list'],
                            daysOfWeekDisabled: type['days'],
                            format : "DD/MM/YYYY",
                            });
                                
                        }
                $('#delivery_date').val('');
                });
            }
            catch(e){
            }
});

});