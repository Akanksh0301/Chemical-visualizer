from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings

from .models import Dataset
from .serializers import DatasetSerializer

import pandas as pd
import os
from django.http import FileResponse, Http404
from io import BytesIO

# PDF / Chart libs
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

NUMERIC_COLUMNS = ['Flowrate','Pressure','Temperature']

def compute_summary(df: pd.DataFrame):
    # normalize column names
    df.columns = df.columns.str.strip().str.lower()

    total_count = len(df)
    averages = {}
    numeric_cols = ['flowrate','pressure','temperature']
    for col in numeric_cols:
        if col in df.columns:
            series = pd.to_numeric(df[col], errors='coerce').dropna()
            averages[col.capitalize()] = float(series.mean()) if not series.empty else None

    type_dist = {}
    if 'type' in df.columns:
        type_dist = df['type'].dropna().astype(str).value_counts().to_dict()

    return {
        'total_count': total_count,
        'averages': averages,
        'type_distribution': type_dist
    }

# ---------------- CSV Upload ---------------- #
class UploadCSV(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        f = request.FILES.get('file')
        if not f:
            return Response({"detail":"No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        ds = Dataset(original_filename=f.name)
        ds.file.save(f.name, f, save=False)
        ds.row_count = 0
        ds.set_summary({})
        ds.save()

        file_path = ds.file.path
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            try:
                os.remove(file_path)
            except:
                pass
            ds.delete()
            return Response({"detail":"Invalid CSV", "error": str(e)}, status=400)

        summary = compute_summary(df)
        ds.row_count = len(df)
        ds.set_summary(summary)
        ds.save()

        # keep only last 5 datasets
        all_ds = list(Dataset.objects.order_by('-uploaded_at'))
        if len(all_ds) > 5:
            for old in all_ds[5:]:
                try:
                    os.remove(old.file.path)
                except:
                    pass
                old.delete()

        return Response({"id": ds.id, "summary": summary}, status=201)

# ---------------- History API ---------------- #
class DatasetList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DatasetSerializer

    def get_queryset(self):
        return Dataset.objects.order_by('-uploaded_at')[:5]

# ---------------- Dataset Detail ---------------- #
class DatasetDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

# ---------------- PDF Download ---------------- #
class DownloadPDF(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            ds = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            raise Http404

        summary = ds.get_summary()
        buffer = BytesIO()

        with PdfPages(buffer) as pp:
            # Page 1: text
            fig, ax = plt.subplots(figsize=(8.27, 11.69))
            ax.axis('off')
            lines = [
                f"Report: {ds.original_filename}",
                f"Uploaded: {ds.uploaded_at}",
                f"Rows: {ds.row_count}",
                "",
                "Averages:"
            ]
            for k, v in summary.get('averages', {}).items():
                lines.append(f"  {k}: {v if v is not None else 'N/A'}")
            lines.append("")
            lines.append("Type distribution:")
            for k, v in summary.get('type_distribution', {}).items():
                lines.append(f"  {k}: {v}")

            y = 1.0
            for line in lines:
                ax.text(0.01, y, line, fontsize=10, transform=ax.transAxes, va='top')
                y -= 0.035
            pp.savefig(fig)
            plt.close(fig)

            # Page 2: type distribution bar chart
            type_dist = summary.get('type_distribution', {})
            if type_dist:
                fig2, ax2 = plt.subplots(figsize=(8,4))
                labels = list(type_dist.keys())
                vals = list(type_dist.values())
                ax2.bar(labels, vals)
                ax2.set_title('Type distribution')
                ax2.set_ylabel('Count')
                pp.savefig(fig2)
                plt.close(fig2)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'report_{ds.id}.pdf')

# ---------------- Token Auth ---------------- #
class ObtainAuthTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
