<div class="content">
<div class="row">
<div class="report">
<div class="col-md-12">
    

<div class="row" style="background: #; margin: 20px 0; overflow: hidden; ">
    <div class="report">
    <div class="col-md-12"><center><h4 class="dashboard-title"><i class="fa fa-check-square"></i>THÔNG TIN TỔNG HỢP</h4></center></div>
    <div class="col-md-4">
        <div class="widget widget-blue">
            <div class="widget-header">
                <h3 class="widget-title"><i class="fa fa-play-circle"></i>HOẠT ĐỘNG TRẠI</h3>
            </div>
            <div class="widget-body">
                <div class="row">
                    <div class="info col-xs-7">CHI PHÍ TRẠI :</div>
                    <div
                        class="info col-xs-5 data text-right"><b><?php echo (isset($tongtien)) ? cms_encode_currency_format($tongtien) : '0'; ?></b></div>
                    <div class="info col-xs-7">TỔNG SỐ CÔNG VIỆC :</div>
                    <div
                        class="info col-xs-5 data text-right"><b><?php echo (isset($slsorders)) ? cms_encode_currency_format($slsorders) : '0'; ?></b></div>
                    <div class="info col-xs-7">SỐ VẬT DỤNG ĐÃ XUẤT :</div>
                    <div
                        class="info col-xs-5 data text-right"><b><?php echo (isset($slsitem)) ? cms_encode_currency_format($slsitem) : '0'; ?></b></div>
                    <div class="info col-xs-7">ĐANG CẬP NHẬT 1</div>
                    <div class="info col-xs-5 data text-right"><b>0</b></div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="widget widget-orange">
            <div class="widget-header">
                <h3 class="widget-title"><i class="fa fa-ioxhost"></i>THÔNG TIN KHO</h3>
            </div>
            <div class="widget-body">
                <div class="row">
                    <div class="info col-xs-7">TỒN KHO :</div>
                    <div
                        class="info col-xs-5 data text-right"><b><?php echo (isset($slsinventory)) ? cms_encode_currency_format($slsinventory) : '0'; ?></b></div>
                    <div class="info col-xs-7">HẾT HÀNG :</div>
                    <div
                        class="info col-xs-5 data text-right"><b><?php echo (isset($slsaceitem)) ? cms_encode_currency_format($slsaceitem) : '0'; ?></b></div>
                    <div class="info col-xs-7">SẮP HẾT HÀNG :</div>
                    <div class="info col-xs-5 data text-right"><b>0</b></div>
                    <div class="info col-xs-7">XUẤT ÂM :</div>
                    <div class="info col-xs-5 data text-right"><b>0</b></div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="widget widget-green">
            <div class="widget-header">
                <h3 class="widget-title"><i class="fa fa-barcode"></i>THÔNG TIN TỒN KHO</h3>
            </div>
            <div class="widget-body">
                <div class="row">
                    <div class="info col-xs-7">VẬT DỤNG :</div>
                    <div
                        class="info col-xs-5 data text-right"><b><?php echo (isset($data['_sl_product'])) ? $data['_sl_product'] : 0; ?></b></div>
                     <div class="info col-xs-7">NHÀ CUNG CẤP :</div>
                     <div
                        class="info col-xs-5 data text-right"><b><?php echo (isset($data['_sl_manufacture'])) ? $data['_sl_manufacture'] : 0; ?></b></div>
                    <div class="info col-xs-7">CHƯA NHẬP GIÁ :</div>
                    <div
                        class="info col-xs-5 data text-right"><b><?php echo (isset($lamgiaban)) ? cms_encode_currency_format($lamgiaban) : '0'; ?></b></div>
                    <div class="info col-xs-7">CHƯA NHẬP GIÁ :</div>
                    <div
                        class="info col-xs-5 data text-right"><b><?php echo (isset($lamgiamua)) ? cms_encode_currency_format($lamgiamua) : '0'; ?></b></div>
                    <!-- <div class="info col-xs-7">Loading ...</div> -->
                    <div class="info col-xs-5 data text-right"><b></b></div>
                </div>
            </div>
        </div>
    </div>
    </div>
</div>




<center>
    <h4 class="dashboard-title"><i class="fa fa-check-square"></i>Quét mã QR này để mở trang nhập công việc hằng ngày</h4>
    <br>
    <a href="https://docs.google.com/spreadsheets/d/1aJR5_3OdGttVt-XtIo_eAFORNribDcLWJ8MJ28JHzpI/edit?usp=sharing"><h4 class="dashboard-title"><i ></i>Cick vào đây để truy cập </h4></a>
    <br>
    <img class="fit-picture"
     src="images/h1.png"
     alt="Grapefruit slice atop a pile of other slices">
     <br><br>
     <a href="/download/cvt8.xlsx" download><h4 class="dashboard-title"><i ></i>Cick vào đây để tải file excel </h4></a>
     </center>
    <!--<iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&bgcolor=%23ffffff&ctz=Asia%2FHo_Chi_Minh&src=cWhvZDNvOWE3ajVzYzN2cjE4Y2Z2aWt1bm9AZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&src=azhuOXE0NjQwMmttZGplZjJmYzVpN2c2ZGtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&src=MzhmczNlaDZ1ZmZpNDhwMTRxYXEzcjRsZTRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%2333B679&color=%234285F4&color=%23E67C73&mode=AGENDA&showTz=1&showCalendars=1" style="border:solid 1px #777" width="450" height="600" frameborder="0" scrolling="no"></iframe>   -->
