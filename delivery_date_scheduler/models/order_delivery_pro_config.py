# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import *
import re

start_time_slot_12 = [('1', '1:00'), ('1.5', '1:30'), ('2', '2:00'), ('2.5', '2:30'), ('3', '3:00'), ('3.5', '3:30'), ('4', '4:00'), ('4.5', '4:30'),
                      ('5', '5:00'), ('5.5', '5:30'), ('6', '6:00'), ('6.5', '6:30'), ('7',
                                                                                       '7:00'), ('7.5', '7:30'), ('8', '8:00'), ('8.5', '8:30'),
                      ('9', '9:00'), ('9.5', '9:30'), ('10', '10:00'), ('10.5', '10:30'), ('11',
                                                                                           '11:00'), ('11.5', '11:30'), ('12', '12:00'), ('12.5', '12:30')
                      ]

start_time_slot_24 = [('0', '0:00'), ('0.5', '0:30'), ('1', '1:00'), ('1.5', '1:30'), ('2', '2:00'), ('2.5', '2:30'), ('3', '3:00'), ('3.5', '3:30'),
                      ('4', '4:00'), ('4.5', '4:30'), ('5', '5:00'), ('5.5', '5:30'), ('6',
                                                                                       '6:00'), ('6.5', '6:30'), ('7', '7:00'), ('7.5', '7:30'),
                      ('8', '8:00'), ('8.5', '8:30'), ('9', '9:00'), ('9.5', '9:30'), ('10',
                                                                                       '10:00'), ('10.5', '10:30'), ('11', '11:00'), ('11.5', '11:30'),
                      ('12', '12:00'), ('12.5', '12:30'), ('13', '13:00'), ('13.5', '13:30'), ('14',
                                                                                               '14:00'), ('14.5', '14:30'), ('15', '15:00'), ('15.5', '15:30'),
                      ('16', '16:00'), ('16.5', '16:30'), ('17', '17:00'), ('17.5', '17:30'), ('18',
                                                                                               '18:00'), ('18.5', '18:30'), ('19', '19:00'), ('19.5', '19:30'),
                      ('20', '20:00'), ('20.5', '20:30'), ('21', '21:00'), ('21.5', '21:30'), ('22',
                                                                                               '22:00'), ('22.5', '22.30'), ('23', '23:00'), ('23.5', '23:30')
                      ]

end_time_slot_12 = [('1', '1:00'), ('1.5', '1:30'), ('2', '2:00'), ('2.5', '2:30'), ('3', '3:00'), ('3.5', '3:30'), ('4', '4:00'), ('4.5', '4:30'),
                    ('5', '5:00'), ('5.5', '5:30'), ('6', '6:00'), ('6.5', '6:30'), ('7',
                                                                                     '7:00'), ('7.5', '7:30'), ('8', '8:00'), ('8.5', '8:30'),
                    ('9', '9:00'), ('9.5', '9:30'), ('10', '10:00'), ('10.5', '10:30'), ('11',
                                                                                         '11:00'), ('11.5', '11:30'), ('12', '12:00'), ('12.5', '12:30')
                    ]

end_time_slot_24 = [('0', '0:00'), ('0.5', '0:30'), ('1', '1:00'), ('1.5', '1:30'), ('2', '2:00'), ('2.5', '2:30'), ('3', '3:00'), ('3.5', '3:30'),
                    ('4', '4:00'), ('4.5', '4:30'), ('5', '5:00'), ('5.5', '5:30'), ('6',
                                                                                     '6:00'), ('6.5', '6:30'), ('7', '7:00'), ('7.5', '7:30'),
                    ('8', '8:00'), ('8.5', '8:30'), ('9', '9:00'), ('9.5', '9:30'), ('10',
                                                                                     '10:00'), ('10.5', '10:30'), ('11', '11:00'), ('11.5', '11:30'),
                    ('12', '12:00'), ('12.5', '12:30'), ('13', '13:00'), ('13.5', '13:30'), ('14',
                                                                                             '14:00'), ('14.5', '14:30'), ('15', '15:00'), ('15.5', '15:30'),
                    ('16', '16:00'), ('16.5', '16:30'), ('17', '17:00'), ('17.5', '17:30'), ('18',
                                                                                             '18:00'), ('18.5', '18:30'), ('19', '19:00'), ('19.5', '19:30'),
                    ('20', '20:00'), ('20.5', '20:30'), ('21', '21:00'), ('21.5', '21:30'), ('22',
                                                                                             '22:00'), ('22.5', '22.30'), ('23', '23:00'), ('23.5', '23:30')
                    ]


class SingleDayOff(models.Model):

    _name = "single.dayoff"
    _description = 'Single dayoff'

    day_off = fields.Date(string='Day Off')
    dayoff_setting = fields.Many2one('website', string="Website")


