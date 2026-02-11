from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Document
from employee.models import Employee


# ✅ Inline DocumentForm (instead of forms.py)
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['employee', 'document_type', 'file']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DocumentForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['employee'].queryset = Employee.objects.filter(user=user)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from .models import Document  # Adjust import as needed

@login_required
def document_list(request):
    query = request.GET.get('q', '').strip()
    documents = Document.objects.filter(employee__user=request.user)

    if query:
        documents = documents.filter(
            Q(employee__full_name__icontains=query) |
            Q(document_type__icontains=query)
        )

    return render(request, 'document/document_list.html', {'documents': documents})


# ✅ Document Upload
@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        doc_type = request.POST.get("document_type")
        employee = request.POST.get("employee")

        if doc_type == "Educational Certificates":
            files = request.FILES.getlist('multi_files')
            for f in files:
                Document.objects.create(
                    employee_id=employee,
                    user=request.user,
                    document_type=doc_type,
                    file=f
                )
            messages.success(request, "📚 Educational documents uploaded successfully!")
            return redirect('document_list')
        else:
            if form.is_valid():
                document = form.save(commit=False)
                document.user = request.user
                document.save()
                messages.success(request, "📎 Document uploaded successfully!")
                return redirect('document_list')
    else:
        form = DocumentForm(user=request.user)

    return render(request, 'document/document_upload.html', {'form': form})


# ✅ Document Edit (via slug)
@login_required
def document_edit(request, slug):
    doc = get_object_or_404(Document, slug=slug, user=request.user)
    form = DocumentForm(request.POST or None, request.FILES or None, instance=doc, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Document updated successfully!")
        return redirect('document_list')
    return render(request, 'document/document_form.html', {'form': form})


# ✅ Document Delete (via slug)
@login_required
def document_delete(request, slug):
    doc = get_object_or_404(Document, slug=slug, user=request.user)
    doc.delete()
    messages.success(request, "🗑️ Document deleted successfully!")
    return redirect('document_list')
