from django import forms
from beam.models import *
from django.db import models
from crispy_forms.helper import FormHelper 

class addPointLoad(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(addInvoice, self).__init__(*args, **kwargs)
    helper = FormHelper()
    helper.form_show_labels = False

    index = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'form-index'}))
    magnitude = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'form-magnitude'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'form-location'}))

    def save(self):
        data = self.cleaned_data

        # cust = customer.objects.get(pk = data['cust_id'])
        # print('cust', type(cust))
        # prod = product.objects.get(pk = data['prod_id'])
        # print('prod', prod)
        # price = data['price'] * data['quant']
        # print('price', price)

        pointLoad.objects.create(index=data['index'], magnitude=data['magnitude'], location=data['location'])