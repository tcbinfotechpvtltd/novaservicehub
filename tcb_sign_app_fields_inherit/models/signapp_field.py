from odoo import models,fields,api
import base64


class SignappField(models.Model):
    _inherit = 'signapp.field'


    def sign_app_fields_generate_pdf(self):
        # Executed on a Generate PDF report button click.Crate Roles, Tags, based on data. based on reports selected will also crated attachemnt and SignApp Template. And add Signature Item inside Reports.

        # Iterate through all selected PDF Reports.
        report_appliance_agreement = self.env.ref('tg_sign_app.signapp_field_report_appliance_agreement')
        report_biz_letter = self.env.ref('tg_sign_app.signapp_field_report_biz_letter')
        report_lease_addendum_crime_free = self.env.ref('tg_sign_app.signapp_field_report_lease_addendum_crime_free')
        report_garage_lease = self.env.ref('tg_sign_app.signapp_field_report_garage_lease')
        report_lease_rental_agreement = self.env.ref('tg_sign_app.signapp_field_report_lease_rental_agreement')
        report_lease_security_deposit = self.env.ref('tg_sign_app.signapp_field_report_lease_security_deposit')

        if self.landlord_name:
            # Fetch value for Role "Landlord" as Signature in PDF report
            sign_item_role_landlord = self.env['sign.item.role'].search([('name', '=', 'Landlord')], limit=1)
        #                sign_item_role_landlord = self.env.ref('tg_sign_app.sign_item_role_landlord')
        if self.tenant_name1:
            # Fetch value for Role "Tenant Name 1" as Signature in PDF report
#            sign_item_role_tenant1 = self.env['sign.item.role'].search([('name', '=', 'Tenant Name 1')], limit=1)
            sign_item_role_tenant1 = self.env.ref('tg_sign_app.sign_item_role_tenant_name_1')
        if self.tenant_name2:
            # Fetch value for Role "Tenant Name 2" as Signature in PDF report
#            sign_item_role_tenant2 = self.env['sign.item.role'].search([('name', '=', 'Tenant Name 2')], limit=1)
             sign_item_role_tenant2 = self.env.ref('tg_sign_app.sign_item_role_tenant_name_2')
        if self.tenant_name3:
            # Fetch value for Role "Tenant Name 3" as Signature in PDF report
#            sign_item_role_tenant3 = self.env['sign.item.role'].search([('name', '=', 'Tenant Name 3')], limit=1)
             sign_item_role_tenant3 = self.env.ref('tg_sign_app.sign_item_role_tenant_name_3')
        if self.tenant_ssn2:
            # Fetch value for Role "Tenant SSN 2" as Signature in PDF report
