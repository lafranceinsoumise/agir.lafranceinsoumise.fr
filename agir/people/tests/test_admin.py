from django.test import TestCase
from django.urls import reverse

from agir.people.models import Person, PersonTag, PersonForm, PersonFormSubmission


class AddEmailTestCase(TestCase):
    def setUp(self) -> None:
        self.admin = Person.objects.create_superperson(
            "admin@agir.local", password="truc"
        )
        self.user1 = Person.objects.create_insoumise("user1@agir.local")
        self.user2 = Person.objects.create_insoumise("user2@agir.local")

        self.client.force_login(
            self.admin.role, backend="agir.people.backend.PersonBackend"
        )

        self.change_url = reverse("admin:people_person_change", args=[self.user1.pk])
        self.add_email_url = reverse(
            "admin:people_person_addemail", args=[self.user1.pk]
        )
        self.merge_url = f'{reverse("admin:people_person_merge")}?id={self.user1.pk}&id={self.user2.pk}'

    def test_can_display_pages(self):
        res = self.client.get(self.add_email_url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'name="email"')

        res = self.client.get(self.merge_url)
        self.assertEqual(res.status_code, 200)

        self.assertContains(res, f'value="{self.user1.pk}"')
        self.assertContains(res, f'value="{self.user2.pk}"')

    def test_can_add_email(self):
        res = self.client.post(self.add_email_url, data={"email": "user1@example.com"})
        self.assertRedirects(res, self.change_url)

        self.assertEqual(self.user1.email, "user1@example.com")

    def test_can_merge_people(self):
        res = self.client.post(self.add_email_url, data={"email": "user2@agir.local"})
        self.assertRedirects(res, self.merge_url)

        res = self.client.post(
            self.merge_url, data={"primary_account": str(self.user1.pk)}
        )
        self.assertRedirects(res, self.change_url)

        self.assertFalse(Person.objects.filter(pk=self.user2.pk).exists())

        self.assertCountEqual(
            [e.address for e in self.user1.emails.all()],
            ["user1@agir.local", "user2@agir.local"],
        )


class PeopleAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.admin = Person.objects.create_superperson(
            "admin@agir.local", password="truc"
        )
        self.user1 = Person.objects.create_insoumise("user1@agir.local")

        self.tag = PersonTag.objects.create(label="tag")

        self.person_form = PersonForm.objects.create(
            title="Formulaire simple",
            slug="formulaire-simple",
            description="Ma description simple",
            confirmation_note="Ma note de fin",
            main_question="QUESTION PRINCIPALE",
            send_answers_to="test@example.com",
            send_confirmation=True,
            custom_fields=[
                {
                    "title": "Profil",
                    "fields": [{"id": "contact_phone", "person_field": True}],
                }
            ],
        )

        self.client.force_login(
            self.admin.role, backend="agir.people.backend.PersonBackend"
        )

    def test_can_display_pages(self):
        views = [
            ("admin:people_person_changelist", ()),
            ("admin:people_person_change", (self.user1.pk,)),
            ("admin:people_persontag_changelist", ()),
            ("admin:people_persontag_change", (self.tag.pk,)),
            ("admin:people_personform_changelist", ()),
            ("admin:people_personform_change", (self.person_form.pk,)),
        ]

        for view, args in views:
            res = self.client.get(reverse(view, args=args))
            self.assertEqual(
                res.status_code, 200, msg=f"La vue '{view}' devrait renvoyer 200."
            )


class PersonFormAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.admin = Person.objects.create_superperson(
            "admin@agir.local", password="truc"
        )
        self.user1 = Person.objects.create_insoumise("user1@agir.local")

        self.person_form = PersonForm.objects.create(
            title="Formulaire simple",
            slug="formulaire-simple",
            description="Ma description simple",
            confirmation_note="Ma note de fin",
            send_confirmation=True,
            custom_fields=[
                {
                    "title": "Profil",
                    "fields": [{"id": "contact_phone", "person_field": True}],
                }
            ],
        )

        self.submission = PersonFormSubmission.objects.create(
            person=self.user1,
            form=self.person_form,
            data={"contact_phone": "+3362345678"},
        )

        self.client.force_login(
            self.admin.role, backend="agir.people.backend.PersonBackend"
        )

    def test_can_see_submission_admin_page(self):
        for view_name in ["change", "delete", "detail"]:
            res = self.client.get(
                reverse(
                    f"admin:people_personformsubmission_{view_name}",
                    args=[self.submission.pk],
                )
            )
            self.assertEqual(res.status_code, 200)

    def test_get_404_with_wrong_submission_id(self):
        for view_name in ["change", "delete", "detail"]:
            res = self.client.get(
                reverse(f"admin:people_personformsubmission_{view_name}", args=[9536])
            )
            self.assertEqual(res.status_code, 404)