class PeriodDayOff(models.Model):
    _name = "period.dayoff"
    _description = 'Period Dayoff'

    period_from = fields.Date(string='Period From')
    period_to = fields.Date(string='Period To')
    dayoff_setting = fields.Many2one('website', string="Website",
                                     default=lambda self: self.env['website'].search([])[0])

    @api.model
    def create(self, vals):
        curr_dayof_setting_id = self.env['website'].search([], limit=1)
        domain = [('dayoff_setting', '=', curr_dayof_setting_id.id)
                  ] if curr_dayof_setting_id else []

        search_ids = self.search(domain)
        all_data = search_ids
        if vals:
            if not vals.get('period_from') or not vals.get('period_to'):
                raise ValidationError(_('Please add Period To and From date to disable Period'))
            if vals.get('period_from'):
                if not vals['period_to']:
                    raise ValidationError(_('Please add Period To date to disable Period'))
                if vals['period_to'] < vals['period_from']:
                    raise ValidationError(_('Period From can not be greater than Period To'))
                for d in all_data:
                    if vals['period_from'] >= d.period_from and vals['period_from'] <= d.period_to:
                        raise ValidationError(_('This period is already disabled'))
            elif vals.get('period_to'):
                if not vals['period_from']:
                    raise ValidationError(_('Please add Period From date to disable Period'))
                if vals['period_to'] < vals['period_from']:
                    raise ValidationError(_('Period From can not be greater than Period From '))
        res = super(PeriodDayOff, self).create(vals)
        return res

    # @api.multi
    def write(self, vals):
        for period in self:
            curr_dayof_setting_id = self.env['website'].search([], limit=1)
            domain = [('dayoff_setting', '=', curr_dayof_setting_id.id)
                      ] if curr_dayof_setting_id else []

            search_ids = self.search(domain)
            all_data = search_ids[1:]
            if vals:
                if vals.get('period_from'):
                    if vals['period_from']:
                        if not period.period_to:
                            raise ValidationError(_('Please add Period To date to disable Period'))
                        if period.period_to < vals['period_from']:
                            raise ValidationError(
                                _('Period From can not be greater than Period To '))
                        for d in all_data:
                            if vals['period_from'] >= d.period_from and vals['period_from'] <= d.period_to:
                                raise ValidationError(_('This period is already disabled'))
                    else:
                        raise ValidationError(_('Please add Period From date to disable Period'))
                elif vals.get('period_to'):
                    if vals['period_to']:
                        if not period.period_from:
                            raise ValidationError(
                                _('Please add Period From date to disable Period'))
                        if vals['period_to'] < period.period_from:
                            raise ValidationError(
                                _('Period From can not be greater than Period From '))
                    else:
                        raise ValidationError(_('Please add Period To date to disable Period'))

        res = super(PeriodDayOff, self).write(vals)
        return res


class WeekOffDay(models.Model):
    _name = "weekoff.days"
    _description = 'Week Off'

    name = fields.Char(string='Day')
    dayoff_setting = fields.Many2one('website', string="Website",
                                     default=lambda self: self.env['website'].search([])[0])


class DeliveryTimeslots(models.Model):
    _name = "delivery.timeslots"
    _description = 'Delivery lots'

    # @api.one
    @api.depends('starttime', 's_time', 'endtime', 'e_time')
    def get_name(self):
        s_time = ''
        e_time = ''
        for dt_slot in self:
            if dt_slot.s_time == '0':
                s_time = 'AM'
            else:
                s_time = 'PM'
            if dt_slot.e_time == '0':
                e_time = 'AM'
            else:
                e_time = 'PM'
            start = dt_slot.starttime
            end = dt_slot.endtime
            name = ''
            if start and '.5' in start or start:
                start = start.replace('.5', ':30')
                name += str(start + " " + s_time + " ")
            if end and '.5' in end or end:
                end = end.replace('.5', ':30')
                name += str(end + " " + e_time)
            dt_slot.name = name

    # @api.multi
    def name_get(self):
        result = []
        for data in self:
            s_time = ''
            e_time = ''
            if data.s_time == '0':
                s_time = 'AM'
            else:
                s_time = 'PM'
            if data.e_time == '0':
                e_time = 'AM'
            else:
                e_time = 'PM'
            start = data.starttime
            end = data.endtime
            name = ''
            if start and '.5' in start or start:
                start = start.replace('.5', ':30')
                name = str(start + " " + s_time + " ")
            if end and '.5' in end or end:
                end = end.replace('.5', ':30')
                name += str(end + " " + e_time)
            result.append((data.id, name))
        return result

    name = fields.Char(compute='get_name', string="Name", store=True)
    week_id = fields.Many2one('website', string="Website")
    starttime = fields.Selection(
        start_time_slot_12+[('0', '00:00'), ('0.5', '00:30')], 'Start Time')
    s_time = fields.Selection([('0', 'AM'), ('1', 'PM')],
                              string="AM PM", required=True, default='1')
    endtime = fields.Selection(end_time_slot_12+[('0', '00:00'), ('0.5', '00:30')], 'End Time')
    e_time = fields.Selection([('0', 'AM'), ('1', 'PM')],
                              string="Delivery time AM PM", required=True, default='1')


