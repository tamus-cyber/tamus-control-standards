jQuery(document).ready(function($) {

	// ------------------------------------------
	// Search -----------------------------------
	// ------------------------------------------
	var searchbutton = $('.nav-primary li.search');
	var searchformarea = $('.search-form-area');

	searchbutton.on( 'click', function() {
		searchformarea.slideToggle('fast');
	});

  const searchform = document.getElementsByName('search')[0];
  const searchquery = document.getElementById('header-search-input');
  const google = 'https://www.google.com/search?q=site%3A';
  const site = 'cyber-standards.tamus.edu';

  function search_submitted(event) {
    event.preventDefault();
    const url = google + site + '+' + searchquery.value;
    const win = window.open(url, '_blank');
    win.focus();
  }

  searchform.addEventListener('submit', search_submitted);


  // ------------------------------------------
  // Header scroll ----------------------------
  // ------------------------------------------
  var siteheader = $('.site-header');
  var headerheight = siteheader.height();

  var oitlogo = $('#tamus-oit-logo');
  var oitlogoheight = oitlogo.height();
  var headercompressed = headerheight - oitlogoheight;


  $(function () {
    $(window).scroll(function () {
      if ($(window).scrollTop() > headerheight) {
      	siteheader.addClass('scrolled');
      }

      if ($(window).scrollTop() <= headercompressed) {
      	siteheader.removeClass('scrolled');
      }
  	});
  });


  /**
	 * Toggle aria attributes.
   * Adapted from _toggleAria in genesis\lib\js\menu\responsive-menus.js
	 *
	 * @param  {button} $this     passed through
	 * @param  {aria-xx} attribute aria attribute to toggle
   * @since   2.0.0
	 * @return {bool}           from _ariaReturn
	 */
	function _toggleAria( $this, attribute ) {
		$this.attr(
			attribute, function( index, value ) {
				return 'false' === value;
			}
		);
	}


  /**
   * On desktop, move the #oit-site-menu links beneath the logo.
   * On mobile, move the #oit-site-menu links to the primary nav.
   * When the DOM first loads, it is in the primary nav menu.
   * @param  {string} subMenuMarkup - html markup for the OIT submenu
	 * @param  {number} currentWidth - Width of the page
	 * @param  {string} callMethod - Either 'pageLoad' or 'resize'
   * @since   2.0.0
   */
  function placeOITMenu(subMenuMarkup, currentWidth, callMethod) {
    type = typeof(subMenuMarkup);

    if (currentWidth >= 992) {
      if ($('.header-widget-area #oit-site-sub-menu').length == 0) {

        // Append the #oit-site-menu links beneath the logo in the header
        $(subMenuMarkup).insertAfter('#tamus-oit-logo');

        // Genesis is adding display:none inline. After moving to .header-widget-area, change display:none to display:flex
        $('.header-widget-area #oit-site-sub-menu').css('display', 'flex');

        $('#oit-site-menu #oit-site-sub-menu').remove();
      }
    }
    else {
      subMenuButton = $('#oit-sub-menu-toggle');

      // Check to see if the sub-menu is already in the primary menu
      if ($('#oit-site-menu #oit-site-sub-menu').length == 0) {
        // If not, add the #oit-site-menu links beneath the OIT link in the primary menu
        $(subMenuMarkup).insertAfter(subMenuButton);
      }

      // If the desktop nav element is in the header, remove it
      if ($('.header-widget-area #oit-site-sub-menu').length > 0) {
        $('.header-widget-area #oit-site-sub-menu').remove();
      }

      /**
       * On click, toggle aria attributes, toggle sub-menu
       * Adapted from _submenuToggle function in genesis\lib\js\menu\responsive-menus.js
       * .off will unbind other click events that interfere with our functionality
       */
      $('#oit-sub-menu-toggle').off('click').on('click', function() {
        var subMenuButtonClass  = 'sub-menu-toggle';
        var $this  = $(this),
          others = $this.closest( '.menu-item' ).siblings();
        _toggleAria( $this, 'aria-pressed' );
        _toggleAria( $this, 'aria-expanded' );
        $this.toggleClass( 'activated' );
        $('#oit-site-sub-menu').slideToggle( 'fast' );

        others.find( '.' + subMenuButtonClass ).removeClass( 'activated' ).attr( 'aria-pressed', 'false' );
        others.find( '.sub-menu' ).slideUp( 'fast' );
      });
    }
  } // end function placeOITMenu


  subMenu       = $('#oit-site-sub-menu');
  subMenuMarkup = null;

  // Check to see if the #oit-site-sub-menu exists
  if($(subMenu).length > 0){
    subMenuMarkup = $(subMenu[0].outerHTML);
  }

  // If the sub menu has html, run the placeOITMenu function on page load and resize
  if (subMenuMarkup !== null){
    // Width when the page is loaded
    currentWidth = $(window).width();

    // On page load, place the OIT links in the header on desktop, primary nav on mobile
    placeOITMenu(subMenuMarkup, currentWidth, 'pageLoad');

    // Check width when the page is resized
    $(window).on('resize', function() {
      currentWidth = $(window).width();
      placeOITMenu(subMenuMarkup, currentWidth, 'resize');
    });
  }



  /**
   * We were doing this with nth-of-type but it won't work if cards are in different parent divs,
   * nth-of-type always looks at the element's index relative to it's direct parent, so it won't work across the whole page.
   * src: https://stackoverflow.com/questions/17159644/css3-nth-of-type-across-the-entire-page
   *
   * Targeting only direct descendants of .cards, nested columns will be skipped
   */
  var index = 0;
  $('body').find('.cards > .wp-block-column').each(function() {
      $(this).addClass('card-' + [index++]);
  });

  // Add the current year in the footer
  var currentYear = new Date().getFullYear();
  $('#year').html(currentYear);
});