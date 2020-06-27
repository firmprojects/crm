var timer = new easytimer.Timer();
var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];


$(document).ready(function () {

  $("#today_").html(`${moment().format("dddd, MMMM DD")}`)
  $.ajax({
    type:'GET',
    url:"{% url 'users:get_date_on_refresh' %}",
    success:(res)=>{
      if(res['time'] == 'No'){
        $("#clock_in_time").html("--:--:--")
      }
      else {
        let clocked_in = new Date(res['time']);

        $("#clock_in_time").html(`${formatAMPM(clocked_in)}`)
        console.log((Date.now() - clocked_in)/1000);
        timer.start({startValues: {seconds: (Date.now() - clocked_in)/1000}});
        timer.addEventListener('secondsUpdated', function (e) {
            $('#timer').html(timer.getTimeValues().toString());
        });

      }

    }
  })

  getWeeklyReport()
})
function getWeeklyReport() {
  let start = moment().subtract(7, 'days').format('YYYY-MM-DD')
  let end = moment().format('YYYY-MM-DD')
  $("#from_to_week").html(`${start} to ${end}`)
  $.ajax({
    type:'POST',url:"/get_weekly_report/",data:{"start":start,"end":end,"csrfmiddlewaretoken":"{{ csrf_token }}"},
    success:(res)=>{
      $("#weekly_report").html('')
      for(let day of Object.keys(res['report'])){
        let row_data = ''
        let total_time = 0
        res['report'][day].map((item,i)=>{
          let data = ''
          if(i===0){
            let current = new Date(day)
            console.log(current);
            data+=`
            <th rowspan=${res['report'][day].length}>${moment().format("dddd, MMMM DD")}</th>
            <th rowspan=${res['report'][day].length}>${sec_to_hrs_min(res['hours_spent'][day])}</th>
            `
          }
          let clock_in = new Date(item['clock_in'])
          if(item['clock_out'] === undefined){

            data+=`<td>${formatAMPM(clock_in)}</td><td>--</td>`
          }
          else{
            let clock_out = new Date(item['clock_out'])
            total_time+=clock_out - clock_in

            data+=`<td>${formatAMPM(clock_in)}</td><td>${formatAMPM(clock_out)}</td>`
          }

          row_data+=`<tr>${data}</tr>`

        })

        $("#weekly_report").append(`<tr>${row_data}</tr>`)
      }
    }
  })
}
function clockIn(){
  $.ajax({
    type:'POST',
    data:{"data":JSON.stringify({'date':moment().format(),'today':`${moment().format("YYYY-MM-DD")}`})},
    url:"{% url 'users:clock_in' %}",
    success: (res)=>{
      date = new Date(res['time_now'])
      $("#clock_in_time").html(formatAMPM(date))
      timer.start();
      timer.addEventListener('secondsUpdated', function (e) {
          $('#timer').html(timer.getTimeValues().toString());
      });
    }
  })
}
function clockOut(){
  let today = new Date()
  $.ajax({
    type:'POST',
    data:{"data":JSON.stringify({'today':`${moment().format("YYYY-MM-DD")}`})},
    url:"{% url 'users:clock_out' %}",
    success: (res)=>{
      timer.stop();
      getWeeklyReport()
    }
  })
}
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
