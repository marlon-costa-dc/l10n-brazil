# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests.common import TransactionCase


class L10nBrCoaGeneric(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.l10n_br_company = cls.env["res.company"].create(
            {"name": "Empresa Teste do Plano de Contas CFC"}
        )

    def test_l10n_br_coa_generic(self):
        """Test installing the chart of accounts template in a new company"""

        chart_template = self.env["account.chart.template"]
        chart_template.try_loading(
            "br_oca_generic", self.l10n_br_company, install_demo=True
        )

        # Verify the chart template was loaded
        self.assertEqual(self.l10n_br_company.chart_template, "br_oca_generic")

        # Verify anglo saxon accounting is enabled
        self.assertTrue(self.l10n_br_company.anglo_saxon_accounting)

    def test_guess_brazilian_chart(self):
        """A Brazilian company is never proposed the br_oca parent, which has
        no income/expense accounts, once a complete chart is installed."""
        chart_template = self.env["account.chart.template"]
        guess = chart_template._guess_chart_template(self.env.ref("base.br"))
        self.assertNotEqual(guess, "br_oca")
        self.assertEqual(
            chart_template._get_chart_template_mapping()[guess]["parent"], "br_oca"
        )