class DeliveryTimeslotsHis(models.Model):
    _name = "delivery.timeslots.his"
    _description = 'Delivery time his'

    # @api.one
    @api.depends('starttime_his', 'endtime_his')
    def get_name(self):
        for time_slot in self:
            start = time_slot.starttime_his
            end = time_slot.endtime_his
            if '.5' in start or '.5' in end:
                start = start.replace('.5', ':30')
                end = end.replace('.5', ':30')
            time_slot.name = str(start + ' - ' + end + " ")

    # @api.multi
    def name_get(self):
        result = []
        for data in self:
            start = data.starttime_his
            end = data.endtime_his
            if '.5' in start or '.5' in end:
                start = start.replace('.5', ':30')
                end = end.replace('.5', ':30')
            name = str(start + ' - ' + end + " ")
            result.append((data.id, name))
        return result

    name = fields.Char(compute='get_name', string="Name", store=True)
    week_id = fields.Many2one('website', string="Website",
                              default=lambda self: self.env['website'].search([])[0])
    starttime_his = fields.Selection(start_time_slot_24, 'Start Time')
    endtime_his = fields.Selection(end_time_slot_24, 'End Time')


class DeliveryDateTimeslots(models.Model):
    _name = "delivery.date.timeslots"
    _description = 'Delivery Date timeslots'

    # @api.multi
    def name_get(self):
        result = []
        for data in self:
            name = str(data.starttime_his + ' - ' + data.endtime_his + " ")
            result.append((data.id, name))
        return result

    name = fields.Char(string="Name")
    week_id = fields.Many2one('website', string="Website")


class DisableTimeslots(models.Model):
    _name = "disable.timeslots"
    _description = 'Disable timeslots'

    week_id = fields.Many2one('website', string="Website",
                              default=lambda self: self.env['website'].search([])[0])
    day = fields.Many2one('weekoff.days', string="Day")
    slots = fields.Many2many('delivery.timeslots', 'disable_time',
                             'weak_id', 'slot_id', string="Disable Time Slots", domain="[('week_id', '=', week_id)]")

    @api.model
    def create(self, vals):
        #search_ids = self.search([])
        curr_week_id = self.env['website'].search([], limit=1)
        domain = [('week_id', '=', curr_week_id.id)] if curr_week_id else []

        all_data = self.search(domain)
        if vals:
            if not vals.get('day') or not vals.get('slots'):
                raise ValidationError(_('Please add Day and Slots to disable TimeSlots'))
            if not vals['day']:
                raise ValidationError(_('Please add Day to disable TimeSlots'))
            if vals.get('day'):
                for d in all_data:
                    day_name = d.day.name
                    if day_name == 'Sunday':
                        day_count = 1
                    elif day_name == 'Monday':
                        day_count = 2
                    elif day_name == 'Tuesday':
                        day_count = 3
                    elif day_name == 'Wednesday':
                        day_count = 4
                    elif day_name == 'Thursday':
                        day_count = 5
                    elif day_name == 'Friday':
                        day_count = 6
                    elif day_name == 'Saturday':
                        day_count = 7
                    if vals['day'] == day_count:
                        raise ValidationError(_('Please Select other Day to disable TimeSlots'))
        res = super(DisableTimeslots, self).create(vals)
        return res

    # @api.multi
    def write(self, vals):
        # search_ids.remove(ids[0])
        curr_week_id = self.env['website'].search([], limit=1)
        domain = [('week_id', '=', curr_week_id.id)] if curr_week_id else []

        all_data = self.search(domain)
        if vals:
            if vals.get('day'):
                if vals['day']:
                    for d in all_data:
                        day_name = d.day.name
                        if day_name == 'Sunday':
                            day_count = 1
                        elif day_name == 'Monday':
                            day_count = 2
                        elif day_name == 'Tuesday':
                            day_count = 3
                        elif day_name == 'Wednesday':
                            day_count = 4
                        elif day_name == 'Thursday':
                            day_count = 5
                        elif day_name == 'Friday':
                            day_count = 6
                        elif day_name == 'Saturday':
                            day_count = 7
                        if vals['day'] == day_count:
                            raise ValidationError(
                                _('Please Select other Day to disable TimeSlots'))
                    if vals.get('slots'):
                        if vals['slots']:
                            if not vals['slots'][0][2]:
                                raise ValidationError(_('Please Add Time Slots to disable'))

                else:
                    raise ValidationError(_('Please add Day to disable TimeSlots'))
            elif vals.get('slots'):
                if vals['slots']:
                    if not vals['slots'][0][2]:
                        raise ValidationError(_('Please Add Time Slots to disable'))
        res = super(DisableTimeslots, self).write(vals)
        return res


