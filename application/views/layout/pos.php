<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <base href="<?php echo CMS_BASE_URL; ?>"/>
    <link rel="shortcut icon" type="image/png" href="images/logo.png"/>
    <title><?php echo isset($seo['title']) ? $seo['title'] : 'quản lý công việc'; ?></title>
    <link href="public/templates/css/bootstrap.min.css" rel="stylesheet">
    <link href="public/templates/css/font-awesome.min.css" rel="stylesheet">
    <link href="public/templates/css/style.css" rel="stylesheet">
    <link href="public/templates/css/jquery-ui.min.css" rel="stylesheet">
    <!--Start of Zendesk Chat Script-->
    <script type="text/javascript">
    window.$zopim||(function(d,s){var z=$zopim=function(c){z._.push(c)},$=z.s=
    d.createElement(s),e=d.getElementsByTagName(s)[0];z.set=function(o){z.set.
    _.push(o)};z._=[];z.set._=[];$.async=!0;$.setAttribute("charset","utf-8");
    $.src="https://v2.zopim.com/?2Z9j3qQJSSSIytel3Hsn5sCSk4aspfwy";z.t=+new Date;$.
    type="text/javascript";e.parentNode.insertBefore($,e)})(document,"script");
    </script>
    <!--End of Zendesk Chat Script-->
</head>
<body>
<header>
    <?php $this->load->view('common/header', isset($data) ? $data : NULL); ?>
</header>
<div id="fb-root"></div>
<script async defer crossorigin="anonymous" src="https://connect.facebook.net/vi_VN/sdk.js#xfbml=1&version=v11.0" nonce="SOXKvZKo"></script>
<section id="pos" class="main" role="main">
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-12 padd-left-0">
                <div class="main-content">
                    <?php
                    $this->load->view('common/modal', isset($data) ? $data : NULL);
                    //$user_name = cms_getNameAuthbyID($data_input['user_init']);
                    ?>
                    <div >
<!-- sinh sửa -->
                         <!--<form method="post" id="Upload" align="center" enctype="multipart/form-data"> -->
