from django.urls import path
from .views import UploadCSV, DatasetList, DatasetDetail, DownloadPDF, ObtainAuthTokenView

urlpatterns = [
    path("upload/", UploadCSV.as_view()),
    path("history/", DatasetList.as_view()),
    path("datasets/<int:pk>/", DatasetDetail.as_view()),
    path('download_pdf/<int:pk>/', DownloadPDF.as_view(), name='download-pdf'),
    path("api-token-auth/", ObtainAuthTokenView.as_view()),
]
