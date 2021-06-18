from flask import Blueprint, request

instru = Blueprint('instru', __name__)

@instru.route('/instru-control')
def instru_control():
    threshold_high = request.form.get('high')
    threshold_low = request.form.get('low')