<!--<iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&bgcolor=%237CB342&ctz=Asia%2FHo_Chi_Minh&src=bmhhdHNpbmg5N0BnbWFpbC5jb20&src=cWhvZDNvOWE3ajVzYzN2cjE4Y2Z2aWt1bm9AZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&src=NzN1a2psMmY5bDNiOTllMmNrM3JyZ3MwMjBAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23AD1457&color=%2333B679&color=%238E24AA&mode=AGENDA&title=C%C3%94NG%20VI%E1%BB%86C%20H%E1%BA%B0NG%20NG%C3%80Y&showDate=0&showNav=1&showPrint=0&showTabs=1&showCalendars=1&showTz=0" style="border:solid 1px #777" width="470" height="600" frameborder="0" scrolling="no"></iframe> -->
</div>

        <div class="col-md-12">
           <center>
             <h4 class="dashboard-title"><i class="fa fa-check-square"></i>HOẠT ĐỘNG HÔM NAY</h4>
             </center>
            </div>


        <!-- <div class="col-md-3">
            <div class="report-box box-red">
                <div class="infobox-icon">
                    <i class="fa fa-arrow-circle-left"></i>
                </div>
                <div class="infobox-data">
                    <h3 class="infobox-title">Đang cập nhật 1</h3>
                    <span class="infobox-data-number">0</span>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="report-box box-orange">
                <div class="infobox-icon">
                    <i class="fa fa-soundcloud"></i>
                </div>
                <div class="infobox-data">
                    <h3 class="infobox-title">Đang cập nhật 2</h3>
                    <span class="infobox-data-number">0</span>
                </div>
            </div>
        </div> -->
    </div>
</div>

<!-- <div class="row" style="margin: 20px 0; overflow: hidden; ">
    <div class="chart-report">
        <div class="row">
            <div class="col-md-4">
                <div class="panel panel-default">
                    <div class="panel-heading"><i class="fa fa-align-left"></i>Biểu đồ chi phí tuần</div>
                    <div class="panel-body">
                        Loading ...
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="panel panel-default">
                    <div class="panel-heading"><i class="fa fa-globe"></i>Thông tin từ web</div>
                    <div class="panel-body">
                        Loading ...
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="panel panel-default">
                    <div class="panel-heading"><i class="fa fa-rss"></i>Tin chuyên ngành</div>
                    <div class="panel-body">
                        Loading ...
                    </div>
                </div>
            </div>
        </div>
    </div>
	
	
</div> -->

<script>
      //khai báo biến slideIndex đại diện cho slide hiện tại
      var slideIndex;
      // KHai bào hàm hiển thị slide
      function showSlides() {
          var i;
          var slides = document.getElementsByClassName("mySlides");
          var dots = document.getElementsByClassName("dot");
          for (i = 0; i < slides.length; i++) {
             slides[i].style.display = "none";  
          }
          for (i = 0; i < dots.length; i++) {
              dots[i].className = dots[i].className.replace(" active", "");
          }

          slides[slideIndex].style.display = "block";  
          dots[slideIndex].className += " active";
          //chuyển đến slide tiếp theo
          slideIndex++;
          //nếu đang ở slide cuối cùng thì chuyển về slide đầu
          if (slideIndex > slides.length - 1) {
            slideIndex = 0
          }    
          //tự động chuyển đổi slide sau 5s
          setTimeout(showSlides, 5000);
      }
      //mặc định hiển thị slide đầu tiên 
      showSlides(slideIndex = 0);


      function currentSlide(n) {
        showSlides(slideIndex = n);
      }
</script>
<div class="fb-page" data-href="https://www.facebook.com/Arduino-219171748979799" data-tabs="Tr&#x1ea1;i B&#xec;nh Thu&#x1ead;n" data-width="1140" data-height="366" data-small-header="false" data-adapt-container-width="true" data-hide-cover="false" data-show-facepile="true"><blockquote cite="https://www.facebook.com/Arduino-219171748979799" class="fb-xfbml-parse-ignore"><a href="https://www.facebook.com/Arduino-219171748979799">Arduino</a></blockquote></div>
    <div class="zalo-chat-widget" data-oaid="3611113386652115239" data-welcome-message="Rất vui khi được hỗ trợ bạn!" data-autopopup="2" data-width="350" data-height="420"></div>
<script src="https://sp.zalo.me/plugins/sdk.js"></script>
