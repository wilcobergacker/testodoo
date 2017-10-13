# -*- coding: utf-8 -*-
{
    'name': 'VZ - Install',
    'version': '10.0.1.0.0',
    'category': 'Generic Module',
    'summary': 'Vitamine & Zo - Install',
    'author': 'ERP|OPEN',
    'depends': [
        #localisation first
        'vz_l10n_nl',
        'account_chart_template_multicompany',
        'vz_l10n_nl_reports',
        'vz_local',

        #Base
        'crm',
        'stock',
        'mrp',
        'sale_management',
        'stock_account',
        'mail',
        'account',
        'account_invoicing',
        'account_asset',
        'account_accountant',
        'mrp_mps',
        'quality',
        'quality_mrp',
        'mrp_workorder',
        'helpdesk',
        'purchase',
        'account_3way_match',
        'account_bank_statement_import',
        'account_bank_statement_import_camt',
        'account_cancel',
        'account_deferred_revenue',
        'account_extension',
        'account_reports',
        'account_sepa',
        'analytic',
        'auth_crypt',
        'auth_signup',
        'barcodes',
        'base',
        'base_iban',
        'base_import',
        'base_setup',
        'base_vat',
        'base_vat_autocomplete',
        'bus',
        'contacts',
        'currency_rate_live',
        'decimal_precision',
        'delivery',
        'fetchmail',
        #'l10n_nl',
        #'l10n_nl_reports',
        'mail_push',
        'mrp_account',
        'payment',
        'payment_transfer',
        'product',
        'product_margin',
        'purchase_mrp',
        'rating',
        'resource',
        'sale',
        'sale_crm',
        'sale_mrp',
        'sale_order_dates',
        'sales_team',
        'sale_stock',
        'sale_subscription',
        'sale_subscription_asset',
        'utm',
        'web',
        'web_clearbit',
        'web_diagram',
        'web_editor',
        'web_enterprise',
        'web_gantt',
        'web_grid',
        'web_kanban_gauge',
        'web_mobile',
        'web_planner',
        'web_settings_dashboard',
        'web_tour',
        'calendar',
        'portal',
        'http_routing',
        'crm_phone_validation',
        'phone_validation',
        'account_sepa_direct_debit',
        'web_studio',
        'fleet',
        'document',




        #Custom
        'vz_base',
        'vz_balance_sheet',
        'vz_profit_loss',
        'vz_subscription_planning',
        'vz_sale',
        'vz_product_display',





        # Community
        # 'account_cost_spread', not working 11
        #'account_tax_balance',
        #'auth_server_admin_passwd_passkey',
        #'base_optional_quick_create',
        'base_partner_sequence',
        'base_technical_features',
        'cancel_invoice_number',
        #'date_range',
        #'import_salary_journal_entries',
        # 'l10n_nl_tax_statement', not working 11
        #'max_web_freeze_list_view_header',
        'max_web_hide_list_view_import',
        'password_security',
        'web_disable_export_group',
        'account_credit_control',
        'l10n_nl_bank',
        #'account_invoice_default_account',
        #'crm_tags_interest',
        #'bi_mass_invoices_send_by_email',
        'partner_contact_type_display',
        'sale_order_type',
        'crm_tags_interest',

    ],
    'data': [],
    'installable': True,
}
