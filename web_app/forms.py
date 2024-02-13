from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Fieldset, Layout, HTML
from django import forms

from web_app.models import Product


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Почта")
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput())
    repeat_password = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit",
                                     "Зарегистрироваться",
                                     css_class="w-100"))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["repeat_password"]:
            self.add_error("repeat_password", "Пароли не совпадают")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit",
                                     "Войти",
                                     css_class="w-100"))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "product_type", "price", "photo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["enctype"] = "multipart/form-data"
        self.helper.layout = Layout(
            Fieldset(
                "Новый товар",
                "title",
                "description",
                "product_type",
                "price",
                "photo"
            ),
            FormActions(
                Submit('save', 'Сохранить изменения'),
                Button('cancel', 'Отмена')),

        )


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "product_type", "price", "photo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["enctype"] = "multipart/form-data"
        self.helper.layout = Layout(
            Fieldset(
                "Редактирование товара",
                "title",
                "description",
                "product_type",
                "price",
                "photo"
            ),
            FormActions(
                Submit('save', 'Сохранить изменения'),
                HTML("<a class=\"btn btn-danger\" href=\"/\">Отмена</a>"))
        )
