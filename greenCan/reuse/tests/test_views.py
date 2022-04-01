from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from PIL import Image as Img
from six import BytesIO
from recycle.models import ZipCode
from reuse.models import Image, Post

from reuse.models import NGOLocation

User = get_user_model()


def create_image(
    storage, filename, size=(100, 100), image_mode="RGB", image_format="PNG"
):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Img.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class TestCreatePost(TestCase):
    def setUp(self):
        self.url = reverse("reuse:create-post")
        self.redirect_url = reverse("reuse:donation-page")
        self.login_redirect_url = reverse("accounts:login") + "?next=" + self.url
        image = create_image(None, "test.png")
        image_file = SimpleUploadedFile("test.png", image.getvalue())
        image2 = create_image(None, "test2.png")
        image_file2 = SimpleUploadedFile("test2.png", image2.getvalue())
        self.data = {
            "file[]": [image_file, image_file2],
            "title": "Bed",
            "description": "Twin bed",
            "zipcode": "10001",
            "number": "9999999998",
            "email": "kevin@gmail.com",
            "category": "Furniture",
        }

        zipcode = ZipCode(
            zip_code="10001",
            state_id="NY",
            state="New York",
            borough="Manhattan",
            centroid_latitude=40.75021293296376,
            centroid_longitude=-73.99692994900218,
            polygon="",
        )
        zipcode.save()

    def test_unauthenticated(self):
        response = self.client.post(self.url, data=self.data, follow=True)
        self.assertRedirects(response, self.login_redirect_url, 302)
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)

    def test_auth_valid_form(self):
        data = self.data.copy()
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 1)
        images = Image.objects.all()
        self.assertEquals(len(images), 2)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_1(self):
        data = self.data.copy()
        del data["title"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_2(self):
        data = self.data.copy()
        del data["description"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_3(self):
        data = self.data.copy()
        del data["zipcode"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_4(self):
        data = self.data.copy()
        del data["category"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_5(self):
        data = self.data.copy()
        data["zipcode"] = "10002"
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        self.assertRedirects(response, self.redirect_url, 302)


class TestViews(TestCase):
    def setUp(self):
        self.index_url = reverse("reuse:index")
        self.donation_page_url = reverse("reuse:donation-page")
        self.listing_page_url = reverse("reuse:listing-page")
        self.create_post_url = reverse("reuse:create-post")
        self.ngo_location_url = reverse("reuse:ngo-donation")
        self.search_ngo_locations_url = reverse("reuse:fetch-ngo-locations")
        self.client = Client()
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])

        zipcode = ZipCode(
            zip_code="10001",
            state_id="NY",
            state="New York",
            borough="Manhattan",
            centroid_latitude=40.75021293296376,
            centroid_longitude=-73.99692994900218,
            polygon="",
        )
        zipcode.save()
        post = Post(
            title="Apple",
            category="Books",
            phone_number="9175185345",
            email="pb2640@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=user,
        )
        post.save()
        self.zipcode = zipcode
        ngo_location = NGOLocation(
            zip_code=zipcode,
            latitude=40.75021293296376,
            longitude=-73.99692994900218,
            items_accepted="Food",
            email="tandon@nyu.edu",
            phone="2121112011",
            address="101 Willoughby street",
            hours="Open on everyday",
            website="www.recycle.com",
        )
        ngo_location.save()
        self.ngo_location = ngo_location

    def test_index_GET(self):
        """
        test to check if reuse home page is returning a valid response
        """

        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reuse-index.html")

    def test_donationpage_GET(self):
        """
        test to check if donation page is returning a valid response
        """

        response = self.client.get(self.donation_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reuse/templates/donate-item-page.html")

    def test_listing_page_GET(self):
        """
        test to check if listing page is returning a valid response
        """

        response = self.client.get(self.listing_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "listing-page.html")

    def test_listing_page_search_GET(self):
        """
        test to check if search is returning a valid response
        """
        response = self.client.get("%s?q=%s" % (reverse("reuse:listing-page"), "book"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "listing-page.html")

    def test_ngo_location_GET(self):
        """
        test to check if ngo page is returning a valid response
        """

        response = self.client.get(self.ngo_location_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reuse/templates/ngo-donation.html")

    def test_query_search_context_filter(self):
        """
        Test to check if on making a query something is being returned to the view
        """

        response = self.client.get("%s?q=%s" % (reverse("reuse:listing-page"), "book"))

        self.assertTrue(len(response.context["posts"]) >= 0)

    def test_query_search_returns(self):
        """
        Test to check if I search for an item which is present, it should return something
        """

        response = self.client.get("%s?q=%s" % (reverse("reuse:listing-page"), "book"))

        self.assertTrue(len(response.context["posts"]) >= 1)

    def test_query_search_does_not_return(self):
        """
        Test to check if I search for an item which is not present, it should return nothing
        """

        response = self.client.get(
            "%s?q=%s" % (reverse("reuse:listing-page"), "veryrandomstring")
        )

        self.assertTrue(len(response.context["posts"]) == 0)

    def test_ngo_locations1(self):
        """
        test to check if searching by input zip code is returning a valid response
        """

        response = self.client.get(
            self.search_ngo_locations_url
            + "?type=live-location&latitude=40.7362&longitude=-74.0422"
        )

        self.assertEquals(response.status_code, 200)

    def test_ngo_locations2(self):
        """
        test to check if searching by user's current location is returning a valid response
        """

        response = self.client.get(
            self.search_ngo_locations_url + "?type=zipcode&zipcode=10004"
        )

        self.assertEquals(response.status_code, 200)

    def test_ngo_locations_invalid_data(self):
        """
        test to check if searching by user's current location is returning a valid response
        """

        response = self.client.get(
            self.search_ngo_locations_url + "?type=somerandomstring"
        )

        self.assertEquals(response.status_code, 200)
        self.assertContains(
            response.json, {"err_flg": True, "err_msg": "Invalid arguments provided"}
        )
