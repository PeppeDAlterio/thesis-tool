################ BEGIN OF TIMELINE HTML ################

timeline_head_html = """
<html>
<head>
<title>Timeline</title>
<style>
* {
  box-sizing: border-box;
}

/* Set a background color */
body {
  background-color: #474e5d;
  font-family: Helvetica, sans-serif;
}

/* The actual timeline (the vertical ruler) */
.timeline {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
}

/* The actual timeline (the vertical ruler) */
.timeline::after {
  content: '';
  position: absolute;
  width: 6px;
  background-color: white;
  top: 0;
  bottom: 0;
  left: 50%;
  margin-left: -3px;
}

/* Container around content */
.container {
  padding: 10px 40px;
  position: relative;
  background-color: inherit;
  width: 50%;
}

/* The circles on the timeline */
.container::after {
  content: '';
  position: absolute;
  width: 25px;
  height: 25px;
  right: -17px;
  background-color: white;
  border: 4px solid #FF9F55;
  top: 15px;
  border-radius: 50%;
  z-index: 1;
}

/* Place the container to the left */
.left {
  left: 0;
}

/* Place the container to the right */
.right {
  left: 50%;
}

/* Add arrows to the left container (pointing right) */
.left::before {
  content: " ";
  height: 0;
  position: absolute;
  top: 22px;
  width: 0;
  z-index: 1;
  right: 30px;
  border: medium solid white;
  border-width: 10px 0 10px 10px;
  border-color: transparent transparent transparent white;
}

/* Add arrows to the right container (pointing left) */
.right::before {
  content: " ";
  height: 0;
  position: absolute;
  top: 22px;
  width: 0;
  z-index: 1;
  left: 30px;
  border: medium solid white;
  border-width: 10px 10px 10px 0;
  border-color: transparent white transparent transparent;
}

/* Fix the circle for containers on the right side */
.right::after {
  left: -16px;
}

/* The actual content */
.content {
  padding: 20px 30px;
  background-color: white;
  position: relative;
  border-radius: 6px;
}

/* Media queries - Responsive timeline on screens less than 600px wide */
@media screen and (max-width: 600px) {
/* Place the timelime to the left */
  .timeline::after {
    left: 31px;
  }

/* Full-width containers */
  .container {
    width: 100%;
    padding-left: 70px;
    padding-right: 25px;
  }

/* Make sure that all arrows are pointing leftwards */
  .container::before {
    left: 60px;
    border: medium solid white;
    border-width: 10px 10px 10px 0;
    border-color: transparent white transparent transparent;
  }

/* Make sure all circles are at the same spot */
  .left::after, .right::after {
    left: 15px;
  }

/* Make all right containers behave like the left ones */
  .right {
    left: 0%;
  }
}
</style>
</head>
<body>

<div style="text-align: center; color: white;">
    <h1>Detection Id: $detectionId$</h1>
</div>

<div class="timeline">
"""

timeline_foot_html = """
</div>

</body>
</html>
"""

################# END OF TIMELINE HTML #################

#
#

################# BEGIN OF REPORT HTML #################

report_head_html = """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<title>
$app_name$ v. $app_version$ ($app_commit_id$) Security Report
</title>
<style type="text/css">

.tg  {border-collapse:collapse;border-color:#ccc;border-spacing:0;}
.tg td{background-color:#fff;border-color:#ccc;border-style:solid;border-width:1px;color:#333;
  font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{background-color:#f0f0f0;border-color:#ccc;border-style:solid;border-width:1px;color:#333;
  font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-baqh{text-align:center;vertical-align:top}
.tg .tg-amwm{font-weight:bold;text-align:center;vertical-align:top}
.tg .tg-l2oz{font-weight:bold;text-align:right;vertical-align:top}

body{
  font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
  color: #000;
  font-size: 13px;
}
h1{
  text-align: center;
  font-weight: bold;
  font-size: 32px
}
h3{
  font-size: 16px;
}
table{
  border: none;
  font-size: 13px;
}
td, th {
  padding: 3px 4px;
  word-break: break-word;
}
th{
  font-weight: bold;
}
.results th{
  text-align: left;
}
.spacer{
  margin: 10px;
}
.spacer-lg{
  margin: 40px;
}
.test-unknown{
  background-color: orange;
  color: #FFF;
}
.test-fail{
  background-color: red;
  color: #FFF;
}
.test-pass{
  background-color: green;
  color: #FFF;
}
.summary th{
  color: #FFF;
}
</style>
</head>
<body>
<h1>
$app_name$ v. $app_version$ ($app_commit_id$) Security Report
</h1>

<div class="spacer-lg"></div>

<div style="text-align: -webkit-center;">
$PLACE_STATS_TABLE_HERE$
</div>

<div class="spacer-lg"></div>

<table width="100%" class="results">
  
<tbody>
"""
################## END OF REPORT HTML ##################