<!-- END sinh sửa /id="upload_form" -->
                        <div class="row">
                            <div class="fb-page" data-href="https://www.facebook.com/Arduino-219171748979799" data-tabs="Tr&#x1ea1;i B&#xec;nh Thu&#x1ead;n" data-width="1140" data-height="366" data-small-header="false" data-adapt-container-width="true" data-hide-cover="false" data-show-facepile="true"><blockquote cite="https://www.facebook.com/Arduino-219171748979799" class="fb-xfbml-parse-ignore"><a href="https://www.facebook.com/Arduino-219171748979799">Trại Bình Thuận</a></blockquote></div>
                            <div class="orders-act">
                                <div class="col-md-12">
                                            <div class="btn-groups pull-right" style="margin-bottom: 50px;">
                                                 <!--<input type="submit" name="upload" id="upload" value="Lưu (1)"  class="btn btn-primary"   class="fa fa-check"/> -->
                                                <button type="button" class="btn btn-primary"
                                                        onclick="cms_save_orders(3)"><i
                                                        class="fa fa-check"></i> Lưu 
                                                </button>
                                                <a href="./dashboard">
                                                    <button type="button" class="btn btn-primary"
                                                        onclick="cms_javascript_redirect( cms_javascrip_fullURL() )"><i
                                                        class="fa fa-arrow-left"></i> Trở về
                                                    </button>
                                                </a>
                        <!-- </form>  -->
                                            </div>
                                        </div>




                                <div class="col-md-8">
                                    <div class="uv-search" style="margin: 10px 0px; position: relative;">
                                        <input type="text" class="form-control"
                                               placeholder="Nhập mã vật dụng hoặc tên vật dụng"
                                               id="search-pro-box">
                                    </div>
                                    <div class="product-results">
                                        <table class="table table-bordered table-striped">
                                            <thead>
                                            <tr>
                                                <th class="text-center">STT</th>
                                                <th>Mã vật dụng</th>
                                                <th>Tên vật dụng</th>
                                                <th class="text-center">Số lượng</th>
                                                <th class="text-center">Giá tiền</th>
                                                <th class="text-center">Còn tồn 123</th>
                                                <th></th>
                                            </tr>
                                            </thead>
                                            <tbody id="pro_search_append">
                                            </tbody>
                                        </table>
                                        <div class="alert alert-success" style="margin-top: 30px;" role="alert">Gõ mã hoặc tên vật dụng vào hộp tìm kiếm để thêm vật dụng vào công việc
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row">
                                        <div class="col-md-12">
                                            <h4 class="lighter" style="margin-top: 0;">
                                                <i  class="fa fa-info-circle blue"></i>
                                                THÔNG TIN CÔNG VIỆC
                                            </h4>
                                            <div class="morder-info" style="padding: 4px;">
                                                <div class="tab-contents" style="padding: 8px 6px;">
                                                    <div class="form-group marg-bot-10 clearfix">
                                                        <div style="padding:0px" class="col-md-4">
                                                            <label>TÊN KHU:</label>
                                                        </div>
                                                        <div class="col-md-8">
                                                            <div class="col-md-10 padd-0" style="position: relative;">
                                                                <input id="search-box-cys" class="form-control"
                                                                       type="text"
                                                                       placeholder="Tìm khu"
                                                                       style="border-radius: 3px 0 0 3px !important;"><span
                                                                    style="color: red; position: absolute; right: 5px; top:5px; "
                                                                    class="del-cys"></span>

                                                                <div id="cys-suggestion-box"
                                                                     style="border: 1px solid #444; display: none; overflow-y: auto;background-color: #fff; z-index: 2 !important; position: absolute; left: 0; width: 100%; padding: 5px 0px; max-height: 400px !important;">
                                                                    <div class="search-cys-inner"></div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                        </div>
                                                           <div class="form-group marg-bot-10 clearfix">
                                                                 <div style="padding:0px" class="col-md-4" >
                                                                  <label>TÊN NHÀ:</label>
                                                                 </div>
                                                                 <div class="col-md-8" style="position: relative;">
                                                                 <?php if(isset($data['store'])){ ?>
                                                                 <select id="store-id" class="col-md-8">
                                                                  <?php foreach ($data['store'] as $key => $item) :?>
                                                                    <option <?php if($item['ID']==$data['store_id']) echo 'selected '; ?> value="<?php echo $item['ID']; ?>">
                                                                    <?php echo $item['stock_name']; ?></option>
                                                                      <?php endforeach;?>
                                                                 </select>
                                                                 <?php } ?>
                                                             </div>
                                                            </div>
                                                            <!-- <div class="form-group marg-bot-10 clearfix">
                            <div style="padding:0px" class="col-md-4">
                                <label>Người nhập</label>
                            </div>
                            <div class="col-md-8">
                                <?php echo cms_getNameAuthbyID($data['_import']['user_init']); ?>
                            </div>
                        </div> -->
                                                         <div class="form-group marg-bot-10 clearfix">
                                                             <div style="padding:0px" class="col-md-4">
                                                                 <label>NHÂN VIÊN:</label>
                                                             </div>
                                                             <div class="col-md-8">
                                                               <select class="form-control" id="sale_id">
                                                                  <option value="">Lựa chọn nhân viên</option>
                                                                  <?php foreach ($data['sale'] as $item) { ?>
                                                                    <option
                                                                        value="<?php echo $item['id']; ?>"><?php echo $item['display_name']; ?></option>
                                                                    <?php } ?>
                                                               </select>
                                                             </div>
                                                         </div>
                                                         <div class="form-group marg-bot-10 clearfix">
                                                             <div style="padding:0px" class="col-md-4">
                                                               <label>NGUYÊN NHÂN:</label>
                                                             </div>
                                                             <div class="col-md-8">
                                                                <textarea id="note-uv" cols="" class="form-control" rows="3"
                                                                style="border-radius: 0;"></textarea>
                                                             </div>
                                                         </div>
                                                         <div class="form-group marg-bot-10 clearfix">
                                                             <div style="padding:0px" class="col-md-4">
                                                               <label>CÁCH KHẮC PHỤC:</label>
                                                             </div>
                                                             <div class="col-md-8">
                                                                <textarea id="note-order2" cols="" class="form-control" rows="3"
                                                                style="border-radius: 0;"></textarea>
                                                             </div>
                                                         </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-12">

                                            <div class="morder-info" style="padding: 4px;">
                                                <div class="tab-contents" style="padding: 8px 6px;">
                                                    <div class="form-group marg-bot-10 clearfix">
                                                        <div class="col-md-4">
                                                            <label>HÌNH THỨC:</label>
                                                        </div>
                                                        <div class="col-md-8">
                                                            <div class="input-group">
                                                                <input type="radio" class="payment-method"
                                                                       name="method-pay" value="1" checked>
                                                                 ĐỊNH KỲ &nbsp;
                                                                <input type="radio" class="payment-method"
                                                                       name="method-pay" value="2"> SỰ CỐ&nbsp;
                                                                <input type="radio" class="payment-method"
                                                                       name="method-pay" value="3"> KHÁC&nbsp;
                                                            </div>

                                                        </div>
                                                    </div>
                                                    <!-- <div class="form-group marg-bot-10 clearfix">
                                                        <div class="col-md-4">
                                                            <label>CHI PHÍ VẬT DỤNG:</label>
                                                        </div>
                                                        <div class="col-md-8">
                                                            <div class="total-money">
                                                                0
                                                            </div>
                                                        </div>
                                                    </div> -->
                                                    <div class="form-group marg-bot-10 clearfix">
                                                      <label>ẢNH SỰ CỐ:</label>
                                                      <input type="file" class="form-control" name="image_file" id="img_upload"/>
                                                    </div>
                                                    <div class="form-group marg-bot-10 clearfix">
                                                            <label>ẢNH KHẮC PHỤC:</label>
                                                            <input type="file" class="form-control" name="image_file" id="img_upload"/>
                                                        </div>
                                                </div> 
                                            </div>
                                        </div>
                                        <div class="col-md-12">
                                            <div class="btn-groups pull-right" style="margin-bottom: 50px;">
                                                 <!--<input type="submit" name="upload" id="upload" value="Lưu (1)"  class="btn btn-primary"   class="fa fa-check"/> -->
                                                <button type="button" class="btn btn-primary"
                                                        onclick="cms_save_orders(3)"><i
                                                        class="fa fa-check"></i> Lưu 
                                                </button>
                                                <a href="./dashboard">
                                                    <button type="button" class="btn btn-primary"
                                                        onclick="cms_javascript_redirect( cms_javascrip_fullURL() )"><i
                                                        class="fa fa-arrow-left"></i> Trở về
                                                    </button>
                                                </a>
                         <!--</form>  -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
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
<script src="public/templates/js/ajax.js"></script>
<script>
    $(function () {
        $("#search-pro-box").autocomplete({
            minLength: 1,
            source: 'orders/cms_autocomplete_products/',
            focus: function (event, ui) {
                $("#search-pro-box").val(ui.item.prd_code);
                return false;
            },
            select: function (event, ui) {
                cms_select_product_sell(ui.item.ID);
                $("#search-pro-box").val('');
                return false;
            }
        }).keyup(function (e) {
            if (e.which === 13) {
                cms_autocomplete_enter_sell();
                $("#search-pro-box").val('');
                $(".ui-menu-item").hide();
            }
        })
            .autocomplete("instance")._renderItem = function (ul, item) {
            return $("<li>")
                .append("<div>" + item.prd_code + " - " + item.prd_name + "</div>")
                .appendTo(ul);
        };
    });
    // start sinh sửa
    $(document).ready(function(){
      $('#upload_form').on('submit', function(e){  
           e.preventDefault();  
           if($('#image_file').val() == '')  
           {  
                alert("Chưa nhập hình ảnh!");  
           }  
           else  
           {   
            
            var data = new FormData(this);
            
             $.ajax({  
                     url:"https://traibinhthuan.com/quanlycongviec/orders/upload_hieu",   
                     method:"POST",  
                     data: data,
                     contentType: false,  
                     cache: false,  
                     processData:false,  
                     success:function(data)  
                     {  
                        console.log(data['notes']);
                        $('.ajax-success-ct').html('Đã lưu thành công đơn hàng.').parent().fadeIn().delay(1000).fadeOut('slow');
                        setTimeout(function () {
                            $('.btn-back').delay('1000').trigger('click');
                        }, 1000);
                       // location.reload();

                          
                     }  
                });  

 

               
           }  
      });  
 }); 
  // END sinh sửa 





    document.addEventListener('keyup', hotkey, false);
</script>
</html>