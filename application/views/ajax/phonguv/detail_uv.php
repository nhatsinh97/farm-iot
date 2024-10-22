<div class="breadcrumbs-fixed panel-action">
    <div class="row">
        <div class="orders-act">
            <div class="col-md-6">
                    <div class="btn-groups">
                            <button type="button" class="btn btn-primary" onclick="cms_vsell_order();"><i
                                    class="fa fa-plus"></i> Công việc mới
                            </button>
                            <button type="button" class="btn btn-primary"
                                    onclick="cms_print_order(1,<?php echo $data['_order']['ID']; ?>)"><i
                                    class="fa fa-print"></i> In
                            </button>
                            <button type="button" class="btn btn-primary"
                                    onclick="cms_javascript_redirect( cms_javascrip_fullURL() )"><i
                                    class="fa fa-arrow-left"></i> Quay lại
                            </button>
                            <br>
                </div>
            </div>
            <div class="col-md-4 col-md-offset-2">
                <div class="left-action text-left clearfix">
                    <h2>Mã công việc: &raquo;<span
                            style="font-style: italic; font-weight: 400; font-size: 16px;"><?php echo $data['_order']['output_code']; ?></span>
                    </h2>
                </div>
            </div>
        </div>
    </div>
</div>
<div class="main-space orders-space"></div>
<div class="orders-content">
    <div class="row">
        <div class="col-md-4">
            <div class="row">
                <div class="col-md-12">
                    <h4 class="lighter" style="margin-top: 0;">
                        <i class="fa fa-info-circle blue"></i>
                        Thông tin công việc | Lịch sử 
                    </h4>
                    <div class="morder-info" style="padding: 4px;">
                        <div class="tab-contents" style="padding: 8px 6px;">
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Mã công việc:</label>
                                </div>
                                <div class="col-md-7">
                                    <?php echo $data['_order']['output_code']; ?>
                                </div>
                                </div>
<!--          ------------------start sua --------------------- -->
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Khu vực:</label>
                                </div>
                                <div class="col-md-7">
                                    <?php echo cms_getNamecustomerbyID($data['_order']['customer_id']); ?>
                                </div>
                            </div>


                                
<!-- ----------------------------END sửa ------------------------- -->
                            
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Tên nhà:</label>
                                </div>
                                <div class="col-md-7" >
                                    <?php echo cms_getNamecustomerbyID($data['_order']['store_id']); ?>
                                </div>
                            </div>
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Ngày khắc phục:</label>
                                </div>
                                <div class="col-md-7">
                                    <?php echo ($data['_order']['sell_date'] != '0000-00-00 00:00:00') ? gmdate("H:i d/m/Y", strtotime(str_replace('-', '/', $data['_order']['sell_date'])) + 7 * 3600) : '-'; ?>
                                </div>
                            </div>
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Người khắc phục:</label>
                                </div>
                                <div class="col-md-7">
                                    <?php echo cms_getNameAuthbyID($data['_order']['sale_id']); ?>
                                </div>
                            </div>
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Nguyên nhân:</label>
                                </div>
                                <div class="col-md-7">
                                    <textarea readonly id="note-uv" cols="" class="form-control" rows="3"
                                              style="border-radius: 0;"><?php echo $data['_order']['notes']; ?></textarea>
                                </div>
                            </div>
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Cách khắc phục:</label>
                                </div>
                                <div class="col-md-7">
                                    <textarea readonly id="note-order2" cols="" class="form-control" rows="3"
                                              style="border-radius: 0;"><?php echo $data['_order']['notes2']; ?></textarea>
                                </div>
                            </div>
<!-- code thêm -->



                        </div>
                    </div>
                </div>
                <div class="col-md-12">
                    <div class="morder-info" style="padding: 4px;">
                        <div class="tab-contents" style="padding: 8px 6px;">
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Hình thức</label>
                                </div>
                                <div class="col-md-7">
                                    <div class="input-group">
                                        <input disabled type="radio" class="payment-method" name="method-pay"
                                               value="1" <?php echo ($data['_order']['payment_method'] == 1) ? 'checked' : ''; ?>>
                                        ĐỊNH KỲ &nbsp;
                                        <input disabled type="radio" class="payment-method" name="method-pay"
                                               value="2" <?php echo ($data['_order']['payment_method'] == 2) ? 'checked' : ''; ?>>
                                        SỰ CỐ&nbsp;
                                        <input disabled type="radio" class="payment-method" name="method-pay"
                                               value="3" <?php echo ($data['_order']['payment_method'] == 3) ? 'checked' : ''; ?>>
                                        KHÁC&nbsp;
                                    </div>

                                </div>
                            </div>
                            <!--       start  bỏ         -->
                            <!-- <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Tiền hàng</label>
                                </div>
                                <div class="col-md-7">
                                    <div class="">
                                        <?php echo cms_encode_currency_format($data['_order']['total_price']); ?>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Chiếc khấu</label>
                                </div>
                                <div class="col-md-7">
                                    <div><?php echo cms_encode_currency_format($data['_order']['coupon']); ?></div>
                                </div>
                            </div>
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Tổng cộng</label>
                                </div>
                                <div class="col-md-7">
                                    <div class="">
                                        <?php echo cms_encode_currency_format($data['_order']['total_money']); ?>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5 padd-right-0">
                                    <label>Khách đưa</label>
                                </div>
                                <div class="col-md-7 orange">
                                    <?php echo cms_encode_currency_format($data['_order']['customer_pay']); ?>
                                </div>
                            </div>
                            <div class="form-group marg-bot-10 clearfix">
                                <div class="col-md-5">
                                    <label>Còn nợ</label>
                                </div>
                                <div class="col-md-7">
                                    <div
                                        class=""><?php echo cms_encode_currency_format($data['_order']['lack']); ?></div>
                                </div>
                            </div> -->
                            <!--     end bỏ    -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-8">
            <h4 class="lighter" style="margin-top: 0;">
                        <i class="fa fa-info-circle blue"></i>
                        Thông tin xuất vật dụng 
                    </h4>
            <table class="table table-bordered table-striped" style="margin-top: 30px;">
                <thead>
                <tr>
                    <th class="text-center">STT</th>
                    <th>Mã CODE</th>
                    <th>Tên phụ tùng</th>
                    <th class="text-center">Số lượng</th>
                    <th class="text-center">Giá thành</th>
                    <th class="text-center">Còn tồn</th>
                </tr>
                </thead>
                <tbody>
                <?php if (isset($_list_products) && count($_list_products)) :
                    $nstt = 1;
                    foreach ($_list_products as $product) :
                        ?>
                        <tr data-id=<?php echo '"' .$product['ID'] .'"'?>>

                            <td class="text-center"><?php echo $nstt++; ?></td>
                            <td><?php echo $product['prd_code']; ?></td>
                            <td><?php echo $product['prd_name']; ?></td>
                            <td class="text-center" style="max-width: 30px;"><?php echo $product['quantity']; ?> </td>
                            <td class="text-center price-uv"><?php echo cms_encode_currency_format($product['price']); ?></td>
                            <td class="text-center"><?php echo "ID=" .$product['ID'];?></td>
                        </tr>
                    <?php endforeach; endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>