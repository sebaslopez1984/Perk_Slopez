from decimal import Decimal
import json
from site import ENABLE_USER_SITE
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Empresa, Transaccion
import bunch
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
 
    
class EmpresaRechazos(View):
    def get(self, request):
        query = "select tr.id, sum(tr.price) as total, tr.idCompany, tr.company from api_transaccion tr"
        query += " inner join api_empresa em"
        query += " on em.id = tr.idCompany"
        query += " where status_approved = 'false'"
        query += " group by company"
        query += " order by total desc"
        query += " limit 1"
        
        empres = Transaccion.objects.raw(query)
        lista = []
        
        for i in empres:
            d = bunch.Bunch()
            d["Total"] = i.total
            d["IdCompany"] = i.idCompany
            d["Company"] = i.company
            
            lista.append((d))
        
        #jsonList = json.dumps(lista, cls = CustomJsonEncoder)
        datos = {'Api': "Empresa con mas rechazos",'Message' : "Success", 'Transaccion' : lista}  
        return JsonResponse(datos)
        
class EpresaMayorVentas(View):
    def get(self, request):
        query = "select tr.id, sum(tr.price) as total, tr.idCompany, tr.company"
        query +=" from api_transaccion tr"
        query +=" inner join api_empresa em"
        query +=" on em.id = tr.idcompany"
        query +=" where tr.status_transaction = 'Closed' and tr.status_approved = 'true'"
        query +=" group by tr.company"
        query +=" order by total desc"
        query +=" limit 1;"
        
        empres = Transaccion.objects.raw(query)
        lista = []
        
        for i in empres:
            d = bunch.Bunch()
            d["Total"] = i.total
            d["IdCompany"] = i.idCompany
            d["Company"] = i.company
            
            lista.append((d))
        
        #jsonList = json.dumps(lista, cls = CustomJsonEncoder)
        #print(jsonList)    
        datos = {'Api': "Empresa con más ventas",'Message' : "Success", 'Transaccion' : lista} 
        return JsonResponse(datos)
    
class EpresaMenorVentas(View):
    def get(self, request):
        query = "select tr.id, sum(tr.price) as total, tr.idCompany, tr.company"
        query +=" from api_transaccion tr"
        query +=" inner join api_empresa em"
        query +=" on em.id = tr.idcompany"
        query +=" where tr.status_transaction = 'closed' and tr.status_approved = 'true'"
        query +=" group by tr.company"
        query +=" order by total asc"
        query +=" limit 1;"
        
        empres = Transaccion.objects.raw(query)
        lista = []
        
        for i in empres:
            d = bunch.Bunch()
            d["Total"] = i.total
            d["IdCompany"] = i.idCompany
            d["Company"] = i.company
            
            lista.append((d))
        
        datos = {'Api': "Empresa con menos ventas",'Message' : "Success", 'Transaccion' : lista} 
        return JsonResponse(datos)
       
class PrecioTotalTransaccion(View):
    def get(self,request,status="", compani=""):
        nombre = compani.lower()
        estado = status.lower()
        print("estado" + estado)
        print("nombre" + nombre)
        lista = []
        if estado == 'true' or estado == "false":
            if nombre == 'true' or nombre == "false":
                if nombre ==  "false":    
                    query = "select tr.id, sum(tr.price) as TotalPrice, tr.status_approved from api_transaccion tr where status_approved = '{0}'".format(estado)
                    empres = Transaccion.objects.raw(query)
                    for i in empres:
                        d = bunch.Bunch()
                        d["Total"] = i.TotalPrice
                        d["status_approved"] = i.status_approved
                        #d["Company"] = i.company

                        lista.append((d))
                else:
                    query = "select id,sum(price) as TotalPrice, status_approved, company from api_transaccion where status_approved = '{0}' GROUP by company order by totalprice desc".format(estado)
                    empres = Transaccion.objects.raw(query)
                    for i in empres:
                        d = bunch.Bunch()
                        d["Total"] = i.TotalPrice
                        d["status_approved"] = i.status_approved
                        d["Company"] = i.company

                        lista.append((d))

                if estado == "True":
                    datos = {'Api': "Precio total de las transacciones que SÍ se cobraron",'Message' : "Success", 'Transaccion' : lista} 
                    return JsonResponse(datos)
                else:
                    datos = {'Api': "Precio total de las transacciones que NO se cobrarons",'Message' : "Success", 'Transaccion' : lista} 
                    return JsonResponse(datos)
            else:
                datos = {'Estado' : "Error", 'Message' : "Debe ingresar un True o False para continuar"} 
                return JsonResponse(datos)

        else:
            datos = {'Estado' : "Error", 'Message' : "Debe ingresar un True o False para continuar"} 
            return JsonResponse(datos)

class EmpresaCURL(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request,id=0):  
        if (id > 0):
            companies = list(Empresa.objects.filter(id=id).values())
            if len(companies) > 0:
                company = companies[0]
                datos = {'message': "Success", 'company': company}
            else:
                datos = {'message': "Company not found..."}
            return JsonResponse(datos)
        else:
            companies = list(Empresa.objects.values())
            if len(companies) > 0:
                datos = {'message': "Success", 'companies': companies}
            else:
                datos = {'message': "Companies not found..."}
            return JsonResponse(datos)
    
    def delete(self, request, id):
        companies = list(Empresa.objects.filter(id=id).values())
        if len(companies) > 0:
            Empresa.objects.filter(id=id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Company not found..."}
        return JsonResponse(datos)
    
    def put(self, request, id):
        jd = json.loads(request.body)
        companies = list(Empresa.objects.filter(id=id).values())
        if len(companies) > 0:
            company = Empresa.objects.get(id=id)
            company.Nombre = jd['Nombre']
            company.status = jd['status']
            company.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "No Existe la compania"}
        return JsonResponse(datos)
    
    def post(self, request):
       
        jd = json.loads(request.body)
        
        Empresa.objects.create(Nombre=jd['Nombre'], status=jd['status'])
        datos = {'message': "Success"}
        return JsonResponse(datos)