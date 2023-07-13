from django.test import TestCase, Client
from django.urls import reverse
from .models import Company
import json

class CompanyViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        
        # pylint: disable=no-member
        self.company1 = Company.objects.create(name='Company 1', website='www.company1.com', foundation='2021')
        self.company2 = Company.objects.create(name='Company 2', website='www.company2.com', foundation='2022')
        self.company3 = Company.objects.create(name='Company 3', website='www.company3.com', foundation='2023')

    def test_get_all_companies(self):
        response = self.client.get(reverse('companies_list'))
        companies = response.json()['companies']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(companies), 3)

    def test_get_company_by_id(self):
        response = self.client.get(reverse('companies_process', args=[self.company1.id]))
        company = response.json()['company']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(company['name'], 'Company 1')

    def test_get_company_by_invalid_id(self):
        response = self.client.get(reverse('companies_process', args=[999]))
        message = response.json()['message']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Company not found...')

    def test_create_company(self):
        new_company = {
            'name': 'New Company',
            'website': 'www.newcompany.com',
            'foundation': '2023'
        }
        response = self.client.post(reverse('companies_list'), json.dumps(new_company), content_type='application/json')
        message = response.json()['message']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Success')

    def test_update_company(self):
        updated_company = {
            'name': 'Updated Company',
            'website': 'www.updatedcompany.com',
            'foundation': '2023'
        }
        response = self.client.put(reverse('companies_process', args=[self.company1.id]), json.dumps(updated_company), content_type='application/json')
        message = response.json()['message']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Success')
        
        # pylint: disable=no-member
        updated_company_data = Company.objects.get(id=self.company1.id)
        self.assertEqual(updated_company_data.name, 'Updated Company')
        self.assertEqual(updated_company_data.website, 'www.updatedcompany.com')
        self.assertEqual(str(updated_company_data.foundation), '2023')

    def test_update_company_with_invalid_id(self):
        updated_company = {
            'name': 'Updated Company',
            'website': 'www.updatedcompany.com',
            'foundation': '2023'
        }
        response = self.client.put(reverse('companies_process', args=[999]), json.dumps(updated_company), content_type='application/json')
        message = response.json()['message']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Company not found...')

    def test_delete_company(self):
        response = self.client.delete(reverse('companies_process', args=[self.company1.id]))
        message = response.json()['message']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Success')
        
        # pylint: disable=no-member
        remaining_companies = Company.objects.count()
        self.assertEqual(remaining_companies, 2)

    def test_delete_company_with_invalid_id(self):
        response = self.client.delete(reverse('companies_process', args=[999]))
        message = response.json()['message']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Company not found...')

