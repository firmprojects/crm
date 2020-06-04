from django.urls import path, include
from .views import (
    EstimatesView,
    CreateEstimate,
    EstimateDetail,
    EstimateUpdate,
    EstimateDelete,

    InvoiceView,
    CreateInvoice,
    InvoiceDetail,
    InvoiceUpdate,
    InvoiceDelete,
    PaymentsView,
    ProvidentFundView,
    ExpensesView,
    CreateTaxes,
    TaxUpdate,
    TaxDelete,
    ClientAutocompletesView,
    ProjectAutocompletesView

)


app_name = 'crm_accounts'
urlpatterns = [
    path('estimates/', EstimatesView.as_view(), name='estimates'),
    path('estimates/<int:pk>', EstimateDetail.as_view(), name='estimate_detail'),
    path('estimates/edit/<int:pk>',
         EstimateUpdate.as_view(), name='edit_estimate'),
    path('estimates/delete/<int:pk>',
         EstimateDelete.as_view(), name='delete_estimate'),
    path('create_estimates/', CreateEstimate.as_view(), name='create'),
    path('invoices/', InvoiceView.as_view(), name='invoices'),
    path('invoices/<int:pk>', InvoiceDetail.as_view(), name='invoice_detail'),
    path('invoices/edit/<int:pk>',
         InvoiceUpdate.as_view(), name='edit_invoice'),
    path('invoices/delete/<int:pk>',
         InvoiceDelete.as_view(), name='delete_invoice'),
    path('create_invoices/', CreateInvoice.as_view(), name='invoice_create'),
    path('payments/', PaymentsView.as_view(), name='payments'),
    path('providentfund/', ProvidentFundView.as_view(), name='providentfund'),
    path('expenses/', ExpensesView.as_view(), name='expenses'),
    path('taxes/', CreateTaxes.as_view(), name='taxes'),
    path('taxes/<int:pk>/update', TaxUpdate.as_view(), name='edit_tax'),
    path('taxes/<int:pk>/delete', TaxDelete.as_view(), name='delete_tax'),
    path('client_autocomplete/', ClientAutocompletesView.as_view(), name="client-autocomplete"),
    path('project_autocomplete/', ProjectAutocompletesView.as_view(), name="project-autocomplete")

]
