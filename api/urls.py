from django.urls import path
from .views import EmpresaRechazos,EpresaMayorVentas,EpresaMenorVentas,PrecioTotalTransaccion,EmpresaCURL,PrecioTotalTransaccion

urlpatterns = [
    path('empresarechazos/', EmpresaRechazos.as_view(), name='empresa_rechazos'),
    path('empresamayorvta/', EpresaMayorVentas.as_view(), name='empresa_mayor_vtas'),
    path('empresamenorvta/', EpresaMenorVentas.as_view(), name='empresa_menor_vtas'),
    path('preciototal/<str:status>/<str:compani>', PrecioTotalTransaccion.as_view(), name='precio_total'),  
    path('empresa/<int:id>', EmpresaCURL.as_view(), name='empresa_process'),
    path('empresa/', EmpresaCURL.as_view(), name='empresa_process'),
]
