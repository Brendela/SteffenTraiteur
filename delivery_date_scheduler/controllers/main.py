# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

import os
from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT


class website_sale_json(WebsiteSale):

    @http.route(['/shop/disable_slot'], type='json', auth="public", website=True)
    def disable_slot(self):
        timeformat = request.website.timeformat
        slot_24_obj = request.registry.get('disable.timeslots.his')
        slot_12_obj = request.registry.get('disable.timeslots')
        disable_dict = {}
        disable_days = []
        week_off_days = []
        single_day_off = []
        period_day_off = []
        disable_date_dict = {}
        for week_off in request.website.week_off_days:
            week_off_days.append(week_off.name)
        for single_day in request.website.single_day_off:
            single_day_off.append(single_day.day_off)
        for period_day in request.website.period_day_off:
            period_day_off.append(str(period_day.period_from) + 'to' + str(period_day.period_to))
        if timeformat == '24h':
            for slot_disable in request.website.disable_time_slot_his_ids:
                disable_days.append(slot_disable.day.name)
                disable_slot = []
                for slot in slot_disable.slots:
                    disable_slot.append(slot.id)
                disable_dict.update({slot_disable.day.name: disable_slot})
            for slot_date in request.website.disable_date_time_slot_his_ids:
                disable_slot = []
                for slot in slot_date.slots:
                    disable_slot.append(slot.id)
                disable_date_dict.update({str(slot_date.disable_date): disable_slot})
        else:
            for slot_disable in request.website.disable_time_slot_ids:
                disable_days.append(slot_disable.day.name)
                disable_slot = []
                for slot in slot_disable.slots:
                    disable_slot.append(slot.id)
                disable_dict.update({slot_disable.day.name: disable_slot})
            for slot_date in request.website.disable_date_time_slot_ids:
                disable_slot = []
                for slot in slot_date.slots:
                    disable_slot.append(slot.id)
                slot_date_string = str(slot_date.disable_date)

                disable_date_dict.update({slot_date_string: disable_slot})
        res = {'slot': disable_dict, 'day': disable_days, 'date_slot': disable_date_dict,
               'week_off': week_off_days, 'single_day': single_day_off, 'period_day': period_day_off}
        return {'slot': disable_dict, 'day': disable_days, 'date_slot': disable_date_dict, 'week_off': week_off_days, 'single_day': single_day_off, 'period_day': period_day_off}

    @http.route(['/shop/terms_json'], type='json', auth="public", website=True)
    def term_update_json(self):
        date_list = []
        days_list = []

        for day in range(0, int(request.website.minimum_interval_days or 0)):
            n_date = datetime.now() + relativedelta(days=day)
            date1 = n_date.strftime('%Y-%m-%d')
            date_list.append(date1)
        for day in request.website.single_day_off:
            date_list.append(day.day_off)
        for day in request.website.period_day_off:
            date = datetime.strptime(str(day.period_from), '%Y-%m-%d').date()
            date_to = datetime.strptime(str(day.period_to), '%Y-%m-%d').date()
            diff = (date_to-date).days
            d_list = []
            d_list.append(day.period_from)
            for i in range(0, diff):
                n_date = date + relativedelta(days=1)
                date1 = n_date.strftime('%Y-%m-%d')
                d_list.append(date1)
                date = n_date
            for d in d_list:
                date_list.append(d)
        for day in request.website.week_off_days:
            if day.name == 'Sunday':
                days_list.append(0)
            elif day.name == 'Monday':
                days_list.append(1)
            elif day.name == 'Tuesday':
                days_list.append(2)
            elif day.name == 'Wednesday':
                days_list.append(3)
            elif day.name == 'Thursday':
                days_list.append(4)
            elif day.name == 'Friday':
                days_list.append(5)
            elif day.name == 'Saturday':
                days_list.append(6)
        return {'list': date_list, 'days': days_list,
                'dateformat': request.website.date_format,
                'timeformat': request.website.timeformat,
                'min_days': request.website.minimum_interval_days
                }

    @http.route(['/shop/customer_order_delivery'], type='json', auth="public", methods=['POST'], website=True)
    def customer_order_delivery(self, **post):
        """ Json method that used to add a
        delivery date and/or comment when the user clicks on 'pay now' button.
        """
        uid = request.uid
        timeformat = request.website.timeformat
        if uid:
            user_obj = request.env['res.users'].sudo()
            user = user_obj.search([('id', '=', int(uid))])
        if post.get('delivery_date') or post.get('delivery_comment'):
            sale_order_obj = request.env['sale.order'].sudo()
            order = request.website.sale_get_order()
            redirection = self.checkout_redirection(order)
            if redirection:
                return redirection
            if order and order.id:
                values = {}
                if post.get('delivery_comment'):
                    values.update(
                        {'customer_order_delivery_comment': post.get('delivery_comment')})
                else:
                    values.update({'customer_order_delivery_comment': 'No Comment'})

                date = post.get('delivery_date')

                if request.website.show_delivery_schedule == 'timeslotview':
                    final_date = date
                else:
                    final_date = ''
                if date.endswith('PM'):
                    split_str = date.split(' ')
                    if split_str[1].startswith('10'):
                        hour = 22
                    elif split_str[1].startswith('11'):
                        hour = 23
                    elif split_str[1].startswith('12'):
                        hour = 12
                    elif split_str[1].startswith('01'):
                        hour = 13
                    elif split_str[1].startswith('02'):
                        hour = 14
                    elif split_str[1].startswith('03'):
                        hour = 15
                    elif split_str[1].startswith('04'):
                        hour = 16
                    elif split_str[1].startswith('05'):
                        hour = 17
                    elif split_str[1].startswith('06'):
                        hour = 18
                    elif split_str[1].startswith('07'):
                        hour = 19
                    elif split_str[1].startswith('08'):
                        hour = 20
                    elif split_str[1].startswith('09'):
                        hour = 21
                    minute1 = split_str[1].split(':')
                    minute = minute1[1]
                    time1 = str(hour) + ':' + str(minute) + ':' + '00'
                    final_date = split_str[0] + " " + time1
                elif date.endswith('AM'):
                    split_str = date.split(' ')
                    minute1 = split_str[1].split(':')
                    hour = minute1[0]
                    if split_str[1].startswith('12'):
                        hour = 00
                    minute = minute1[1]
                    time = str(hour) + ':' + str(minute) + ':' + '00'
                    final_date = split_str[0] + " " + time
                else:
                    final_date = date
                if request.website.date_format in ('D-M-Y', 'M-D-Y'):
                    final_date = final_date.replace('-', '/')
                if request.website.date_format in ('D.M.Y', 'M.D.Y'):
                    final_date = final_date.replace('.', '/')
                format = '%m/%d/%Y'  # default odoo date format
                date_mon_year = ['M', 'D', 'Y']
                if final_date:
                    if request.website.date_format in ('D-M-Y', 'D.M.Y', 'D/M/Y', 'M-D-Y', 'M.D.Y'):
                        if request.website.show_delivery_schedule == 'timeslotview':
                            if request.website.date_format == 'D-M-Y':
                                temp_str = final_date.split('/')
                                temp = temp_str[0]
                                temp_str[0] = temp_str[1]
                                temp_str[1] = temp
                                res = dict(zip(date_mon_year, temp_str))
                            if request.website.date_format == 'D.M.Y':
                                temp_str = final_date.split('/')
                                temp = temp_str[0]
                                temp_str[0] = temp_str[1]
                                temp_str[1] = temp
                                res = dict(zip(date_mon_year, temp_str))
                            if request.website.date_format == 'D/M/Y':
                                temp_str = final_date.split('/')
                                temp = temp_str[0]
                                temp_str[0] = temp_str[1]
                                temp_str[1] = temp
                                res = dict(zip(date_mon_year, temp_str))
                            if request.website.date_format == 'M-D-Y':
                                temp_str = final_date.split('-')
                                res = dict(zip(date_mon_year, temp_str))
                            if request.website.date_format == 'M.D.Y':
                                temp_str = final_date.split('.')
                                res = dict(zip(date_mon_year, temp_str))
                            final_date = ''
                            for t in temp_str:
                                final_date += t
                                final_date += '/'
                            if final_date.endswith('/'):
                                cnt = len(final_date)
                                final_date = final_date[:cnt-1]
                            final_date = res['Y'] + '-' + res['M'] + '-' + res['D']
                            final_date = final_date.split(' ')[0]
                            slot_name = post.get('slot_value', False)
                            if slot_name:
                                slot_value = slot_name.split('-')[0]
                                hour_get = slot_value.split(' ')[0]
                                hr_len = str(hour_get.split('.')[0])
                                if len(hour_get.split('.')) < 2:
                                    if len(hr_len) < 2:
                                        slot_hours = '0' + hour_get.split('.')[0]
                                    else:
                                        slot_hours = hour_get.split('.')[0]
                                    slot_minute = ':00'
                                else:
                                    slot_hours = hour_get.split('.')[0]
                                    slot_minute = hour_get.split('.')[1]
                                    if slot_minute == '5':
                                        slot_minute = ':30'
                                if timeformat == '24h':
                                    if slot_hours == '24':
                                        hours = '00'
                                        if slot_minute != '5':
                                            slot_minute = ':00:00'
                                            final_date = final_date + ' ' + hours + slot_minute
                                        else:
                                            final_date = final_date + ' ' + hours + slot_minute + ':00'
                                    else:
                                        final_date = final_date + ' ' + slot_hours + slot_minute + ':00'
                                else:
                                    final_date = final_date + ' ' + slot_hours + slot_minute + ':00'
                            else:
                                final_date = final_date + ' 00:00:00'
                        else:
                            final_spit_date_time = final_date.split(' ')
                            fdate = final_spit_date_time[0].split("/")
                            temp = fdate[0]
                            fdate[0] = fdate[1]
                            fdate[1] = temp
                            res = dict(zip(date_mon_year, fdate))
                            if request.website.enable_time_calendar:
                                final_date = res['Y'] + '-' + res['M'] + '-' + \
                                    res['D'] + ' ' + final_spit_date_time[1]
                            else:
                                final_date = res['Y'] + '-' + res['M'] + '-' + res['D']
                    if request.website.enable_time_calendar and request.website.show_delivery_schedule == 'calendarview':
                        if request.website.timeformat == '24h':
                            post_date = datetime.strptime(
                                final_date, DEFAULT_SERVER_DATE_FORMAT + ' %H:%M')
                        else:
                            post_date = datetime.strptime(
                                final_date, DEFAULT_SERVER_DATE_FORMAT + ' %H:%M:%S')
                        today_date = datetime.strptime(datetime.strftime(
                            datetime.today(), format + ' %H:%M:%S'), format + ' %H:%M:%S')
                    elif not request.website.enable_time_calendar and request.website.show_delivery_schedule == 'calendarview':
                        post_date = datetime.strptime(final_date, DEFAULT_SERVER_DATE_FORMAT)
                        today_date = datetime.strptime(datetime.strftime(
                            datetime.today(), format + ' %H:%M:%S'), format + ' %H:%M:%S')
                    else:
                        post_date = datetime.strptime(
                            final_date, DEFAULT_SERVER_DATE_FORMAT + ' %H:%M:%S')
                        today_date = datetime.strptime(
                            datetime.strftime(datetime.today(), format), format)
                    if os.path.exists("/etc/timezone"):
                        try:
                            f = open("/etc/timezone")
                            tz_value = f.read(128).strip()
                        except Exception:
                            pass
                        finally:
                            f.close()
                        from_zone = timezone('UTC')  # defualt utc store in db
                        to_zone = timezone(tz_value)  # system timezone
                        # use localize http://stackoverflow.com/questions/11442183/pytz-timezone-shows-weird-results-for-asia-calcutta
                        local_time = to_zone.localize(post_date)
                        utc = local_time.astimezone(from_zone)
                        date_utc = utc.strftime(DEFAULT_SERVER_DATE_FORMAT + ' %H:%M:%S')
                        final_date = date_utc.split('+')[0]
                    if post_date >= today_date:
                        values.update({'customer_order_delivery_date': final_date})
                if post.get('slot_name_val'):
                    if request.website.timeformat == '24h':
                        values.update({'time_slote_his_id': post.get('slot_name_val')})
                    else:
                        values.update({'time_slote_id': post.get('slot_name_val')})
                order.write(values)
        return True

    @http.route(['/shop/pay_delivery'], type='json', auth="public", website=True)
    def pay_delivery(self):
        if request and request.website and request.website.is_customer_order_delivery_date_feature:
            return False

        return {
            'interval': request.website.minimum_interval_days,
            'dateformat': request.website.date_format,
        }

    @http.route(['/shop/delivery_date_mandatory'], type='json', auth='public', website=True)
    def delivery_date_mandatory(self):
        if request and request.website and request.website.is_customer_order_delivery_date_feature:
            return False

        if request and request.website and request.website.delivery_date_mandatory:
            return True
        else:
            return False

    @http.route(['/shop/delivery_date/get_translated_warning'], type='json', auth="public", website=True)
    def get_translated_warning(self, interval_days=None):

        warning_msg = {
            'alert_1': _('Alert'),
            'warning_1': [_("<p>Please Select the date with minimum interval of %s days from today. </p>" % interval_days or '')],
            'warning_2': _('<p>Please Select Delivery Date and Time.</p>'),
        }

        return warning_msg
