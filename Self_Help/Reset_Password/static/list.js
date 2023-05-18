$(document).ready(function() {
$('select').on('change', function() {
  var selectedValues = [];
  $('select').each(function() {
    var thisValue = this.value;
    if(thisValue !== '')
      selectedValues.push(thisValue);
  }).each(function() {
    $(this).find('option:not(:selected)').each(function() {
      if( $.inArray( this.value, selectedValues ) === -1 ) {
        $(this).removeAttr('hidden');
      } else {
        if(this.value !== '')
          $(this).attr('hidden', 'hidden');
      }
    });
  });
});
});