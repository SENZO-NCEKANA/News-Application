"""
Forms for news application with validation and user-friendly interfaces.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User, Article, Publisher, Category, Newsletter, Subscription
)


class UserRegistrationForm(UserCreationForm):
    """
    Custom user registration form with role selection.
    """
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        """
        Meta options for UserRegistrationForm.
        """
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'role', 'password1', 'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class PublisherRegistrationForm(forms.ModelForm):
    """
    Form for publisher registration.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        """
        Meta options for PublisherRegistrationForm.
        """
        model = Publisher
        fields = ['name', 'description', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3
            }),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists")
        return email

    def save(self, commit=True):
        publisher = super().save(commit=False)
        if commit:
            publisher.save()

            # Create admin user for publisher
            try:
                user = User.objects.create_user(
                    username=self.cleaned_data['username'],
                    email=self.cleaned_data['email'],
                    password=self.cleaned_data['password1'],
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                    role='editor'
                )

                # Add user as editor to publisher
                publisher.editors.add(user)
            except Exception as e:
                # If user creation fails, delete the publisher
                publisher.delete()
                raise forms.ValidationError(f"Failed to create user: {str(e)}")

        return publisher


class ArticleForm(forms.ModelForm):
    """
    Form for creating and editing articles.
    """
    class Meta:
        """
        Meta options for ArticleForm.
        """
        model = Article
        fields = [
            'title', 'content', 'summary', 'publisher', 'category'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Enter article content'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter article summary (optional)'
            }),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'].queryset = Publisher.objects.all()
        self.fields['category'].queryset = Category.objects.all()


class ArticleApprovalForm(forms.ModelForm):
    """
    Form for editors to approve articles.
    """
    class Meta:
        """
        Meta options for ArticleApprovalForm.
        """
        model = Article
        fields = ['status', 'is_approved']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_approved': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}),
        }


class NewsletterForm(forms.ModelForm):
    """
    Form for creating newsletters.
    """
    class Meta:
        """
        Meta options for NewsletterForm.
        """
        model = Newsletter
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter newsletter title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Enter newsletter content'
            }),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'].queryset = Publisher.objects.all()


class SubscriptionForm(forms.ModelForm):
    """
    Form for managing subscriptions.
    """
    class Meta:
        """
        Meta options for SubscriptionForm.
        """
        model = Subscription
        fields = ['publisher', 'journalist']
        widgets = {
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'journalist': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'].queryset = Publisher.objects.all()
        self.fields['journalist'].queryset = User.objects.filter(
            role='journalist'
        )
        self.fields['publisher'].required = False
        self.fields['journalist'].required = False

    def clean(self):
        cleaned_data = super().clean()
        publisher = cleaned_data.get('publisher')
        journalist = cleaned_data.get('journalist')

        if not publisher and not journalist:
            raise forms.ValidationError(
                'You must subscribe to either a publisher or a journalist.'
            )

        return cleaned_data


class SearchForm(forms.Form):
    """
    Form for searching articles.
    """
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search articles...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        empty_label="All Publishers",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ForgotPasswordForm(forms.Form):
    """
    Form for requesting password reset.
    """
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )


class ResetPasswordForm(forms.Form):
    """
    Form for resetting password with token.
    """
    new_password1 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
        return cleaned_data
