from django import forms
from .models import Vehicle, WasteTransfer, Path, Workforce_WorkHours, Workforce


class WorkforceWorkHoursForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(WorkforceWorkHoursForm, self).__init__(*args, **kwargs)
        self.fields['workforce'].queryset = Workforce.objects.filter(
            user=user)
        self.fields['workforce'].initial = Workforce.objects.filter(
            user=user).first()

    class Meta:
        model = Workforce_WorkHours
        fields = ['workforce', 'login_time', 'logout_time']
        widgets = {
            'login_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'logout_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class WorkforceRegistrationForm(forms.Form):
    email = forms.EmailField(label='Email')
    start_date = forms.DateField(
        label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(
        label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    job_title = forms.CharField(label='Job Title', max_length=100)
    payment_rate_per_hour = forms.DecimalField(
        label='Payment Rate Per Hour', max_digits=10, decimal_places=2)


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'type', 'capacity',
                  'loaded_fuel_cost_per_km', 'unloaded_fuel_cost_per_km']


class WasteTransferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WasteTransferForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(
            status='Available')

    class Meta:
        model = WasteTransfer
        fields = ['landfill', 'vehicle',  'volume', ]


class WasteTransferForm_Path(forms.ModelForm):
    def __init__(self, sts, landfill, *args, **kwargs):
        super(WasteTransferForm_Path, self).__init__(*args, **kwargs)
        self.fields['path'].queryset = Path.objects.filter(
            sts=sts, landfill=landfill)

    class Meta:
        model = WasteTransfer
        fields = ['path']
