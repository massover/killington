!function($) {
    "use strict";

    var Page = function() {
        this.$topSection = $('#home-fullscreen'),
        this.$topNavbar = $("#navbar-menu"),
        this.$stickyElem = $("#sticky-nav"),
        this.$backToTop = $('#back-to-top'),
        this.$goToRegister = $('.go-to-register')
    };

    //
    Page.prototype.init = function () {
        var $this = this;
        //window related event

        //Handling load event
        $(window).on('load', function() {
            var windowHeight = $(window).height();
            // adding height attr to top section
            $this.$topSection.css('height', windowHeight);

            //init sticky
            $this.$stickyElem.sticky({topSpacing: 0});
        });

        //Handling the resize event
        $(window).on('resize', function() {
            var windowHeight = $(window).height();
            $this.$topSection.css('height', windowHeight);
        });

        //Handling the scroll event
        $(window).scroll(function(){
            if ($(this).scrollTop() > 100) {
                $this.$backToTop.fadeIn();
            } else {
                $this.$backToTop.fadeOut();
            }
        });

        this.$goToRegister.on('click', function(event){
            var $anchor = $(event.target);
            $('html, body').stop().animate({
                scrollTop: $('#register').offset().top - 0
            }, 1500, 'easeInOutExpo');
            event.preventDefault();
        })

        //back-to-top button
        $this.$backToTop.click(function(){
            $("html, body").animate({ scrollTop: 0 }, 1000);
            return false;
        });

    },
    //init
    $.Page = new Page, $.Page.Constructor = Page
}(window.jQuery),

//initializing
function($) {
    "use strict";
    $.Page.init()
}(window.jQuery);