# analyzer/views.py
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from pandas.errors import EmptyDataError


def upload_csv(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect("analyze_csv", user_id=user.id)
    else:
        form = UserForm()
    return render(request, "upload_csv.html", {"form": form})


def analyze_csv(request, user_id):
    user = User.objects.get(id=user_id)
    csv_path = user.csv_file.path

    try:
        data = pd.read_csv(csv_path)

        if data.empty:
            raise EmptyDataError("The uploaded file is empty.")

        # Basic data analysis
        head = data.head().to_html()
        description = data.describe().to_html()

        # Handle missing values
        missing_values = data.isnull().sum().to_frame(name="Missing Values").to_html()

        # Generate histograms
        histograms = {}
        for column in data.select_dtypes(include=[np.number]).columns:
            plt.figure()
            sns.histplot(data[column].dropna(), kde=True)
            plt.title(f"Histogram of {column}")
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            image_base64 = base64.b64encode(image_png).decode("utf-8")
            histograms[column] = image_base64

        context = {
            "user": user,
            "head": head,
            "description": description,
            "missing_values": missing_values,
            "histograms": histograms,
        }
        return render(request, "analyze_csv.html", context)

    except EmptyDataError:
        return render(
            request,
            "analyze_csv.html",
            {
                "user": user,
                "error": "The uploaded CSV file is empty or contains no columns.",
            },
        )
    except Exception as e:
        return render(
            request,
            "analyze_csv.html",
            {
                "user": user,
                "error": f"An error occurred while processing the file: {e}",
            },
        )
