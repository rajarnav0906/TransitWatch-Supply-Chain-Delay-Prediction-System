from flask import Flask, jsonify, render_template, request, make_response, Response
from delay_engine import estimate_delay
from xhtml2pdf import pisa
from io import BytesIO
import csv


PDF_FILENAME = "shipment_prediction.pdf"
CSV_FILENAME = "shipment_prediction.csv"
SUMMARY_TEMPLATE = {
    "delay": 3,
    "reason": "Heavy rainfall along the route",
    "route_type": "Fastest",
    "transport_mode": "Road",
    "carrier_name": "Blue Dart",
    "weather_impact": "High",
    "risk_score": 87,
    "suggested_action": "Switch to Rail mode or re-route via NH48",
}


def _clone_summary_payload():
    """Return a mutable copy of the canned report payload."""
    return dict(SUMMARY_TEMPLATE)


def _collect_form_payload(form_data):
    """Map user form input to the model-friendly structure."""
    return {
        "distance_km": float(form_data["distance_km"]),
        "vehicle_type": form_data["vehicle_type"],
        "vendor_rating": int(form_data["vendor_rating"]),
        "weather": form_data["weather"],
        "carrier": form_data.get("carrier", "Delhivery"),  # Default if not provided
    }


web_app = Flask(__name__)


@web_app.route("/")
def landing_page():
    return render_template("form.html")


@web_app.route("/predict", methods=["POST"])
def handle_prediction_request():
    shipment_payload = _collect_form_payload(request.form)
    prediction_summary = estimate_delay(shipment_payload)

    return render_template(
        "result.html",
        delay=prediction_summary["predicted_delay_days"],
        reason=prediction_summary["reason"],
        route_type="Fastest",
        transport_mode="Road",
        carrier_name="Blue Dart",
        weather_impact="High",
        risk_score=87,
        suggested_action="Switch to Rail mode or re-route via NH48",
    )


@web_app.route("/download_pdf")
def export_pdf_report():
    report_payload = _clone_summary_payload()

    html_content = render_template("delay_prediction.html", **report_payload)
    pdf_buffer = BytesIO()
    pdf_document = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), pdf_buffer)

    if pdf_document.err:
        return "PDF generation failed"

    pdf_response = make_response(pdf_buffer.getvalue())
    pdf_response.headers["Content-Type"] = "application/pdf"
    pdf_response.headers["Content-Disposition"] = f"attachment; filename={PDF_FILENAME}"
    return pdf_response


@web_app.route("/download_csv")
def export_csv_report():
    report_payload = _clone_summary_payload()

    csv_buffer = BytesIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(["Field", "Value"])
    for field_name, field_value in report_payload.items():
        csv_writer.writerow([field_name, field_value])
    csv_buffer.seek(0)

    return Response(
        csv_buffer.read(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={CSV_FILENAME}"},
    )


@web_app.route("/api/predict")
def prediction_endpoint():
    prediction_summary = estimate_delay()
    return jsonify(prediction_summary)


if __name__ == "__main__":
    web_app.run(debug=True, port=5001, host='0.0.0.0')