class DisableTimeslotsHis(models.Model):
    _name = "disable.timeslots.his"
    _description = 'disable timeslots his'

    week_id = fields.Many2one('website', string="Website",
                              default=lambda self: self.env['website'].search([])[0])
    day = fields.Many2one('weekoff.days', string="Day")
    slots = fields.Many2many('delivery.timeslots.his', 'disable_time_his',
                             'weak_id', 'slot_id', string="Disable Time Slots", domain="[('week_id', '=', week_id)]")

    @api.model
    def create(self, vals):
        #search_ids = self.search([])
        curr_week_id = self.env['website'].search([], limit=1)
        domain = [('week_id', '=', curr_week_id.id)] if curr_week_id else []

        all_data = self.search(domain)
        if vals:
            if not vals.get('day') or not vals.get('slots'):
                raise ValidationError(_('Please add Day and Slots to disable TimeSlots'))
            if not vals['day']:
                raise ValidationError(_('Please add Day to disable TimeSlots'))
            if vals.get('day'):
                for d in all_data:
                    day_name = d.day.name
                    if day_name == 'Sunday':
                        day_count = 1
                    elif day_name == 'Monday':
                        day_count = 2
                    elif day_name == 'Tuesday':
                        day_count = 3
                    elif day_name == 'Wednesday':
                        day_count = 4
                    elif day_name == 'Thursday':
                        day_count = 5
                    elif day_name == 'Friday':
                        day_count = 6
                    elif day_name == 'Saturday':
                        day_count = 7
                    if vals['day'] == day_count:
                        raise ValidationError(_('Please Select other Day to disable TimeSlots'))
#                   if not vals['slots'][0][2]:
#                       raise ValidationError(_('Please Add Time Slots to disable'))
        res = super(DisableTimeslotsHis, self).create(vals)
        return res

    # @api.multi
    def write(self, vals):
        curr_week_id = self.env['website'].search([], limit=1)
        domain = [('week_id', '=', curr_week_id.id)] if curr_week_id else []

        all_data = self.search(domain)
        if vals:
            if vals.get('day'):
                if vals['day']:
                    for d in all_data:
                        day_name = d.day.name
                        if day_name == 'Sunday':
                            day_count = 1
                        elif day_name == 'Monday':
                            day_count = 2
                        elif day_name == 'Tuesday':
                            day_count = 3
                        elif day_name == 'Wednesday':
                            day_count = 4
                        elif day_name == 'Thursday':
                            day_count = 5
                        elif day_name == 'Friday':
                            day_count = 6
                        elif day_name == 'Saturday':
                            day_count = 7
                        if vals['day'] == day_count:
                            raise ValidationError(
                                _('Please Select other Day to disable TimeSlots'))
                    if vals.get('slots'):
                        if vals['slots']:
                            if not vals['slots'][0][2]:
                                raise ValidationError(_('Please Add Time Slots to disable'))

                else:
                    raise ValidationError(_('Please add Day to disable TimeSlots'))
            elif vals.get('slots'):
                if vals['slots']:
                    if not vals['slots'][0][2]:
                        raise ValidationError(_('Please Add Time Slots to disable'))
        res = super(DisableTimeslotsHis, self).write(vals)
        return res


class DisableDateTimeslots(models.Model):
    _name = "disable.date.timeslots"
    _description = 'Disable Date timeslots'

    week_id = fields.Many2one('website', string="Website",
                              default=lambda self: self.env['website'].search([])[0])
    disable_date = fields.Date(string='Disable Date')
    slots = fields.Many2many('delivery.timeslots', 'disable_date_time',
                             'weak_id', 'slot_id', string="Disable Time Slots", domain="[('week_id', '=', week_id)]")


class DisableDateTimeslotsHis(models.Model):
    _name = "disable.date.timeslots.his"
    _description = 'disable date timeslots his'

    week_id = fields.Many2one('website', string="Website",
                              default=lambda self: self.env['website'].search([])[0])
    disable_date = fields.Date(string='Disable Date')
    slots = fields.Many2many('delivery.timeslots.his', 'disable_date_his_time',
                             'weak_id', 'slot_id', string="Disable Time Slots", domain="[('week_id', '=', week_id)]")