#            sign_item_role_ssn2 = self.env['sign.item.role'].search([('name', '=', 'Tenant - SSN 2')], limit=1)
             sign_item_role_ssn2 = self.env.ref('tg_sign_app.sign_item_role_tenant_ssn_2')

        sign_item_type = self.env['sign.item.type'].search([('item_type', '=', 'signature')], limit=1)

        # Tags will be auto created based on form data based on ordering -> 1 Tenannt Name 1 , 2. Landlord name, 3. Today’s date
        # If the Tag already exist than we don't have to create it again
        tag_ids = []
        date_name_str = str(self.todays_date.day) + '_' + str(self.todays_date.month) + '_' + str(self.todays_date.year)
        date_tag_str = str(self.todays_date.day) + '/' + str(self.todays_date.month) + '/' + str(self.todays_date.year)

        # Check for Tag- Today's Data already exist
        date_tag_exist = self.env['sign.template.tag'].search([('name', '=', date_tag_str)])
        if not date_tag_exist:
            val = {'name': date_tag_str}
            tag_todays_date = self.env['sign.template.tag'].create(val)
            tag_ids.append(tag_todays_date.id)
        else:
            tag_ids.append(date_tag_exist.id)

        # Check for Tag- Tenan't Name 1 already exist
        tenant_tag_exist = self.env['sign.template.tag'].search([('name', '=', self.tenant_name1)])
        if not tenant_tag_exist:
            val = {'name': self.tenant_name1}
            tag_tenant = self.env['sign.template.tag'].create(val)
            tag_ids.append(tag_tenant.id)
        else:
            tag_ids.append(tenant_tag_exist.id)

        # Check for Tag- Landlord Name already exist
        land_tag_exist = self.env['sign.template.tag'].search([('name', '=', self.landlord_name)])
        if not land_tag_exist:
            val = {'name': self.landlord_name}
            tag_landlord = self.env['sign.template.tag'].create(val)
            tag_ids.append(tag_landlord.id)
        else:
            tag_ids.append(land_tag_exist.id)

        for rec in self.pdf_report_selection:

            content = False
            ### Create Signature Item Role to be placed on PDF report based on exact match on roles we have created in Sign -> Configuration -> Roles

            rec_name = rec.name.replace(" ", "_")
            rec_name = rec_name.replace("-", "")
            file_name = rec_name.replace("__", "_")

            landlord_prfx = self.landlord_name.split(' ', 1)[0]

            if landlord_prfx:
                file_name = file_name + '_' + landlord_prfx
            tenant_prfx = self.tenant_name1.split(' ', 1)[0]

            if tenant_prfx:
                file_name = file_name + '_' + tenant_prfx
            file_name = file_name + '_' + date_name_str

            # file_name - Name of generated PDF File, by concatinate Report Name ,Land Lord's name first word , Tenant Name 1's first Word and today's date field

            if report_appliance_agreement and rec.id == report_appliance_agreement.id :
                content, _ = self.env['ir.actions.report']._render('tg_sign_app.action_report_wp_appliancemaintenanceagreement',self.ids)
            elif report_biz_letter and rec.id == report_biz_letter.id:
                content, _ = self.env['ir.actions.report']._render('tg_sign_app.action_report_wp_bizletter',self.ids)
            elif report_lease_addendum_crime_free and rec.id == report_lease_addendum_crime_free.id:
                content, _ = self.env['ir.actions.report']._render('tg_sign_app.action_report_wp_crimefreehousingaddendum',self.ids)
            elif report_garage_lease and rec.id == report_garage_lease.id:
                content, _ = self.env['ir.actions.report']._render('tg_sign_app.action_report_wp_garagelease',self.ids)
            elif report_lease_rental_agreement and rec.id == report_lease_rental_agreement.id:
                content, _ = self.env['ir.actions.report']._render('tg_sign_app.action_report_wp_lease_rental',self.ids)
            elif report_lease_security_deposit and rec.id == report_lease_security_deposit.id:
                content, _ = self.env['ir.actions.report']._render('tg_sign_app.action_report_lease_security_deposit',self.ids)

            if content :
                ######## create attachments #######
                attachment = self.env['ir.attachment'].create({
                    'name': file_name,
                    'datas': base64.b64encode(content),
                    'mimetype': 'application/pdf',
                })
                if attachment:
                    ######## create Template with attachment #######
                    template = self.env['sign.template'].create({
                        'name': file_name,
                        'attachment_id': attachment.id,
                        'tag_ids' :[(6,0,tag_ids)]
                    })

                    if template:
                        # for each report place signature for Landlord,Tenant Name 1, Tenant Name 2,Tenant Name 3 ,Tenant SSN 2 and place based on static postion defined
                        if report_appliance_agreement and rec.id == report_appliance_agreement.id:
                            ### Landlord ###
                            sign_item_val = {'template_id': template.id, 'page': 1,'posX':0.609,'posY':0.683,'width':0.200,'height': 0.025}

                            if sign_item_type:
                                sign_item_val.update({'type_id': sign_item_type.id})
                            if self.landlord_name and sign_item_role_landlord:
                                sign_item_val.update({'responsible_id': sign_item_role_landlord.id})
                            sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Landlord ###

                            ### Tenant Name 1 ###
                            sign_item_val = {'template_id': template.id,'page':1,'posX':0.123,'posY':0.683,'width':0.200,'height': 0.025}

                            if sign_item_type:
                                sign_item_val.update({'type_id': sign_item_type.id})
                            if self.tenant_name1 and sign_item_role_tenant1:
                                sign_item_val.update({'responsible_id':sign_item_role_tenant1.id})
                            sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Tenant Name 1 ###

                        elif report_lease_addendum_crime_free and rec.id == report_lease_addendum_crime_free.id:

                            ### Landlord ###
                            sign_item_val = {'template_id': template.id, 'page': 1,'posX':0.144,'posY':0.600,'width':0.200,'height': 0.025}

                            if self.landlord_name and sign_item_role_landlord:
                                sign_item_val.update({'responsible_id': sign_item_role_landlord.id})
                                if sign_item_type:
                                    sign_item_val.update({'type_id': sign_item_type.id})
                                sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Landlord ###

                            ### Tenant Name 1 ###
                            sign_item_val = {'template_id': template.id, 'page': 1, 'posX': 0.144, 'posY': 0.520,
                                             'width': 0.200, 'height': 0.025}

                            if self.tenant_name1 and sign_item_role_tenant1:
                                sign_item_val.update({'responsible_id': sign_item_role_tenant1.id})
                                if sign_item_type:
                                    sign_item_val.update({'type_id': sign_item_type.id})
                                sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Tenant Name 1 ###

                            ### Tenant Name 2 ###
                            sign_item_val = {'template_id': template.id, 'page': 1,'posX':0.615,'posY':0.520,'width':0.200,'height': 0.025}

                            if self.tenant_name2 and sign_item_role_tenant2:
                                sign_item_val.update({'responsible_id': sign_item_role_tenant2.id})
                                if sign_item_type:
                                    sign_item_val.update({'type_id': sign_item_type.id})
                                sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Tenant Name 2 ###

                            ### Tenant Name 3 ###
                            sign_item_val = {'template_id': template.id, 'page': 1, 'posX': 0.615, 'posY': 0.600,
                                             'width': 0.200, 'height': 0.025}
                            if self.tenant_name3 and sign_item_role_tenant3:
                                sign_item_val.update({'responsible_id': sign_item_role_tenant3.id})

                                if sign_item_type:
                                    sign_item_val.update({'type_id': sign_item_type.id})
                                sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Tenant Name 3 ###

                        elif report_garage_lease and rec.id == report_garage_lease.id:
                            ### Landlord ###
                            sign_item_val = {'template_id': template.id, 'page': 1,'posX':0.144,'posY':0.672,'width':0.200,'height': 0.025}

                            if sign_item_type:
                                sign_item_val.update({'type_id': sign_item_type.id})
                            if self.landlord_name and sign_item_role_landlord:
                                sign_item_val.update({'responsible_id': sign_item_role_landlord.id})
                            sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Landlord ###

                            ### Tenant Name 1 ###
                            sign_item_val = {'template_id': template.id,'page':1,'posX':0.590,'posY':0.672,'width':0.200,'height': 0.025}

                            if sign_item_type:
                                sign_item_val.update({'type_id': sign_item_type.id})
                            if self.tenant_name1 and sign_item_role_tenant1:
                                sign_item_val.update({'responsible_id':sign_item_role_tenant1.id})
                            sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Tenant Name 1 ###

                        elif report_lease_rental_agreement and rec.id == report_lease_rental_agreement.id:
                            ### Landlord ###
                            sign_item_val = {'template_id':template.id,'page': 6,'posX':0.125,'posY':0.195,'width':0.200,'height': 0.025}

                            if sign_item_type:
                                sign_item_val.update({'type_id': sign_item_type.id})
                            if self.landlord_name and sign_item_role_landlord:
                                sign_item_val.update({'responsible_id': sign_item_role_landlord.id})
                            sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Landlord ###

                            ### Tenant Name 1 ###
                            sign_item_val = {'template_id': template.id,'page':6,'posX':0.585,'posY':0.195,'width':0.200,'height': 0.025}

                            if sign_item_type:
                                sign_item_val.update({'type_id': sign_item_type.id})
                            if self.tenant_name1 and sign_item_role_tenant1:
                                sign_item_val.update({'responsible_id':sign_item_role_tenant1.id})
                            sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Tenant Name 1 ###

                            ### Tenant SSN2 ###
                            sign_item_val = {'template_id':template.id,'page':6,'posX':0.585,'posY':0.294,'width':0.200,'height': 0.025}

                            if sign_item_type:
                                sign_item_val.update({'type_id': sign_item_type.id})
                            if self.tenant_ssn2 and sign_item_role_ssn2:
                                sign_item_val.update({'responsible_id':sign_item_role_ssn2.id})
                            # sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Tenant SSN2 ###

                        elif report_lease_security_deposit and rec.id == report_lease_security_deposit.id:
                            ### Landlord ###
                            sign_item_val = {'template_id':template.id,'page': 1,'posX':0.610,'posY':0.416,'width':0.200,'height': 0.025}

                            if self.landlord_name and sign_item_role_landlord:
                                sign_item_val.update({'responsible_id': sign_item_role_landlord.id})
                                if sign_item_type:
                                    sign_item_val.update({'type_id': sign_item_type.id})
                                sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Landlord ###

                            ### Tenant Name 1 ###
                            sign_item_val = {'template_id':template.id,'page':1,'posX': 0.155,'posY':0.416,'width': 0.200, 'height': 0.025}

                            if self.tenant_name1 and sign_item_role_tenant1:
                                sign_item_val.update({'responsible_id': sign_item_role_tenant1.id})
                                if sign_item_type:
                                    sign_item_val.update({'type_id': sign_item_type.id})
                                sign_item_obj = self.env['sign.item'].create(sign_item_val)
                            ### Tenant Name 1 ###
