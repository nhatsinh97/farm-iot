<!DOCTYPE html>
<html lang="vi" prefix="og: https://ogp.me/ns#"><head>
	<meta charset="UTF-8">
    <style>
body {margin:0;height:2000px;}

.icon-bar {
  position: fixed;
  top: 50%;
  -webkit-transform: translateY(-50%);
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
}

.icon-bar a {
  display: block;
  text-align: center;
  padding: 16px;
  transition: all 0.3s ease;
  color: white;
  font-size: 20px;
}

.icon-bar a:hover {
  background-color: #000;
}

.facebook {
  background: #3B5998;
  color: white;
}

.twitter {
  background: #55ACEE;
  color: white;
}

.google {
  background: #dd4b39;
  color: white;
}

.linkedin {
  background: #007bb5;
  color: white;
}

.youtube {
  background: #bb0000;
  color: white;
}

.content {
  margin-left: 75px;
  font-size: 30px;
}
</style>

    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <base href="<?php echo CMS_BASE_URL; ?>"/>
    <title><?php echo isset($seo['title']) ? $seo['title'] : 'Farm Bình Thuận || Quản lý công việc'; ?></title>
    <link rel="shortcut icon" type="image/png" href="images/logo.png"/>
    <link href="public/templates/css/bootstrap.min.css" rel="stylesheet">
    <link href="public/templates/css/bootstrap-datepicker.css" rel="stylesheet">
    <link href="public/templates/css/bootstrap-datetimepicker.min.css" rel="stylesheet">
    <link href="public/templates/css/font-awesome.min.css" rel="stylesheet">
    <link href="public/templates/css/style.css" rel="stylesheet">
    <link href="public/templates/css/jquery-ui.min.css" rel="stylesheet">
    <link href="public/templates/css/jquery.datetimepicker.css" rel="stylesheet">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6346542718805639"
     crossorigin="anonymous"></script>
     <script async defer crossorigin="anonymous" src="https://connect.facebook.net/vi_VN/sdk.js#xfbml=1&version=v11.0" nonce="SOXKvZKo"></script>
</head>
<body>
<header>
    <?php echo phpversion(); $this->load->view('common/header', isset($data) ? $data : NULL); ?>
</header>



<div id="fb-root"></div>
<section class="main" role="main">
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2 padd-0">
                <?php $this->load->view('common/sidebar', isset($data) ? $data : NULL); ?>
            </div>
            <div class="col-md-10 padd-left-0">
                <div class="main-content">
                    <?php
                    $this->load->view('common/modal', isset($data) ? $data : NULL);
                    ?>
                    <?php
                    $this->load->view($template, isset($data) ? $data : NULL);
                    ?>
                </div>
            </div>
        </div>
    </div>
</section>
</body>
<script src="public/templates/js/jquery.js"></script>
<script src="public/templates/js/jquery-ui.min.js"></script>
<script src="public/templates/js/html5shiv.min.js"></script>
<script src="public/templates/js/respond.min.js"></script>
<script src="public/templates/js/bootstrap.min.js"></script>
<script src="public/templates/js/jquery.datetimepicker.full.js"></script>
<script src="public/templates/js/bootstrap-datepicker.min.js"></script>
<script src="public/templates/js/bootstrap-datepicker.vi.min.js"></script>
<script src="public/templates/js/ckeditor.js"></script>
<script src="public/templates/js/editor.js"></script>
<script src="public/templates/js/ajax.js"></script>
</html>