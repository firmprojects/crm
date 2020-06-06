
function formatAMPM(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12;
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = hours + ':' + minutes + ampm;
  return strTime;
}

function sec_to_hrs_min(seconds) {
  var minutes = (seconds / 60).toFixed(1);
  var hours = (seconds / (60 * 60)).toFixed(1);
  var days = (seconds / (60 * 60 * 24)).toFixed(1);

  if (seconds < 60) {
      return seconds.toFixed(1) + " Sec";
  } else if (minutes < 60) {
      return minutes + " Min";
  } else if (hours < 24) {
      return hours + " Hrs";
  } else {
      return days + " Days"
  }
}
