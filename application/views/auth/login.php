<ul class="validation-summary-errors col-md-10 col-md-offset-1">
            <?php echo validation_errors(); ?>
			
</ul>

     <!-- <h1>QUẢN LÝ </h1> -->

	       <div class="w3layoutscontaineragileits">
	       <h2>ĐĂNG NHẬP</h2>
		       <form action="" method="post">
			       <input type="text" name="data[username]" 
                   value="<?php echo cms_common_input(isset($_post) ? $_post : [], 'username'); ?>"
                   id="inputEmail3"  placeholder="Tên đăng nhập" required="">
            
			       <input for="inputPassword3" type="password" name="data[password]" 
                   value="<?php echo cms_common_input(isset($_post) ? $_post : [], 'password'); ?>" 
                   id="inputPassword3" placeholder="Mật khẩu" required="">
			    <ul class="agileinfotickwthree">
				    <li>
					 <input type="checkbox" id="brand1" value="">
					 <label for="brand1"><span></span>Lưu mật khẩu</label>
					 <a href="#">Quên mật khẩu?</a>
				    </li>
			    </ul>
			    <div class="aitssendbuttonw3ls">
                    <input type="submit" name="login" value="Đăng nhập" class="btn btn-primary btn-sm"/>
				    <p>Nhập lượng nước<span>→</span> <a class="w3_play_icon1" href="#small-dialog1"> Click Here</a></p>
				    <div class="clear"></div>
			    </div>
		        </form>
	        </div>
	
	<!-- for register popup -->
	<div id="small-dialog1" class="mfp-hide">
		<div class="contact-form1">
			<div class="contact-w3-agileits">
				<h3>Nhập giá trị lưu lượng nước hằng ngày</h3>
				<form action="#" method="post">
						<div class="form-sub-w3ls">
							<input placeholder="Lưu lượng nước bơm 1"  type="text" required="">&ensp;
						</div>
						<div class="form-sub-w3ls">
							<input placeholder="Lưu lượng nước bơm 2" class="mail" type="text" required="">
						</div>
						<div class="form-sub-w3ls">
							<input placeholder="Lưu lượng nước bơm 3"  type="text" required="">
						</div>
						<div class="form-sub-w3ls">
							<input placeholder="Lưu lượng nước bơm 4"  type="text" required="">
							<div class="icon-agile">
								<i class="fa fa-unlock-alt" aria-hidden="true"></i>
							</div>
						</div>
					<div class="login-check">
						 <label class="checkbox"><input type="checkbox" name="checkbox" checked="">I Accept Terms & Conditions</label>
					</div>
					<div class="submit-w3l">
						<input type="submit" value="Register">
					</div>
				</form>
			</div>
		</div>	
	</div>
	<!-- //for register popup -->


	
	<div class="w3footeragile">
		<p> &copy; 2021 Website quản lý công việc | Design by <a href="http://w3layouts.com" target="_blank">Nguyễn Nhất Sinh</a></p>
	</div>

	
	<script type="text/javascript" src="js/jquery-2.1.4.min.js"></script>

	<!-- pop-up-box-js-file -->  
		<script src="js/jquery.magnific-popup.js" type="text/javascript"></script>
	<!--//pop-up-box-js-file -->
	<script>
		$(document).ready(function() {
		$('.w3_play_icon,.w3_play_icon1,.w3_play_icon2').magnificPopup({
			type: 'inline',
			fixedContentPos: false,
			fixedBgPos: true,
			overflowY: 'auto',
			closeBtnInside: true,
			preloader: false,
			midClick: true,
			removalDelay: 300,
			mainClass: 'my-mfp-zoom-in'
		});
																		
		});
	</script>
    