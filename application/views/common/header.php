<nav id="navbar-container" class="navbar navbar- navbar-fixed-top">
    

    <div class="container-fluid">
        <!-- <div class="navbar-header">
            <button type="button" class="navbar-toggle menu-toggler pull-left" onclick="$('#sidebar').toggleClass('hidden-xs hidden-sm hidden-md')">
                <span class="sr-only">Thanh menu trên - Sidebar</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
        </div> -->
        
        <div class="dashboard-title" id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav navbar-right">
                <li class="dropdown user-profile">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true"
                       aria-expanded="false"><span class="hello">Xin chào, </span><?php echo (isset($user)) ?
                            $user['display_name'] : $user['username']; ?><span class="caret"></span></a>
                    <ul class="dropdown-menu">
                        <li><a href="dashboard"><i class="fa fa-home"></i>Trang chính</a></li>
                        <li><a href="account"><i class="fa fa-user-secret"></i>Tài khoản</a></li>
                        <li><a href="phonguv"><i class="fa fa-list-ol"></i>Lịch sử phòng UV</a></li>
                        <li><a href="orders"><i class="fa fa-list"></i>Lịch sử công việc BT</a></li>
                        <li><a href="customer"><i class="fa fa-history"></i>Lịch sử KHU</a></li>
                        <li><a href="setting"><i class="fa fa-cogs"></i>Thiết lập</a></li>
                        <li><a href="authentication/logout"><i class="fa fa-power-off"></i>Thoát</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>