class Website(models.Model):

    """Adds the fields for options of the Customer Order Delivery Date Feature."""

    _inherit = 'website'

    week_off_days = fields.Many2many('weekoff.days', 'week_off', 'weak_id', 'day_id',
                                     string="Day Off Settings")
    single_day_off = fields.One2many('single.dayoff', 'dayoff_setting', string="Single Day Off")
    period_day_off = fields.One2many('period.dayoff', 'dayoff_setting', string="Period Off")
    delivery_days = fields.Char(string='Number of Delivery Days')
    minimum_interval_hours = fields.Char(
        string='Minimum Interval of Hours', help=" Minimum interval of hours between the order placing time and delivery time")
    time_slot_ids = fields.One2many('delivery.timeslots', 'week_id', string="Add Time Slot")
    time_slot_ids_his = fields.One2many(
        'delivery.timeslots.his', 'week_id', string="Add Time Slot History")
    disable_time_slot_ids = fields.One2many(
        'disable.timeslots', 'week_id', string="Disable Time Slot of Days")
    disable_time_slot_his_ids = fields.One2many(
        'disable.timeslots.his', 'week_id', string="Disable Time Slot of Day")
    disable_date_time_slot_ids = fields.One2many(
        'disable.date.timeslots', 'week_id', string="Disable Time Slot of Particular Date")
    disable_date_time_slot_his_ids = fields.One2many(
        'disable.date.timeslots.his', 'week_id', string="Disable Time Slot of Particular Dates")
    timeformat = fields.Selection([('am/pm', 'AM/PM'), ('24h', '24 Hour')],
                                  string="Time Format", default='am/pm')
    is_customer_order_delivery_date_feature = fields.Boolean(
        string='Disable Delivery Date Scheduler',
        default=False,)
    is_customer_order_delivery_comment_feature = fields.Boolean(
        string='Disable Delivery Comment Feature',
        default=False,)
    show_delivery_schedule = fields.Selection([('calendarview', 'Calendar View'), ('timeslotview', 'TimeSlot View')],
                                              'Delivery Schedule View', default='calendarview')
    delivery_date_mandatory = fields.Boolean(string="Make Delivery Date Mandatory", default=False)
    label_date = fields.Char(string="Title", default="Delivery Date Time", translate=True)
    label_comment = fields.Char(string="Label for Delivery Date Comments",
                                default="Delivery Comment", translate=True)
    date_format = fields.Selection([('D/M/Y', 'D/M/Y'), ('M/D/Y', 'M/D/Y'), ('D-M-Y', 'D-M-Y'), ('M-D-Y', 'M-D-Y'), ('D.M.Y', 'D.M.Y'), ('M.D.Y', 'M.D.Y')],
                                   string="Date Format", default='D/M/Y')
    enable_time_calendar = fields.Boolean(string="Enable Time in Calendar", default=True)
    minimum_interval_days = fields.Char(string="Minimum interval of days between the order and delivery date",
                                        help=" Minimum Interval of days between the order and delivery date", default=1)
    starttime = fields.Selection(start_time_slot_12, 'Time Slot Start Time')
    starttime_his = fields.Selection(start_time_slot_24, 'Time Slot Start Time 24hrs')
    s_time = fields.Selection([('0', 'AM'), ('1', 'PM')],
                              string="AM PM", required=True, default='1')
    endtime = fields.Selection(end_time_slot_12, 'Time Slot End Time')
    endtime_his = fields.Selection(end_time_slot_24, 'Time Slot End Time 24hrs')
    e_time = fields.Selection([('0', 'AM'), ('1', 'PM')],
                              string="Delivery AM PM", required=True, default='1')


class ResConfigSettings(models.TransientModel):

    """Settings for the Customer Order Delivery Date."""

    _inherit = 'res.config.settings'

    is_customer_order_delivery_date_feature = fields.Boolean(
        related='website_id.is_customer_order_delivery_date_feature', string="Disable Delivery Date Scheduler", store=True, readonly=False)
    is_customer_order_delivery_comment_feature = fields.Boolean(
        related='website_id.is_customer_order_delivery_comment_feature', string="Disable Delivery Comment Feature", store=True, readonly=False)
    show_delivery_schedule = fields.Selection(related='website_id.show_delivery_schedule',
                                              string='Delivery Schedule View', store=True, readonly=False)
    delivery_date_mandatory = fields.Boolean(
        related='website_id.delivery_date_mandatory', string="Make Delivery Date Mandatory", store=True, readonly=False)
    label_date = fields.Char(related='website_id.label_date', string="Title",
                             store=True, translate=True, readonly=False)
    label_comment = fields.Char(related='website_id.label_comment',
                                string="Label for Delivery Date Comments", translate=True, readonly=False)
    date_format = fields.Selection(related='website_id.date_format',
                                   string="Date Format", store=True, readonly=False)
    timeformat = fields.Selection(related='website_id.timeformat',
                                  string="Time Format", store=True, readonly=False)
    enable_time_calendar = fields.Boolean(
        related='website_id.enable_time_calendar', string="Enable Time in Calendar", store=True, readonly=False)
    minimum_interval_days = fields.Char(related='website_id.minimum_interval_days', string="Minimum interval of days between the order and delivery date",
                                        help=" Minimum Interval of days between the order and delivery date", store=True, readonly=False)

    @api.onchange('is_customer_order_delivery_date_feature')
    def on_change_feature_disable(self):
        if self.is_customer_order_delivery_date_feature:
            self.enable_time_calendar = False

    # @api.one
    @api.constrains('minimum_interval_days')
    def on_change_check_days(self):
        for res_con_data in self:
            if res_con_data.minimum_interval_days and not (re.match('^[0-9]*$', res_con_data.minimum_interval_days)):
                raise ValidationError(
                    _('Error!\nPlease enter the Minimum Interval of days in digit (not special character)'))
            if res_con_data.minimum_interval_days and int(res_con_data.minimum_interval_days) < 0:
                raise ValidationError(
                    _('Error!\nPlease enter the Minimum Interval of days greater than -1'))


