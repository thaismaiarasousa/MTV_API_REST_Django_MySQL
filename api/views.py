from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Company
import json
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# pylint: disable=E1101
class CompanyView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                company = Company.objects.get(id=id)
                datos = {'message': "Success", 'company': {'id': company.id, 'name': company.name, 'website': company.website, 'foundation': company.foundation}}
            except Company.DoesNotExist:
                datos = {'message': "Company not found..."}
            return JsonResponse(datos)
        
        else:
            companies = Company.objects.all()
            if companies:
                companies_data = [{'id': company.id, 'name': company.name, 'website': company.website, 'foundation': company.foundation} for company in companies]
                datos = {'message': "Success", 'companies': companies_data}
            else:
                datos = {'message': "Companies not found..."}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        company = Company.objects.create(name=jd['name'], website=jd['website'], foundation=jd['foundation'])
        datos = {'message': "Success", 'company': {'id': company.id, 'name': company.name, 'website': company.website, 'foundation': company.foundation}}

        # Geração do token JWT
        serializer = TokenObtainPairSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["access"]
        datos['token'] = str(token)

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            company = Company.objects.get(id=id)
            company.name = jd['name']
            company.website = jd['website']
            company.foundation = jd['foundation']
            company.save()
            datos = {'message': "Success"}
        except Company.DoesNotExist:
            datos = {'message': "Company not found..."}
        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            company = Company.objects.get(id=id)
            company.delete()
            datos = {'message': "Success"}
        except Company.DoesNotExist:
            datos = {'message': "Company not found..."}
        return JsonResponse(datos)
