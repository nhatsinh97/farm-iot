<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <base href="<?php echo CMS_BASE_URL; ?>"/>
    <link rel="shortcut icon" type="image/png" href="public/templates/images/check.png"/>
    <title><?php echo isset($seo['title']) ? $seo['title'] : 'Phần mềm quản lý công việc'; ?></title>
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
<section id="pos" class="main" role="main">
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-12 padd-left-0">
                <div class="main-content">
                    <?php
                    $this->load->view('common/modal', isset($data) ? $data : NULL);
                    ?>
                    <div >
                        <div class="row">
                            <div class="orders-act">
                                <div class="col-md-4">
                                        <div class="col-md-12">
                                                <h4 class="lighter" style="margin-top: 0;">
                                                  <i class="fa fa-info-circle blue"></i>
                                                  Thông tin công việc
                                                </h4>
                                                <br>
                                                <br>
                                            <div class="form-group marg-bot-10 clearfix">
                                                        <div class="col-md-4">
                                                            <label>Hình thức</label>
                                                        </div>
                                                        <div class="col-md-8">
                                                            <div class="input-group">
                                                                <input type="radio" class="payment-method"
                                                                       name="method-pay" value="1" checked>
                                                             Sửa chữa định kỳ &nbsp;
                                                                <input type="radio" class="payment-method"
                                                                       name="method-pay" value="2"> Khắc phục sự cố&nbsp;
                                                            </div>

                                                        </div>
                                                    </div>
                                                <div class="form-group marg-bot-10 clearfix">
                                                        <div style="padding:0px" class="col-md-4">
                                                            <label>Khu:</label>
                                                        </div>
                                                        <div class="col-md-8">
                                                            <div class="col-md-10 padd-0" style="position: relative;">
                                                                <input id="search-box-cys" class="form-control"
                                                                       type="text"
                                                                       placeholder="Nhập tên khu hoặc mã"
                                                                       style="border-radius: 3px 0 0 3px !important;"><span
                                                                    style="color: red; position: absolute; right: 5px; top:5px; "
                                                                    class="del-cys"></span>

                                                                <div id="cys-suggestion-box"
                                                                     style="border: 1px solid #444; display: none; overflow-y: auto;background-color: #fff; z-index: 2 !important; position: absolute; left: 0; width: 100%; padding: 5px 0px; max-height: 400px !important;">
                                                                    <div class="search-cys-inner"></div>
                                                                </div>
                                                            </div>
                                                            <div class="col-md-2 padd-0">
                                                                <button type="button" data-toggle="modal"
                                                                        data-target="#create-cust"
                                                                        class="btn btn-primary"
                                                                        style="border-radius: 0 3px 3px 0; box-shadow: none; padding: 7px 11px;">
                                                                    new
                                                                </button>
                                                            </div>
                                                        </div>
                                                    </div>
                                                <div class="form-group marg-bot-10 clearfix">
                                                         <div style="padding:0px" class="col-md-4">
                                                            <label>Tên nhà:</label>
                                                         </div>
                                                            <?php if(isset($data['store'])){ ?>
                                                         <div class="col-md-8">
                                                               <select id="store-id" class="form-control" style="margin: 8px auto">
                                                               <?php foreach ($data['store'] as $key => $item) :?>
                                                               <option <?php if($item['ID']==$data['store_id']) echo 'selected '; ?> value="<?php echo $item['ID']; ?>">
                                                               <?php echo $item['stock_name']; ?></option>
                                                               <?php endforeach;?>
                                                               </select>
                                                               <?php } ?>
                                                         </div>
                                                         <div class="form-group marg-bot-10 clearfix">
                                                           <div style="padding:0px" class="col-md-4">
                                                            <label>Tên nhân viên:</label>
                                                           </div>
                                                           <div class="col-md-8">
                                                               <select class="form-control" id="sale_id">
                                                                <option value="">Tìm nhân viên</option>
                                                                 <?php foreach ($data['sale'] as $item) { ?>
                                                                        <option
                                                                        value="<?php echo $item['id']; ?>"><?php echo $item['display_name']; ?></option>
                                                                        <?php } ?>
                                                               </select>
                                                           </div>
                                                         </div>
                                                    <div class="form-group marg-bot-10 clearfix">
                                                            <div style="padding:0px" class="col-md-4">
                                                            <label>Nguyên nhân:</label>
                                                            </div>
                                                            <div class="col-md-8">
                                                               <textarea id="note-uv" cols="" class="form-control" rows="3"
                                                               style="border-radius: 0;"></textarea>
                                                            </div>
                                                    </div>
                                                    <div class="form-group marg-bot-10 clearfix">
                                                        <div style="padding:0px" class="col-md-4">
                                                            <label>Cách khắc phục:</label>
                                                        </div>
                                                        <div class="col-md-8">
                                                        <textarea id="note-order2" cols="" class="form-control" rows="3"
                                                        style="border-radius: 0;"></textarea>
                                                        </div>
                                                    </div>
                                                    
                                                </div>
                                            </div> ////
                                                    <div class="col-md-12">
                                                       <div class="morder-info" style="padding: 4px;">
                                                           <div class="tab-contents" style="padding: 8px 6px;">
                                                           <div class="form-group marg-bot-10 clearfix">
                                                                 <div class="col-md-4">
                                                                  <label>Giá thành:</label>
                                                                 </div>
                                                                 <div class="col-md-8">
                                                                   <div class="total-money">
                                                                    0
                                                                   </div>
                                                                  </div>
                                                            </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                             <div class="col-md-12">
                                            <div class="btn-groups pull-right" style="margin-bottom: 50px;">
                                                <button type="button" class="btn btn-primary"
                                                        onclick="cms_save_orders(3)"><i
                                                        class="fa fa-check"></i> Lưu
                                                </button>
                                                <a href="/quanlycongviec/dashboard">
                                                    <button type="button" class="btn btn-primary"
														onclick="cms_javascript_redirect( cms_javascrip_fullURL() )"><i
														class="fa fa-arrow-left"></i> Trở về
													</button>
                                                </a>
                                            </div>
                                        </div>
                                    //////////////// 
                                </div>
                                </div>
                                <div class="col-md-8">
                                    <div class="uv-search" style="margin: 10px 0px; position: relative;">
                                        <input type="text" class="form-control"
                                               placeholder="Nhập mã CODE hoặc tên vật dụng"
                                               id="search-pro-box">
                                    </div>
                                    <div class="product-results">
                                        <table class="table table-bordered table-striped">
                                            <thead>
                                            <tr>
                                                <th class="text-center">STT</th>
                                                <th>Mã CODE</th>
                                                <th>Tên vật dụng</th>
                                                <th class="text-center">Số lượng</th>
                                                <th class="text-center">Giá thành</th>
                                                <th class="text-center">Thành tiền</th>
                                                <th></th>
                                            </tr>
                                            </thead>
                                            <tbody id="pro_search_append">
                                            </tbody>
                                        </table>
                                        <div class="alert alert-success" style="margin-top: 30px;" role="alert">Gõ mã hoặc tên vật dụng vào hộp tìm kiếm để thêm vật dụng vào thông tin công việc!
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

    document.addEventListener('keyup', hotkey, false);
</script>
</html>