class DayoffSettings(models.Model):
    _name = 'dayoff.settings'
    _rec_name = 'website_id'
    _description = 'dayoff settings'

    def _default_website(self):
        return self.env['website'].search([('company_id', '=', self.env.company.id)], limit=1)

    # website_id = fields.Many2one('website', string="website")
    website_id = fields.Many2one('website', string="website",
                                 default=_default_website, ondelete='cascade')
    week_off_days = fields.Many2many(
        'weekoff.days', related='website_id.week_off_days', string="Day Off Settings", readonly=False)
    single_day_off = fields.One2many(
        related='website_id.single_day_off', string="Single Day Off", readonly=False)
    period_day_off = fields.One2many(
        related='website_id.period_day_off', string="Period Off", readonly=False)
    delivery_days = fields.Char(related='website_id.delivery_days',
                                string='Number of Delivery Days', default='2', readonly=False)
    minimum_interval_hours = fields.Char(related='website_id.minimum_interval_hours', string='Minimum Interval of Hours',
                                         help=" Minimum interval of hours between the time slots", default='2', readonly=False)
    timeformat = fields.Selection(related='website_id.timeformat',
                                  string="Time Format", default='am/pm', readonly=False)
    time_slot_ids_his = fields.One2many(
        related='website_id.time_slot_ids_his', string="Add Time Slot", readonly=False)
    disable_time_slot_his_ids = fields.One2many(
        related='website_id.disable_time_slot_his_ids', string="Disable Timing Slot of Day off", readonly=False)
    disable_time_slot_ids = fields.One2many(
        related='website_id.disable_time_slot_ids', string="Disable Time Slot of Day", readonly=False)
    disable_date_time_slot_ids = fields.One2many(
        related='website_id.disable_date_time_slot_ids', string="Disable Time Slot of Particular Date", readonly=False)
    disable_date_time_slot_his_ids = fields.One2many(
        related='website_id.disable_date_time_slot_his_ids', string="Disable Timing Slot of Particular Date", readonly=False)
    time_slot_ids = fields.One2many(related='website_id.time_slot_ids',
                                    string="Add Timing Slot", readonly=False)
    starttime = fields.Selection(related='website_id.starttime',
                                 string="Time Slot Start Time", default='1', readonly=False)
    starttime_his = fields.Selection(related='website_id.starttime_his',
                                     string="Time Slot Start Time 24hrs", default='1', readonly=False)
    s_time = fields.Selection(related='website_id.s_time', string="AM PM",
                              required=True, default='1', readonly=False)
    endtime = fields.Selection(related='website_id.endtime',
                               string="Time Slot End Time", default='4', readonly=False)
    endtime_his = fields.Selection(related='website_id.endtime_his',
                                   string="Time Slot End Time 24hrs", default='4', readonly=False)
    e_time = fields.Selection(related='website_id.e_time',
                              string="DayOff time AM PM", required=True, default='1', readonly=False)

    # @api.multi
    def write(self, vals):
        days_off = self.env['dayoff.settings'].search([]).mapped('website_id')
        if len(days_off.ids) == 0 or not vals.get('website_id') in days_off.ids:
            for day in self:
                if vals.get('starttime') == False or vals.get('starttime_his') == False or vals.get('endtime_his') == False or vals.get("endtime") == False \
                        or vals.get('disable_time_slot_ids') or vals.get('disable_time_slot_his_ids') or vals.get('disable_date_time_slot_ids') or vals.get('disable_date_time_slot_his_ids'):
                    if vals.get('time_slot_ids'):
                        for slot in vals.get('time_slot_ids'):
                            if slot[2] == False:
                                vals.update({'time_slot_ids': []})
                    if vals.get('time_slot_ids_his'):
                        for slot in vals.get('time_slot_ids_his'):
                            if slot[2] == False:
                                vals.update({'time_slot_ids_his': []})
                    res = super(DayoffSettings, self).write(vals)
                    return res
                elif vals.get('starttime', False) or vals.get('s_time') or vals.get("endtime", False)\
                        or vals.get('e_time') or vals.get('starttime_his', False) or vals.get('endtime_his', False) or vals.get('minimum_interval_hours'):
                    if vals.get('time_slot_ids'):
                        new_slot = []
                        for slot in vals.get('time_slot_ids'):
                            if slot[2] != False:
                                new_slot.append(slot)
                        vals.update({'time_slot_ids': new_slot})
                    if vals.get('time_slot_ids_his'):
                        new_slot = []
                        for slot in vals.get('time_slot_ids_his'):
                            if slot[2] != False:
                                new_slot.append(slot)
                        vals.update({'time_slot_ids_his': new_slot})
                    if vals.get('disable_time_slot_ids'):
                        vals.update({'disable_time_slot_ids': []})
                    if vals.get('disable_time_slot_his_ids'):
                        vals.update({'disable_time_slot_his_ids': []})
                    if vals.get('disable_date_time_slot_ids'):
                        vals.update({'disable_date_time_slot_ids': []})
                    if vals.get('disable_date_time_slot_his_ids'):
                        vals.update({'disable_date_time_slot_his_ids': []})
                    if day:
                        for delivery in day.time_slot_ids:
                            delivery.unlink()
                        for delivery in day.time_slot_ids_his:
                            delivery.unlink()
                        for disable_slot in day.disable_time_slot_ids:
                            disable_slot.unlink()
                        for disable_date_time in day.disable_date_time_slot_his_ids:
                            disable_date_time.unlink()
                        for disable_slot_his in day.disable_time_slot_his_ids:
                            disable_slot_his.unlink()
                        for disable_date_time in day.disable_date_time_slot_ids:
                            disable_date_time.unlink()
            res = super(DayoffSettings, self).write(vals)
            return res
        else:
            raise ValidationError(
                _('You can not configure day and timeslot setting for same website'))

    @api.model
    def create(self, vals):
        days_off = self.env['dayoff.settings'].search([]).mapped('website_id')
        if len(days_off.ids) == 0 or not vals.get('website_id') in days_off.ids:
            if vals.get('week_id'):
                domain = [('week_id', '=', vals.get('week_id'))]
            else:
                domain = []
            if vals.get('time_slot_ids'):
                vals.update({'time_slot_ids_his': []})
                obj = self.env['delivery.timeslots']
            else:
                vals.update({'time_slot_ids': []})
                obj = self.env['delivery.timeslots.his']
            if vals.get('disable_time_slot_ids'):
                vals.update({'disable_time_slot_ids': []})
            if vals.get('disable_time_slot_his_ids'):
                vals.update({'disable_time_slot_his_ids': []})
            if vals.get('disable_date_time_slot_ids'):
                vals.update({'disable_date_time_slot_ids': []})
            if vals.get('disable_date_time_slot_his_ids'):
                vals.update({'disable_date_time_slot_his_ids': []})
            #search_ids = obj.search(domain)
            all_data = obj.search(domain)
            for d in all_data:
                if vals.get('time_slot_ids'):
                    new_slot = []
                    for slot in vals.get('time_slot_ids'):
                        if slot[2] != False:
                            new_slot.append(slot)
                    vals.update({'time_slot_ids': new_slot})
                if vals.get('time_slot_ids_his'):
                    new_slot = []
                    for slot in vals.get('time_slot_ids_his'):
                        if slot[2] != False:
                            new_slot.append(slot)
                    vals.update({'time_slot_ids_his': new_slot})
                # d.unlink()
            config_id = super(DayoffSettings, self).create(vals)
            return config_id
        else:
            raise ValidationError(
                _('You can not configure day and timeslot setting for same website'))

    def timeslot_dict_24(self, start, interval, endtime, lot_slot):
        slot_dict = (str(start)), (str(endtime if endtime < start + interval and start < endtime else (start + interval - 24 if start +
                                                                                                       interval > 24 and start + interval - 24 < endtime else (endtime if start + interval - 24 > endtime else start + interval))))
        if '.0' in slot_dict[0]:
            slot_dict1 = slot_dict[0].split('.')[0]
        else:
            slot_dict1 = slot_dict[0]
        if slot_dict1 == '24':
            slot_dict1 = '0'
        if slot_dict1 == '24.5':
            slot_dict1 = '0.5'
        if '.0' in slot_dict[1]:
            slot_dict2 = slot_dict[1].split('.')[0]
        else:
            slot_dict2 = slot_dict[1]
        if slot_dict2 == '24':
            slot_dict2 = '0'
        if slot_dict2 == '24.5':
            slot_dict2 = '0.5'
        lot_dict = {'starttime_his': slot_dict1, 'endtime_his': slot_dict2}
        lot_slot.append((0, 0, lot_dict))

    def timslot_dict(self, start, interval, endtime, d, e_time, time=False):
        if time:
            slot_dict = ((str(start - 12) if start > 12 else str(12 if start == 0.0 else start)),
                         ('0' if start < 12 else '1'),
                         (str(start + interval - 12) if start + interval > 12 and start + interval < endtime
                          else str(endtime - 12 if start+interval >= endtime and endtime > 12.5
                                   else (endtime if endtime < start+interval and e_time != '0' else (start + interval if start + interval < endtime else endtime)))),
                         ('0' if start + interval < 12 or endtime < 12 else '1'))
        else:
            slot_dict = ((str(start - 12) if start > 12 else str(start)),
                         ('1' if start > 12 and start != 24 else ('0' if start < 12 else '1')),
                         (str(start + interval - 12) if start + interval > 12 and start + interval <= 24 and start + interval > endtime
                          else str((endtime if start + interval >= 24 and start + interval - 24 > endtime else abs(start + interval - 24)) if start+interval > 24 and endtime < start and endtime != 0
                                   else (start + interval if start + interval < endtime else (endtime if start + interval >= 24 and start + interval - 24 > endtime else (start + interval - 24 if start + interval >= 24 else start + interval))))),
                         ('1' if start + interval > 12 and start + interval < 24 else ('0' if start + interval < 12 else ('0' if start > 12 else '1'))))
        if '.0' in slot_dict[0]:
            slot_dict1 = slot_dict[0].split('.')[0]
            if slot_dict1 == '0' and slot_dict[1] != '0':
                slot_dict1 = '12'
            if slot_dict1 == '0.5' and slot_dict[1] != '0':
                slot_dict1 = '12.5'
        else:
            if slot_dict[0] == '0':
                slot_dict1 = '12'
            elif slot_dict[0] == '0.5':
                slot_dict1 = '12.5'
            else:
                slot_dict1 = slot_dict[0]

        if slot_dict1 == '12' and slot_dict[1] == '0':
            slot_dict1 = '0'
        if slot_dict1 == '12.5' and slot_dict[1] == '0':
            slot_dict1 = '0.5'
        if '.0' in slot_dict[2]:
            slot_dict2 = slot_dict[2].split('.')[0]
            if slot_dict2 == '0.5':
                slot_dict2 = '12.5'
            if slot_dict2 == '0':
                slot_dict2 = '12'
        else:
            if slot_dict[2] == '0.5':
                slot_dict2 = '12.5'
            elif slot_dict[2] == '0':
                slot_dict2 = '12'
            else:
                slot_dict2 = slot_dict[2]
        if slot_dict2 == '12' and slot_dict[3] == '0':
            slot_dict2 = '0'
        if slot_dict2 == '12.5' and slot_dict[3] == '0':
            slot_dict2 = '0.5'

        lot_dict = {'starttime': slot_dict1,
                    's_time': slot_dict[1], 'endtime': slot_dict2, 'e_time': slot_dict[3]}
        d.append((0, 0, lot_dict))

    @api.onchange('minimum_interval_hours', 'starttime', 's_time', 'endtime', 'e_time', 'starttime_his', 'endtime_his', 'timeformat')
    def onchange_timeslot_12(self):
        if self.time_slot_ids:
            self.time_slot_ids = [(6, False, [])]
        if self.time_slot_ids_his:
            self.time_slot_ids_his = [(6, False, [])]
        if self.starttime == False:
            starttime1 = 1
        else:
            starttime1 = float(self.starttime)
        if self.endtime == False:
            endtime1 = 4
        else:
            endtime1 = float(self.endtime)
        if self.starttime_his == False:
            starttime = 13
        else:
            starttime = float(self.starttime_his)
        if self.endtime_his == False:
            endtime = 17
        else:
            endtime = float(self.endtime_his)
        if self.minimum_interval_hours and not (re.match('^[0-9-.]*$', self.minimum_interval_hours)):
            raise ValidationError(
                _('Error!\nPlease enter the Minimum Interval of time slot in digit or float (not special character)'))
        if float(self.minimum_interval_hours) < 0.5 or not starttime1 or not endtime1 and self.timeformat != '24h':
            self.time_slot_ids = []
            self.time_slot_ids_his = []
        if self.timeformat != '24h' and self.starttime and self.endtime:
            if '.' not in self.starttime:
                start = self.starttime + (':00 am' if self.s_time == '0' else ':00 pm')
            else:
                start = self.starttime.replace(
                    '.', ':') + ('0 am' if self.s_time == '0' else '0 pm')
            if '.' not in self.endtime:
                end = self.endtime + (':00 am' if self.e_time == '0' else ':00 pm')
            else:
                end = self.endtime.replace('.', ':') + ('0 am' if self.e_time == '0' else '0 pm')
            start = datetime.strftime(datetime.strptime(start, '%I:%M %p'), '%H:%M')
            end = datetime.strftime(datetime.strptime(end, '%I:%M %p'), '%H:%M')
            starttime1 = float(start.replace(':', '.')[:4])
            endtime1 = float(end.replace(':', '.')[:4])
            min_interval = float(self.minimum_interval_hours)
        if self.timeformat == '24h':
            slot = []
            min_interval = float(self.minimum_interval_hours)
            #starttime = float(self.starttime_his)
            #endtime = float(self.endtime_his)
            start = starttime
            while start > endtime and min_interval >= 0.5:
                end = min_interval
                if start > 24:
                    start = start - 24
                    break
                else:
                    self.timeslot_dict_24(start, end, endtime, slot)
                    start = start + end
            while start < endtime and min_interval >= 0.5:
                end = min_interval
                self.timeslot_dict_24(start, end, endtime, slot)
                start = start + end
            self.time_slot_ids_his = slot
        else:
            slot = []
            min_interval = float(self.minimum_interval_hours)
            if starttime < endtime1 and min_interval >= 0.5:
                start = starttime1
                while start < endtime1:
                    end = min_interval
                    self.timslot_dict(start, end, endtime1, slot, self.e_time, time=True)
                    start = start + end
            else:
                start = starttime1
                while start >= endtime1 and min_interval >= 0.5:
                    end = min_interval
                    if start >= 24:
                        start = start - 24
                        break
                    else:
                        self.timslot_dict(start, end, endtime1, slot, self.e_time)
                        start = start + end

                while start < endtime1 and min_interval >= 0.5:
                    end = min_interval
                    self.timslot_dict(start, end, endtime1, slot, self.e_time, time=True)
                    start = start + end
            self.time_slot_ids = slot

    @api.onchange('timeformat')
    def onchange_timeformat(self):
        if self.timeformat:
            if self.timeformat == '24h':
                single_day_off = self.env['delivery.timeslots.his']
                data = single_day_off.search([])
                l1 = []
                for d in data:
                    l1.append(d.id)
                single_day_off1 = self.env['disable.timeslots.his']
                data1 = single_day_off1.search([])
                l2 = []
                for d in data1:
                    l2.append(d.id)
                self.time_slot_ids_his = l1
                self.disable_time_slot_his_ids = l2
            else:
                single_day_off = self.env['delivery.timeslots']
                data = single_day_off.search([])
                l1 = []
                for d in data:
                    l1.append(d.id)
                single_day_off1 = self.env['disable.timeslots']
                data1 = single_day_off1.search([])
                l2 = []
                for d in data1:
                    l2.append(d.id)
                self.time_slot_ids = l1
                self.disable_time_slot_ids = l2
        else:
            self.time_slot_ids_his = False
            self.disable_time_slot_his_ids = False
