// Minimal JavaScript for UI enhancements + booking estimate
document.addEventListener('DOMContentLoaded', function() {
  // Enable bootstrap tooltips if present
  if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (el) { return new bootstrap.Tooltip(el); });
  }

  // Booking estimate & client-side validation
  var bookingWidget = document.getElementById('booking-widget');
  if (bookingWidget) {
    var price = parseFloat(bookingWidget.dataset.price);
    var startSel = bookingWidget.querySelector('[name="start_time"]') || document.querySelector('[name="start_time"]');
    var endSel = bookingWidget.querySelector('[name="end_time"]') || document.querySelector('[name="end_time"]');
    var estEl = document.getElementById('estimated-price');
    var form = bookingWidget.querySelector('form');

    function formatVND(n) {
      try { return new Intl.NumberFormat('vi-VN').format(n); } catch (e) { return n.toString(); }
    }

    function computeEstimate() {
      if (!estEl) return;
      if (!startSel || !endSel) { estEl.textContent = ''; return; }
      var sVal = startSel.value;
      var eVal = endSel.value;
      if (!sVal || !eVal) { estEl.className = 'alert alert-secondary small mb-3'; estEl.textContent = 'Ước tính: —'; return; }
      var sHour = parseInt(sVal.split(':')[0],10);
      var eHour = parseInt(eVal.split(':')[0],10);
      var hours = eHour - sHour;
      if (isNaN(hours) || hours <= 0) {
        estEl.className = 'alert alert-danger small mb-3';
        estEl.textContent = 'Giờ kết thúc phải lớn hơn giờ bắt đầu';
      } else {
        var total = hours * price;
        estEl.className = 'alert alert-info small mb-3';
        estEl.textContent = 'Ước tính: ' + formatVND(total) + ' VND (' + hours + ' giờ)';
      }
    }

    [startSel, endSel].forEach(function(el) { if (el) el.addEventListener('change', computeEstimate); });
    if (form) {
      form.addEventListener('submit', function(e) {
        var sVal = startSel ? startSel.value : null;
        var eVal = endSel ? endSel.value : null;
        if (sVal && eVal) {
          var sHour = parseInt(sVal.split(':')[0],10);
          var eHour = parseInt(eVal.split(':')[0],10);
          if (isNaN(sHour) || isNaN(eHour) || eHour <= sHour) {
            e.preventDefault();
            computeEstimate();
            estEl.scrollIntoView({behavior:'smooth', block:'center'});
          }
        }
      });
    }
    computeEstimate();
  }
});
