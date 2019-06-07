from unittest.mock import patch

from django.test import TransactionTestCase, RequestFactory
from django.urls import reverse

from agir.api.redis import using_redislite
from agir.loans import views
from agir.loans.loan_config import LoanConfiguration
from agir.loans.views import generate_and_send_contract, loan_notification_listener
from agir.payments.actions import complete_payment
from agir.payments.models import Payment
from agir.people.models import Person


def contract_path(payment):
    return "contract.pdf"


loan_payment_type = LoanConfiguration(
    id="sample_loan",
    label="Prêts exemple",
    contract_path=contract_path,
    contract_template_name="loans/sample/contract.md",
    pdf_layout_template_name="loans/sample/contract_layout.html",
)


class LoansTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        from agir.payments.types import register_payment_type

        register_payment_type(loan_payment_type)

    @classmethod
    def tearDownClass(cls):
        from agir.payments.types import PAYMENT_TYPES

        del PAYMENT_TYPES[loan_payment_type.id]

    def setUp(self):
        self.p1 = Person.objects.create_person("test@test.com")

        self.loan_information_payload = {
            "amount": "40000",
            "first_name": "Nathalie",
            "last_name": "Kaplan",
            "gender": "F",
            "nationality": "FR",
            "date_of_birth": "01/07/1974",
            "country_of_birth": "FR",
            "city_of_birth": "Paris",
            "departement_of_birth": "75",
            "location_address1": "18 rue Rémy Dumoncel",
            "location_address2": "",
            "location_zip": "75014",
            "location_city": "Paris",
            "location_country": "FR",
            "contact_phone": "06 45 78 98 45",
            "iban": "FR31 3006 6119 2936 7522 3821 795",
            "declaration": "Y",
            "payment_mode": "system_pay",
        }

        self.ask_amount_view = views.BaseLoanAskAmountView.as_view(
            success_url="/success/", payment_type="sample_loan"
        )
        self.personal_information_view = views.BaseLoanPersonalInformationView.as_view(
            base_redirect_url="/base_redirect/",
            success_url="/success/",
            payment_type="sample_loan",
        )
        self.contract_view = views.BaseLoanAcceptContractView.as_view(
            payment_type="sample_loan"
        )

        self.factory = RequestFactory()

    def get(self, url):
        req = self.factory.get(url)
        req.user = self.factory.user
        req.session = self.factory.session
        return req

    def post(self, url, data=None):
        req = self.factory.post(url, data=data)
        req.user = self.factory.user
        req.session = self.factory.session
        return req

    @using_redislite
    @patch("django.db.transaction.on_commit")
    def test_can_make_a_loan_when_logged_in(self, on_commit):
        self.factory.user = self.p1.role
        self.factory.session = {}

        res = self.ask_amount_view(self.get("/amount"))
        self.assertEqual(res.status_code, 200)

        res = self.ask_amount_view(self.post("/amount", {"amount": "400"}))
        self.assertRedirects(res, "/success/", fetch_redirect_response=False)

        res = self.personal_information_view(self.get("/info"))
        self.assertEqual(res.status_code, 200)

        res = self.personal_information_view(
            self.post("/info", self.loan_information_payload)
        )
        self.assertRedirects(res, "/success/", fetch_redirect_response=False)

        res = self.contract_view(self.get("/contract/"))
        self.assertEqual(res.status_code, 200)

        res = self.contract_view(self.post("/contract/", data={"acceptance": "Y"}))
        # no other payment
        payment = Payment.objects.get()
        self.assertRedirects(
            res,
            reverse("payment_page", args=(payment.pk,)),
            fetch_redirect_response=False,
        )

        res = self.client.get(reverse("payment_return", args=(payment.pk,)))
        self.assertEqual(res.status_code, 200)

        self.p1.refresh_from_db()

        # assert fields have been saved on model
        for f in [
            "first_name",
            "last_name",
            "location_address1",
            "location_address2",
            "location_zip",
            "location_city",
            "location_country",
        ]:
            self.assertEqual(getattr(self.p1, f), self.loan_information_payload[f])

        # fake systempay webhook
        complete_payment(payment)

        loan_notification_listener(payment)

        on_commit.assert_called_once()
        partial = on_commit.call_args[0][0]

        self.assertEqual(partial.func, generate_and_send_contract)
        self.assertEqual(partial.args, (payment.id,))