#
#

############# BEGIN OF HISTORY REPORT HTML #############
history_report_head_html = """
<html>

<head>
<style src="https://stackpath.bootstrapcdn.com/bootswatch/3.3.7/slate/bootstrap.min.css"></style>
<style src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></style>
<style type="text/css">

.timeline{
  margin-top:20px;
  position:relative;
  
}

.timeline:before{
  position:absolute;
  content:'';
  width:4px;
  height:calc(100% + 50px);
background: rgb(138,145,150);
background: -moz-linear-gradient(left, rgba(138,145,150,1) 0%, rgba(122,130,136,1) 60%, rgba(98,105,109,1) 100%);
background: -webkit-linear-gradient(left, rgba(138,145,150,1) 0%,rgba(122,130,136,1) 60%,rgba(98,105,109,1) 100%);
background: linear-gradient(to right, rgba(138,145,150,1) 0%,rgba(122,130,136,1) 60%,rgba(98,105,109,1) 100%);
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#8a9196', endColorstr='#62696d',GradientType=1 );
  left:14px;
  top:5px;
  border-radius:4px;
}

.timeline-month{
  position:relative;
  padding:4px 15px 4px 35px;
  background-color:#444950;
  display:inline-block;
  width:auto;
  border-radius:40px;
  border:1px solid #17191B;
  border-right-color:black;
  margin-bottom:30px;
}

.timeline-month span{
  position:absolute;
  top:-1px;
  left:calc(100% - 10px);
  z-index:-1;
  white-space:nowrap;
  display:inline-block;
  background-color:#111;
  padding:4px 10px 4px 20px;
  border-top-right-radius:40px;
  border-bottom-right-radius:40px;
  border:1px solid black;
  box-sizing:border-box;
}

.timeline-month:before{
  position:absolute;
  content:'';
  width:20px;
  height:20px;
background: rgb(138,145,150);
background: -moz-linear-gradient(top, rgba(138,145,150,1) 0%, rgba(122,130,136,1) 60%, rgba(112,120,125,1) 100%);
background: -webkit-linear-gradient(top, rgba(138,145,150,1) 0%,rgba(122,130,136,1) 60%,rgba(112,120,125,1) 100%);
background: linear-gradient(to bottom, rgba(138,145,150,1) 0%,rgba(122,130,136,1) 60%,rgba(112,120,125,1) 100%);
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#8a9196', endColorstr='#70787d',GradientType=0 );
  border-radius:100%;
  border:1px solid #17191B;
  left:5px;
}

.timeline-section{
  padding-left:35px;
  display:block;
  position:relative;
  margin-bottom:30px;
}

.timeline-date{
  margin-bottom:15px;
  padding:2px 15px;
  background:linear-gradient(#74cae3, #5bc0de 60%, #4ab9db);
  position:relative;
  display:inline-block;
  border-radius:20px;
  border:1px solid #17191B;
  color:#fff;
text-shadow:1px 1px 1px rgba(0,0,0,0.3);
}
.timeline-section:before{
  content:'';
  position:absolute;
  width:30px;
  height:1px;
  background-color:#444950;
  top:12px;
  left:20px;
}

.timeline-section:after{
  content:'';
  position:absolute;
  width:10px;
  height:10px;
  background:linear-gradient(to bottom, rgba(138,145,150,1) 0%,rgba(122,130,136,1) 60%,rgba(112,120,125,1) 100%);
  top:7px;
  left:11px;
  border:1px solid #17191B;
  border-radius:100%;
}

.timeline-section .col-sm-4{
  margin-bottom:15px;
}

.timeline-box{
  position:relative;
  
 background-color:#444950;
  border-radius:15px;
  border-top-left-radius:0px;
  border-bottom-right-radius:0px;
  border:1px solid #17191B;
  transition:all 0.3s ease;
  overflow:hidden;
}

.box-icon{
  position:absolute;
  right:5px;
  top:0px;
}

.box-title{
  padding:5px 15px;
  border-bottom: 1px solid #17191B;
}

.box-title i{
  margin-right:5px;
}

.box-content{
  padding:5px 15px;
  background-color:#17191B;
}

.box-content strong{
  color:#666;
  font-style:italic;
  margin-right:5px;
}

.box-item{
  margin-bottom:5px;
}

.box-footer{
 padding:5px 15px;
  border-top: 1px solid #17191B;
  background-color:#444950;
  text-align:right;
  font-style:italic;
}
</style>
</head>

<body style="background-color: #272b30; color: c8c8c8;">

<div class="container">
  <div class="timeline">
"""

history_report_footer_html = """
  </div>
</div>

</body>

</html>
"""
############## END OF HISTORY REPORT HTML ##############